from pydantic import BaseModel
from typing import List, Optional


class JobCard(BaseModel):
    user_id: str
    name: str
    headline: Optional[str]
    skills: List[str]
    location: Optional[str]
    experience_years: Optional[int]
    match_score: int
