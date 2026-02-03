import numpy as np
from typing import List, Dict, Any
from app.core.embeddings_client import embeddings_client

class VectorStore:
    def __init__(self):
        self.embeddings = []
        self.metadata = []
        self.embeddings_np = None

    async def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Processes a list of documents (users) and stores their embeddings.
        """
        print(f"Indexing {len(documents)} candidates for semantic search...")
        self.embeddings = []
        self.metadata = []
        
        for doc in documents:
            text = self._prepare_text(doc)
            embedding = await embeddings_client.get_embeddings(text)
            if embedding:
                self.embeddings.append(embedding)
                self.metadata.append(doc)
            else:
                print(f"Warning: Could not get embedding for {doc.get('name')}")
        
        if self.embeddings:
            self.embeddings_np = np.array(self.embeddings)
            print("Indexing complete.")

    MIN_SIMILARITY = 0.3

    def get_all_candidates(self) -> List[Dict[str, Any]]:
        return self.metadata

    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Performs semantic search using cosine similarity.
        """
        if self.embeddings_np is None or len(self.embeddings_np) == 0:
            print("VectorStore: No documents indexed.")
            return []

        query_vec = await embeddings_client.get_embeddings(query)
        if not query_vec:
            return []

        query_vec = np.array(query_vec)
        
        # Cosine similarity calculation: dot(A, B) / (norm(A) * norm(B))
        norm_q = np.linalg.norm(query_vec)
        norm_docs = np.linalg.norm(self.embeddings_np, axis=1)
        
        # Avoid division by zero
        norm_docs[norm_docs == 0] = 1e-10
        if norm_q == 0: norm_q = 1e-10

        similarities = np.dot(self.embeddings_np, query_vec) / (norm_docs * norm_q)
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            print(f"DEBUG: Similarity for {self.metadata[idx].get('name')}: {score:.4f}")
            
            if score >= self.MIN_SIMILARITY:
                res = self.metadata[idx].copy()
                res["semantic_score"] = score
                results.append(res)
            
        return results

    def _prepare_text(self, doc: Dict[str, Any]) -> str:
        """
        Converts a user object into a rich searchable string for embedding.
        """
        skills = ", ".join(doc.get("skills", []))
        profession = doc.get("profession") or doc.get("headline") or ""
        location = doc.get("location", "")
        return f"Profession: {profession}. Skills: {skills}. Location: {location}."

vector_store = VectorStore()
