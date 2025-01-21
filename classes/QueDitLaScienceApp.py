from classes.ArticleProcessor import ArticleProcessor
from classes.WebSearchProcessor import WebSearchProcessor
from classes.VectorCalculator import VectorCalculator
from classes.PromptManager import PromptManager


class QueDitLaScienceApp:
    def __init__(self, openai_api_key, google_api_key):
        # Initialiser l'API OpenAI et l'API Google Search
        self.article_processor = ArticleProcessor(openai_api_key)
        self.web_search_processor = WebSearchProcessor(openai_api_key, google_api_key)
        self.vector_calculator = VectorCalculator(openai_api_key)
        self.prompt_manager = PromptManager(openai_api_key)

    def run(self, task, question, output_format):
        """
        Fonction principale qui exécute l'application.
        :param task: la tâche que l'IA doit accomplir
        :param question: la question à traiter
        :param output_format: format de la réponse attendue
        """
        
        question_en = self.prompt_manager.get_response_lines("Si le texte suivant n'est pas en anglais, peux-tu traduire la phrase suivante en anglais : " + question)[0]
               
        # Extraction des publications scientifiques
        scientific_results = self.article_processor.process_articles(
            task, question_en, output_format)
        
        # Recherche sur Internet
        web_results = self.web_search_processor.process_web_search(
            task, question_en, output_format
        )

        # Comparaison des résultats
        similarity_scores = (1-self.compare_results(scientific_results, web_results))
       
        return scientific_results, web_results, similarity_scores
        

    def compare_results(self, scientific_results, web_results):
        """
        Compare les résultats scientifiques et les résultats Web pour déterminer leur similarité.
        :param scientific_df: DataFrame des résultats scientifiques
        :param web_df: DataFrame des résultats Web
        :return: DataFrame des similarités entre les résultats scientifiques et Web
        """
       
        articles_vectors = self.vector_calculator.get_vector(scientific_results)
        web_vectors = self.vector_calculator.get_vector(web_results)
        
        return self.vector_calculator.get_distance(articles_vectors, web_vectors, method="cosine")

