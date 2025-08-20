from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    ratings = relationship("Rating", back_populates="user", cascade="all, delete")
    preferences = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete")
    watchlist = relationship("Watchlist", back_populates="user", cascade="all, delete")
