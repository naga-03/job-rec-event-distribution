from pydantic import BaseModel
from typing import Dict
from datetime import datetime


class Notification(BaseModel):
    notification_id: str
    job_seeker_id: str
    message: str
    metadata: Dict
    read: bool
    created_at: datetime
