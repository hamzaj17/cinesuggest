from pydantic import BaseModel

class RatingCreate(BaseModel):
    movie_id: int
    user_id: int
    score: int  # 1–5 range

class RatingOut(BaseModel):
    id: int
    movie_id: int
    user_id: int
    score: int

    class Config:
        orm_mode = True
