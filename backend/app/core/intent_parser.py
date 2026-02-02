import re
from typing import Dict, List, Optional
from app.core.ollama_client import ollama_client


class IntentParser:
    """
    NLP-powered intent parser using Ollama.
    Designed to be dynamic and database-ready.
    """

    SYSTEM_PROMPT = """
    You are a professional recruitment AI. Extract search parameters from a recruiter's request.
    
    1. "keywords": Technical skills or roles mentioned explicitly (e.g., ["Python"]).
    2. "location": City/region mentioned, or null.
    3. "expanded_keywords": Suggest ONLY 2-3 HIGHSLY RELATED skills (e.g. for Python, suggest ["Django", "FastAPI"]). 
       CRITICAL: DO NOT suggest unrelated languages (e.g. don't suggest Java for Python). 
       DO NOT suggest broad terms like "Algorithms" or "SQL" unless relevant.
    
    Return ONLY a valid JSON object.
    """

    async def parse(self, text: str) -> Dict:
        """
        Parses recruiter input text into structured intent with semantic expansion.
        Prioritizes LLM entity extraction.
        """
        # 1️⃣ Try Ollama Analysis
        result = await ollama_client.structured_prompt(self.SYSTEM_PROMPT, text)
        
        if result and "keywords" in result:
            original = result["keywords"]
            expanded = result.get("expanded_keywords", [])
            all_terms = list(set(original + expanded))
            
            print(f"Ollama Extraction: {original} -> Expanded: {expanded}")
            
            return {
                "intent": "JOB_SEARCH",
                "keywords": original,        # UI should show these
                "expanded_keywords": expanded, # Underlying search uses these
                "all_keywords": all_terms,     # Total search scope
                "location": result.get("location")
            }

        # 2️⃣ Fallback Logic (Generic Keyword Extraction)
        print("LLM failed or returned no keywords, using generic fallback")
        tokens = re.findall(r"[a-zA-Z]+", text)
        
        # Simple heuristic: remove very short words and common English particles
        generic_stop_words = {"the", "and", "for", "with", "hiring", "need", "want", "looking"}
        keywords = [
            t for t in tokens 
            if len(t) > 2 and t.lower() not in generic_stop_words
        ]

        return {
            "intent": "JOB_SEARCH",
            "keywords": list(set(keywords)),
            "location": None # Fallback cannot reliably guess location without a master list
        }
