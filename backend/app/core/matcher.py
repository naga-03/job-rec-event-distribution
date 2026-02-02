import json
from typing import List, Dict
from app.config import USERS_FILE


from app.core.vector_store import vector_store


class Matcher:
    """
    Semantic Matcher using Vector Search.
    Finds candidates based on meaning and context.
    """

    async def match(self, keywords: List[str], location: str | None, original_keywords: List[str] = None) -> List[Dict]:
        """
        Hybrid search: Combines Vector Similarity with Keyword exact-matching.
        """
        orig_keys = original_keywords or keywords
        search_query = " ".join(orig_keys)
        
        # 1️⃣ Perform Semantic Search (Vector)
        semantic_results = await vector_store.search(search_query, top_k=5)
        semantic_dict = {r["user_id"]: r for r in semantic_results}

        # 2️⃣ Perform Lexical Search (Keyword Exact Match)
        candidates = vector_store.get_all_candidates()
        matches = []

        for seeker in candidates:
            # a) Calculate Keyword Score (Classic match)
            keyword_score = self._calculate_keyword_score(seeker, keywords, location)
            
            # b) Calculate Semantic Score (Vector match)
            semantic_entry = semantic_dict.get(seeker.get("user_id"))
            vector_score = semantic_entry["semantic_score"] if semantic_entry else 0
            
            # c) Combined Score (Weighted)
            # Keywords are highly reliable (50pts each), Vectors provide context (up to 40pts)
            total_score = (keyword_score * 50) + (vector_score * 40)
            
            print(f"HYBRID DEBUG: {seeker['name']} -> Key: {keyword_score}, Vec: {vector_score:.2f}, Total: {total_score:.1f}")

            if total_score > 0:
                matches.append(self._build_match_result(seeker, int(total_score)))
            
        # 3️⃣ Rank and deduplicate
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        return matches

    def _calculate_keyword_score(self, seeker: Dict, keywords: List[str], location: str | None) -> int:
        score = 0
        text = f"{seeker.get('profession', '')} {' '.join(seeker.get('skills', []))} {seeker.get('location', '')}".lower()
        
        for k in keywords:
            if k.lower() in text:
                score += 1
        
        if location and location.lower() in text:
            score += 1
            
        return score

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
