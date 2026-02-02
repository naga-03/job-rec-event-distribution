import json
from app.config import AUTH_USERS_FILE

class AuthRepository:
    def get_user_by_username(self, username: str):
        with open(AUTH_USERS_FILE, "r") as f:
            users = json.load(f)
        return next((u for u in users if u["username"] == username), None)
