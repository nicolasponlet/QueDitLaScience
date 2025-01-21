from serpapi.google_search import GoogleSearch
from tqdm import tqdm
from classes.PromptManager import PromptManager


class WebSearchProcessor:
    def __init__(self, openai_api_key, google_api_key):
        self.openai_api_key = openai_api_key 
        self.google_api_key = google_api_key

    def process_web_search(self, task, question, output_format):

        prompt_manager = PromptManager(self.openai_api_key)
        
        # Effectuer la recherche sur Internet en utilisant l'API Google
        headlines = self.internet_search(question)
        
        # Extraction du sujet de la question et construction  du persona
        topic = prompt_manager.get_response_lines("Can define the topic of this question: " + question + ", in one word or two?")[0]
        persona = topic + " specialist"
               
        # Créer le prompt pour l'IA et obtenir la réponse
        prompt = prompt_manager.create_prompt(persona, task, headlines, output_format)
        
        response_en = prompt_manager.get_response_lines(prompt)
        
        # Reconstitution d'une chaîne de  caractères en vue de la traduction
        chaine_en = "\n".join(response_en)

        # Retourner la réponse en français                                
        return prompt_manager.get_response_lines("Peux-tu traduire le texte suivant en français: " + chaine_en)
        
    def internet_search(self, query):
        params = {
            "engine": "google",
            "tbm": "nws",
            "num": 50,
            "q": query,
            "api_key": self.google_api_key
        }
        results = GoogleSearch(params).get_dict()
        
        # Ajout d'une barre de progression pour l'extraction des titres
        headlines = []
        for result in tqdm(results["news_results"], desc="Extraction des titres d'articles", unit="article"):
            headlines.append(result["title"])       
             
        return "\n".join(headlines)
