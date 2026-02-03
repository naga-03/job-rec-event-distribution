from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

class EmbeddingsClient:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # This model is fast, small (~80MB), and runs on CPU easily
        print(f"Loading embeddings model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("Embeddings model loaded successfully.")

    async def get_embeddings(self, text: str) -> List[float]:
        """
        Generates a vector embedding using the local SentenceTransformer model.
        """
        try:
            # We run this in the main thread for simplicity as the model is small,
            # but in a high-traffic app we'd use run_in_executor.
            embedding = self.model.encode(text)
            return embedding.tolist()
        except Exception as e:
            print(f"Local Embeddings Error: {e}")
            return []

# Singleton instance
embeddings_client = EmbeddingsClient()
