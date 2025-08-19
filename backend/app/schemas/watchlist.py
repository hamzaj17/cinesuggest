from pydantic import BaseModel

class WatchlistCreate(BaseModel):
    user_id: int
    movie_id: int

class WatchlistOut(BaseModel):
    id: int
    user_id: int
    movie_id: int

    class Config:
        orm_mode = True