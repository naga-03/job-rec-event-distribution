from pydantic import BaseModel

class AuthUser(BaseModel):
    user_id: str
    username: str
    password: str
    user_type: str  # recruiter | job_seeker
