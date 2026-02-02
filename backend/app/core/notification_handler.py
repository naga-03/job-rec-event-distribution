from app.repositories.notification_repository import NotificationRepository

notification_repo = NotificationRepository()


def handle_job_search_event(payload: dict):
    # ✅ FIX: use "matches" (NOT "candidates")
    matches = payload.get("matches", [])
    keywords = payload.get("metadata", {}).get("keywords", [])

    for match in matches:
        job_seeker_id = match.get("user_id")

        if not job_seeker_id:
            continue

        notification_repo.create_notification(
            job_seeker_id=job_seeker_id,
            message=f"You were matched for a role requiring {', '.join(keywords)}",
            metadata={"keywords": keywords}
        )
