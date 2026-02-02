from datetime import datetime, timedelta
from jose import jwt
from app.config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.repositories.auth_repository import AuthRepository

class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def login(self, username: str, password: str):
        user = self.repo.get_user_by_username(username)

        if not user or user["password"] != password:
            return None

        payload = {
            "sub": user["user_id"],
            "user_type": user["user_type"],
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }

        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
