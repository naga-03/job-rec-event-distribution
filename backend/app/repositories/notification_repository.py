import json
import uuid
from pathlib import Path
from datetime import datetime

NOTIFICATIONS_FILE = Path(__file__).parent.parent / "data" / "notifications.json"


class NotificationRepository:
    def __init__(self):
        if not NOTIFICATIONS_FILE.exists():
            NOTIFICATIONS_FILE.write_text("[]")

    def _load(self):
        return json.loads(NOTIFICATIONS_FILE.read_text())

    def _save(self, data):
        NOTIFICATIONS_FILE.write_text(json.dumps(data, indent=2))

    def create_notification(self, job_seeker_id: str, message: str, metadata: dict | None = None):
        notifications = self._load()

        notifications.append({
            "notification_id": str(uuid.uuid4()),
            "job_seeker_id": job_seeker_id,
            "message": message,
            "metadata": metadata or {},
            "read": False,
            "created_at": datetime.utcnow().isoformat()
        })

        self._save(notifications)

    def get_notifications_for_user(self, job_seeker_id: str):
        notifications = self._load()
        return [
            n for n in notifications
            if n.get("job_seeker_id") == job_seeker_id
        ]
