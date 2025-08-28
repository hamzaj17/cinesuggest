from pydantic import BaseModel, confloat
from typing import Optional
from datetime import datetime

# rating validated to 0.5 - 10.0 (you can adjust range)
RatingValue = confloat(ge=0.5, le=10.0)  
class RatingCreate(BaseModel):
    movie_id: int
    rating: RatingValue 

class RatingOut(BaseModel):
    id: int
    movie_id: int
    user_id: int
    rating: float
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
