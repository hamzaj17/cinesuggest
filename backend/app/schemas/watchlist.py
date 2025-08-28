# schemas/watchlist.py
from pydantic import BaseModel
from datetime import datetime

class WatchlistBase(BaseModel):
    movie_id: int

class WatchlistCreate(WatchlistBase):
    pass  # only movie_id needed from client

class WatchlistOut(WatchlistBase):
    id: int
    user_id: int
    added_at: datetime

    class Config:
        orm_mode = True
