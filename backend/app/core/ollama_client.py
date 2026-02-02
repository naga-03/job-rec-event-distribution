import httpx
import json
import asyncio
from typing import Dict, Any, List
from functools import lru_cache

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2.5-coder:latest"):
        self.base_url = base_url
        self.model = model
        self.timeout = httpx.Timeout(60.0, connect=10.0)
        # Embedding cache
        self._embedding_cache = {}

    async def get_embeddings(self, text: str) -> List[float]:
        """
        Generates a vector embedding. Uses cache to avoid redundant calls.
        """
        if text in self._embedding_cache:
            return self._embedding_cache[text]

        url = f"{self.base_url}/api/embeddings"
        payload = {"model": self.model, "prompt": text}
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                embedding = response.json().get("embedding", [])
                if embedding:
                    self._embedding_cache[text] = embedding
                return embedding
        except Exception as e:
            print(f"Ollama Embeddings Error: {e}")
            return []

    async def prompt(self, system_prompt: str, user_input: str) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\nUser: {user_input}\nAssistant:",
            "stream": False,
            "options": {"num_predict": 100} # Limit output length for speed
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return response.json().get("response", "")
        except Exception as e:
            print(f"Ollama Error: {e}")
            return ""

    async def structured_prompt(self, system_prompt: str, user_input: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\nUser: {user_input}\nAssistant:",
            "format": "json",
            "stream": False,
            "options": {"num_predict": 150} # Limit JSON size
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                content = response.json().get("response", "{}")
                return json.loads(content)
        except Exception as e:
            print(f"Ollama Structured Error: {e}")
            return {}

ollama_client = OllamaClient()
