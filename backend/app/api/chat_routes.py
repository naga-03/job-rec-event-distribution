from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services.chat_service import ChatService
from app.core.security import require_recruiter

router = APIRouter(prefix="/api/chat", tags=["chat"])


# -------------------------
# Request / Response Models
# -------------------------

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    message: str
    results: list
    metadata: dict


# -------------------------
# Route
# -------------------------

@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    user=Depends(require_recruiter)
):
    """
    Recruiter-only chat endpoint.
    """
    service = ChatService()
    return await service.process_message(payload.message)
