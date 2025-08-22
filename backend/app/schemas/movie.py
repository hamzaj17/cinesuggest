from pydantic import BaseModel
from typing import Optional

class MovieCreate(BaseModel):
    title: str
    genre: Optional[str] = None
    description: Optional[str] = None
    release_year: Optional[int] = None
    imdb_rating: Optional[float] = None

class MovieOut(BaseModel):
    id: int
    title: str
    genre: Optional[str]
    description: Optional[str]
    release_year: Optional[int]
    imdb_rating: Optional[float]

    class Config:
        orm_mode = True
