import pandas as pd
from tqdm import tqdm
from scholarly import scholarly
from classes.VectorCalculator import VectorCalculator
from classes.PromptManager import PromptManager


class ArticleProcessor:
    """Gestion de l'extraction et du traitement des articles."""
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key 
    
    def process_articles(self, task, question, output_format):
        """Ajout des vecteurs d'embedding et sauvegarde des articles."""
 
        prompt_manager = PromptManager(self.openai_api_key)
        
        # Extraction du sujet de la question et construction  du persona
        topic = prompt_manager.get_response_lines("Can define the topic of this question: " + question + ", in one word or two?")[0]
        persona = topic + "specialist of "
               
        # Extraction des articles
        df = self.extract_articles(topic)

        # Trier les articles par nombre de citations (ordre décroissant)
        dataset = df.sort_values(by="num_citations", ascending=False)
        
        # Sélection des articles les plus proches de la question
        dataset = self.find_closest_articles(dataset, question, 10) 
        
        contexte = dataset["abstract"].tolist()

        # Mise en forme du prompt        
        prompt = prompt_manager.create_prompt(persona, task, contexte, output_format)  
        response_en = prompt_manager.get_response_lines(prompt)
        
        # Reconstitution d'une chaîne de  caractères en vue de la traduction
        chaine_en = "\n".join(response_en)

        # Retourner la réponse en français                                
        return prompt_manager.get_response_lines("Peux-tu traduire le texte suivant en français: " + chaine_en)

    def extract_articles(self, topic, max_results=50):
        """Extraction des articles à partir de Google Scholar."""
        query = scholarly.search_pubs(topic)
        articles = []
        for i, pub in enumerate(tqdm(query, total=max_results, desc="Extraction des articles")):
            if i >= max_results:
                break
            bib = pub['bib']
            num_citations = pub.get('num_citations', 0)
            articles.append({
                "title": bib.get('title', 'No Title'),
                "author": bib.get('author', 'Unknown Author'),
                "year": bib.get('pub_year', 'Unknown Year'),
                "num_citations": num_citations,
                "abstract": bib.get('abstract', 'No Abstract')
            })
        return pd.DataFrame(articles)

    def find_closest_articles(self, dataset, question, top_n=10):
        """Trouve les articles les plus proches d'un texte de référence."""
        vector_calculator = VectorCalculator(self.openai_api_key)

        # Calcul des vecteurs avec une description
        tqdm.pandas(desc="Calcul des vecteurs des articles")
        dataset["vector"] = dataset.progress_apply(
            lambda row: vector_calculator.get_vector(row["abstract"]), axis=1)
        dataset = dataset.dropna(subset=["abstract"]).loc[dataset["abstract"] != ""]
        
        # Calcul du vecteur de référence
        reference_vector = vector_calculator.get_vector(question)

        # Calcul des distances avec une description
        tqdm.pandas(desc="Calcul des distances par rapport à la question")
        dataset["distance"] = dataset["vector"].progress_apply(
            lambda v: vector_calculator.get_distance(reference_vector, v, method="cosine")
        )
        
        return dataset.sort_values("distance", ascending=True).head(top_n)