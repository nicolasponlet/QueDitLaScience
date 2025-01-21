import os
from dotenv import load_dotenv
import streamlit as st
from classes.QueDitLaScienceApp import QueDitLaScienceApp

# Page principale
def main_page():
    st.title("Outil comparatif de ce qui est dit dans les publications scientifiques et sur Internet")
    question = st.text_input("Posez votre question :", placeholder="Entrez une question...")
    if st.button("Soumettre"):
        st.session_state['question'] = question
        st.rerun()  # Naviguer vers la page de résultats
 
# Page des résultats
def results_page():
    question = st.session_state.get('question', None)
    if not question:
        st.error("Veuillez poser une question sur la page principale.")
        st.stop()
 
    st.title("Résultats pour votre question")
    st.write(f"**Question posée :** {question}")
 
    # Exécuter l'application avec les paramètres fournis
    scientific_results, web_results, similarity_scores = app.run(
        task="Describe precisely in 3 points",
        question=question,
        output_format="in 3 sentences of 250 characters maximum"
    )

    # Colonnes pour afficher les résultats
    col1, col2 = st.columns(2)
 
    # Recherche scientifique
    with col1:
        st.header("Synthèse Scientifique")
        # st.write("Recherche en cours...")
        # st.write(scientific_results)
        st.write(line + "\n" for line in scientific_results)
 
     # Recherche sur Internet
    with col2:
        st.header("Synthèse Internet")
        # st.write("Recherche en cours...")
        # st.write(web_results)
        st.write(line + "\n" for line in web_results)
 
   # Calcul de la similarité
    st.header("Indicateur de Similitude")
 
    # Afficher la similarité
    st.metric(label="Score de Similarité", value=f"{similarity_scores*100:.2f}")
    
    # Transformer le score pour qu'il soit entre 0 et 1
    progress_value = (similarity_scores + 1) / 2
    
    # Ajouter une légende descriptive
    if similarity_scores < -0.5:
        description = "Opposé"
    elif -0.5 <= similarity_scores < 0.5:
        description = "Neutre"
    else:
        description = "Similaire"
    
    # Afficher la barre de progression
    st.text(f"Score : {similarity_scores:.2f} ({description})")
    st.progress(progress_value)
 
 
if __name__ == "__main__":
    # Initialiser l'application avec les clés API
    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    google_api_key = os.getenv("GoogleSearch_API_KEY")

    # Créer une instance de l'application
    app = QueDitLaScienceApp(openai_api_key=openai_api_key, google_api_key=google_api_key)

    # # Initialisation de Streamlit
    # st.set_page_config(page_title="Que dit la science ? ", layout="wide")
    
    # # Navigation entre les pages
    # if 'question' not in st.session_state:
    #     main_page()
    # else:
    #     results_page()
        
    scientific_results, web_results, similarity_scores = app.run(
        task="Describe precisely in 3 points",
        question="Quelles sont les causes du changement climatique ?",
        output_format="in 3 sentences of 250 characters maximum"
    )
    
    print("Fini! ")      