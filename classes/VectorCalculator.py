from openai import OpenAI
import scipy.spatial.distance as dist


class VectorCalculator:
    """Gestion des embeddings et des calculs de distance."""
    
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.embedding_model = "text-embedding-3-small"
    
    def find_distance_from_text(self, pDataset, pReferenceText ):
        df_temp = pDataset.copy()
        reference_vector = self.get_vector( pReferenceText )
        df_temp["distance"] = df_temp.apply( lambda row : self.get_distance( reference_vector, row["vector"] ), axis=1 )

        # Tri des lignes. Les lignes les plus proches seront "en haut" du dataframe
        df_temp.sort_values( "distance", ascending=True, inplace=True )
        df_temp.reset_index( inplace=True)
        
        return df_temp
    
    def get_vector(self, text, size=1024):
        """Calcul de l'embedding pour un texte donné."""
        if text == "":
            vector = [0,0,0]
        else:
            vector = self.client.embeddings.create(
                input=text,
                model=self.embedding_model,
                dimensions=size
            ).data[0].embedding
        return vector

    def get_distance(self, vector1, vector2, method):
        """Calcul de la distance entre deux vecteurs."""
        if method == "cosine":
            return dist.cosine(vector1, vector2)
        elif method == "euclidean":
            return dist.euclidean(vector1, vector2)
        else:
            raise ValueError("Méthode inconnue : choisissez 'cosine' ou 'euclidean'.")

