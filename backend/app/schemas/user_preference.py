from pydantic import BaseModel
from typing import Optional

class UserPreferenceBase(BaseModel):
    favorite_genres: str   # e.g. "Action, Comedy"
    min_rating: Optional[float] = None

class UserPreferenceCreate(UserPreferenceBase):
    pass

class UserPreferenceOut(UserPreferenceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
