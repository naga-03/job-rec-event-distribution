from app.core.intent_parser import IntentParser
from app.core.matcher import Matcher


def test_intent_parser_extracts_keywords_and_location():
    parser = IntentParser()

    query = "Need a Python backend developer in Chennai"
    intent = parser.parse(query)

    assert intent["intent"] == "JOB_SEARCH"
    assert "python" in intent["keywords"]
    assert intent["location"] == "Chennai"


def test_matcher_returns_ranked_results():
    parser = IntentParser()
    matcher = Matcher()

    query = "Python developer in Bangalore"
    intent = parser.parse(query)

    results = matcher.match(intent["keywords"], intent["location"])

    assert isinstance(results, list)

    if results:
        assert "match_score" in results[0]
        assert results[0]["match_score"] >= results[-1]["match_score"]
