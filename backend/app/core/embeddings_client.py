from fastembed import TextEmbedding
from typing import List

class EmbeddingsClient:
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        # This model is fast, small (~50MB), and runs on CPU easily
        print(f"Loading embeddings model: {model_name}...")
        self.model = TextEmbedding(model_name=model_name)
        print("Embeddings model loaded successfully.")

    async def get_embeddings(self, text: str) -> List[float]:
        """
        Generates a vector embedding using the local fastembed model.
        """
        try:
            # fastembed returns a generator, we need to convert to list
            embeddings = list(self.model.embed([text]))
            if embeddings:
                return embeddings[0].tolist()
            return []
        except Exception as e:
            print(f"Local Embeddings Error: {e}")
            return []

# Singleton instance
embeddings_client = EmbeddingsClient()
