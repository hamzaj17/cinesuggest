from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # store only hashed passwords
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    ratings = relationship("Rating", back_populates="user", cascade="all, delete")
    preferences = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete")
    watchlist = relationship("Watchlist", back_populates="user", cascade="all, delete")


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    genre = Column(String, index=True)
    description = Column(Text)
    release_year = Column(Integer)
    imdb_rating = Column(Float)

    # relationships
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete")
    watchlisted_by = relationship("Watchlist", back_populates="movie", cascade="all, delete")


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"))
    rating = Column(Float, nullable=False)  # 1-5 or 1-10 scale
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    favorite_genres = Column(String)  # e.g., "Action, Comedy, Sci-Fi"
    favorite_language = Column(String)
    min_rating = Column(Float)  # user only wants movies above this rating

    # relationships
    user = relationship("User", back_populates="preferences")


class Watchlist(Base):
    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"))
    added_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    user = relationship("User", back_populates="watchlist")
    movie = relationship("Movie", back_populates="watchlisted_by")
