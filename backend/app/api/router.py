from fastapi import APIRouter

from app.api.chat_routes import router as chat_router
from app.api.notification_routes import router as notification_router
from app.api.auth_routes import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(chat_router)
api_router.include_router(notification_router)
