from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.repositories.notification_repository import NotificationRepository

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"]
)

repo = NotificationRepository()


@router.get("")
def get_notifications(user: dict = Depends(get_current_user)):
    """
    Get notifications for the authenticated user.
    JWT payload MUST contain: user_id
    """

    user_id = user.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: user_id missing"
        )

    try:
        notifications = repo.get_notifications_for_user(user_id)

        return {
            "success": True,
            "count": len(notifications),
            "data": notifications
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch notifications: {str(e)}"
        )
