from typing import Dict, List
from app.core.event_bus import event_bus
from app.core.intent_parser import IntentParser
from app.core.matcher import Matcher


class ChatService:
    """
    Orchestrates recruiter chat flow.
    Pure business logic layer.
    """

    def __init__(self):
        self.intent_parser = IntentParser()
        self.matcher = Matcher()

    def process_message(self, message: str) -> Dict:
        """
        Main entry point for recruiter chat.
        """

        # 1️⃣ Parse intent
        intent = self.intent_parser.parse(message)

        if intent["intent"] != "JOB_SEARCH":
            return self._no_intent_response()

        # 2️⃣ Match candidates
        matches = self.matcher.match(
            keywords=intent.get("keywords", []),
            location=intent.get("location")
        )

        # ✅ 3️⃣ PUBLISH EVENT (THIS IS THE KEY)
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

        # 4️⃣ Build response
        return self._build_response(intent, matches)

    # -------------------------
    # Internal helpers
    # -------------------------

    def _build_response(self, intent: Dict, matches: List[Dict]) -> Dict:
        if not matches:
            return {
                "message": "No matching job seekers found.",
                "results": [],
                "metadata": {
                    "keywords": intent.get("keywords"),
                    "location": intent.get("location")
                }
            }

        return {
            "message": f"Found {len(matches)} matching job seekers.",
            "results": matches,
            "metadata": {
                "keywords": intent.get("keywords"),
                "location": intent.get("location")
            }
        }

    def _no_intent_response(self) -> Dict:
        return {
            "message": "I can help you find job seekers. Try something like 'Python developer in Bangalore'.",
            "results": [],
            "metadata": {}
        }
