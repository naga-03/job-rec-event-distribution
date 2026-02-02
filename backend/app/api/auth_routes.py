from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])
auth_service = AuthService()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(payload: LoginRequest):
    print(f"DEBUG: Login attempt for {payload.username}")
    token = auth_service.login(payload.username, payload.password)
    if not token:
        print(f"DEBUG: Login failed for {payload.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    print(f"DEBUG: Login successful for {payload.username}")
    return {"access_token": token}
