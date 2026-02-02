from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.options("/login")
def options_login():
    return {"message": "OK"}

@router.post("/login")
def login(payload: LoginRequest):
    token = auth_service.login(payload.username, payload.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token}
