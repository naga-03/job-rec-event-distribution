from app.core.event_bus import event_bus
from app.services.notification_service import notification_service
from app.repositories.notification_repository import NotificationRepository


def test_notification_created_on_job_search_event(tmp_path, monkeypatch):
    """
    Verify notification is created when JOB_SEARCH event is published.
    """

    # Redirect notifications file to temp file
    temp_file = tmp_path / "notifications.json"
    monkeypatch.setattr(
        "app.config.NOTIFICATIONS_FILE",
        str(temp_file)
    )

    repo = NotificationRepository()

    # Publish fake event
    event_bus.publish(
        "JOB_SEARCH",
        {
            "matches": [
                {"user_id": "J001"},
                {"user_id": "J002"}
            ],
            "metadata": {
                "keywords": ["python"],
                "location": "Chennai"
            }
        }
    )

    notifications_j1 = repo.get_for_user("J001")
    notifications_j2 = repo.get_for_user("J002")

    assert len(notifications_j1) == 1
    assert len(notifications_j2) == 1

    assert notifications_j1[0]["read"] is False
    assert "metadata" in notifications_j1[0]
