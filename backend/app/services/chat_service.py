from typing import Dict, List
from app.core.event_bus import event_bus
from app.core.intent_parser import IntentParser
from app.core.matcher import Matcher
from app.core.groq_client import groq_client


class ChatService:
    """
    Orchestrates recruiter chat flow.
    Pure business logic layer.
    """

    def __init__(self):
        self.intent_parser = IntentParser()
        self.matcher = Matcher()

    async def process_message(self, message: str) -> Dict:
        """
        Main entry point for recruiter chat.
        """

        # 1️⃣ Parse intent (Async)
        intent = await self.intent_parser.parse(message)

        if intent["intent"] != "JOB_SEARCH":
            return self._no_intent_response()

        # 2️⃣ Match candidates (Async)
        matches = await self.matcher.match(
            keywords=intent.get("all_keywords", []),
            location=intent.get("location"),
            original_keywords=intent.get("keywords")
        )

        # ✅ 3️⃣ PUBLISH EVENT
        event_bus.publish(
            "JOB_SEARCH",
            {
                "matches": matches,
                "metadata": {
                    "keywords": intent.get("keywords"),
                    "location": intent.get("location")
                }
            }
        )

        # 🤖 4️⃣ GENERATE AI RECOMMENDATION (Async)
        recommendation_reason = await self._generate_ai_reason(message, matches)

        # 5️⃣ Build response
        return self._build_response(intent, matches, recommendation_reason)

    # -------------------------
    # Internal helpers
    # -------------------------

    def _build_response(self, intent: Dict, matches: List[Dict], reason: str = None) -> Dict:
        if not matches:
            return {
                "message": "No matching job seekers found.",
                "results": [],
                "metadata": {
                    "keywords": intent.get("keywords"),
                    "location": intent.get("location"),
                    "ai_reason": reason
                }
            }

        return {
            "message": f"Found {len(matches)} matching job seekers.",
            "results": matches,
            "metadata": {
                "keywords": intent.get("keywords"),
                "location": intent.get("location"),
                "ai_reason": reason
            }
        }

    async def _generate_ai_reason(self, message: str, matches: List[Dict]) -> str:
        if not matches:
            return "No candidates matched the specific criteria provided."

        system_prompt = """
        You are a recruitment consultant. Quickly summarize why the found candidates are a good match for the user's request.
        Request: {message}
        Keep it brief (1-2 sentences). Focus on top skills.
        """
        
        # Limit to top 3 matches for context
        top_matches = [f"{m['name']} ({', '.join(m['skills'])})" for m in matches[:3]]
        context = f"Found: {'; '.join(top_matches)}"
        
        return await groq_client.prompt(system_prompt.format(message=message), context)

    def _no_intent_response(self) -> Dict:
        return {
            "message": "I can help you find job seekers. Try something like 'Python developer in Bangalore'.",
            "results": [],
            "metadata": {}
        }
