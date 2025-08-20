from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db import Base

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    favorite_genres = Column(String)  # e.g., "Action, Comedy, Sci-Fi"
    min_rating = Column(Float)  # user only wants movies above this rating

    # relationships
    user = relationship("User", back_populates="preferences")