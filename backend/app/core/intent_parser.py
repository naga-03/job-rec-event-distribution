import re
from typing import Dict, List, Optional


class IntentParser:
    """
    Stateless, keyword-based intent parser.
    Designed to work with real-world free text.
    """

    LOCATION_KEYWORDS = [
        "bangalore", "bengaluru", "chennai", "hyderabad",
        "mumbai", "pune", "delhi", "noida", "gurgaon"
    ]

    STOP_WORDS = {
        "looking", "need", "want", "hire", "hiring", "for",
        "a", "an", "the", "with", "in", "of", "to", "developer",
        "engineer"
    }

    def parse(self, text: str) -> Dict:
        """
        Parses recruiter input text into structured intent.
        """
        text = text.lower()

        location = self._extract_location(text)
        keywords = self._extract_keywords(text)

        return {
            "intent": "JOB_SEARCH",
            "keywords": keywords,
            "location": location
        }

    def _extract_location(self, text: str) -> Optional[str]:
        for location in self.LOCATION_KEYWORDS:
            if re.search(rf"\b{location}\b", text):
                return location.title()
        return None

    def _extract_keywords(self, text: str) -> List[str]:
        tokens = re.findall(r"[a-zA-Z]+", text)

        keywords = [
            token for token in tokens
            if token not in self.STOP_WORDS and len(token) > 2
        ]

        return list(set(keywords))  # remove duplicates
