from app.repositories.notification_repository import NotificationRepository
from app.core.event_bus import event_bus


class NotificationService:
    """
    Consumes JOB_SEARCH events and notifies job seekers.
    """

    EVENT_TYPE = "JOB_SEARCH"

    def __init__(self):
        self.repo = NotificationRepository()
        event_bus.subscribe(self.EVENT_TYPE, self.handle_job_search)

    def handle_job_search(self, payload: dict):
        matches = payload.get("matches", [])
        metadata = payload.get("metadata", {})

        for match in matches:
            self.repo.create_notification(
                job_seeker_id=match["user_id"],
                message="New job opportunity matching your profile",
                metadata=metadata
            )


# instantiate once
notification_service = NotificationService()
