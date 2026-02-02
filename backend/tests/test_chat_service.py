from app.services.chat_service import ChatService


def test_chat_service_returns_results_structure():
    service = ChatService()

    response = service.process_message(
        "Need a Python backend developer in Chennai"
    )

    assert "message" in response
    assert "results" in response
    assert "metadata" in response

