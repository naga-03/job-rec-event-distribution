import json
from typing import List, Dict
from app.config import USERS_FILE


class Matcher:
    """
    Schema-agnostic relevance matcher.
    Suitable for real DBs and unstructured profiles.
    """

    # 🔧 FIX: Lower threshold to allow single-keyword matches
    MIN_SCORE = 1

    def match(self, keywords: List[str], location: str | None) -> List[Dict]:
        seekers = self._load_job_seekers()
        matches = []

        for seeker in seekers:
            score = self._calculate_score(seeker, keywords, location)
            if score >= self.MIN_SCORE:
                matches.append(self._build_match_result(seeker, score))

        matches.sort(key=lambda x: x["match_score"], reverse=True)
        return matches

    def _load_job_seekers(self) -> List[Dict]:
        with open(USERS_FILE, "r") as f:
            return json.load(f)

    def _calculate_score(
        self,
        seeker: Dict,
        keywords: List[str],
        location: str | None
    ) -> int:
        score = 0
        searchable_text = self._build_search_text(seeker)

        # ✅ keyword-based scoring
        for keyword in keywords:
            if keyword.lower() in searchable_text:
                score += 1

        # ✅ optional location boost
        if location and location.lower() in searchable_text:
            score += 1

        return score

    def _build_search_text(self, seeker: Dict) -> str:
        """
        Flattens all profile data into one searchable string.
        Works regardless of schema.
        """
        parts = []

        for value in seeker.values():
            if isinstance(value, str):
                parts.append(value.lower())
            elif isinstance(value, list):
                parts.extend(str(v).lower() for v in value)
            elif isinstance(value, dict):
                parts.extend(str(v).lower() for v in value.values())

        return " ".join(parts)

    def _build_match_result(self, seeker: Dict, score: int) -> Dict:
        """
        Minimal, safe response object.
        Maps cleanly to job cards.
        """
        return {
            "user_id": seeker.get("user_id"),
            "name": seeker.get("name"),
            "headline": seeker.get("profession") or seeker.get("headline"),
            "skills": seeker.get("skills", []),
            "location": seeker.get("location"),
            "experience_years": seeker.get("experience_years"),
            "match_score": score
        }
