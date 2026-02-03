import os
import httpx
import json
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"
        self.timeout = httpx.Timeout(30.0)

    async def prompt(self, system_prompt: str, user_input: str) -> str:
        """
        Standard text generation using Groq.
        """
        if not self.api_key:
            return "GROQ_API_KEY not configured. AI reasoning disabled."

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.2,
            "max_tokens": 500
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.base_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Groq API Error: {e}")
            return f"Error communicating with AI intelligence: {e}"

    async def structured_prompt(self, system_prompt: str, user_input: str) -> Dict[str, Any]:
        """
        JSON-forced generation using Groq.
        """
        if not self.api_key:
            return {}

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.base_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                return json.loads(content)
        except Exception as e:
            print(f"Groq Structured API Error: {e}")
            return {}

groq_client = GroqClient()
