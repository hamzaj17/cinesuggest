from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime , UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Float, nullable=False)  # 1-5 or 1-10 scale
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relationships
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")

    
    __table_args__ = (
        UniqueConstraint("user_id", "movie_id", name="uix_user_movie"),
        Index("ix_ratings_movie_id", "movie_id"),
    )