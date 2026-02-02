from pydantic import BaseModel
from typing import List, Optional


class JobSeeker(BaseModel):
    user_id: str
    name: str
    skills: List[str]
    location: Optional[str]
    experience_years: Optional[int]
    headline: Optional[str]
