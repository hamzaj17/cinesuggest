from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from app.db import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    genre = Column(String, index=True)
    description = Column(Text)
    release_year = Column(Integer)
    imdb_rating = Column(Float)

    ratings = relationship("Rating", back_populates="movie", cascade="all, delete")
    watchlisted_by = relationship("Watchlist", back_populates="movie", cascade="all, delete")
