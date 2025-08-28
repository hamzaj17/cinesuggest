# app/routers/ratings.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import get_db
from app.models.rating import Rating
from app.models.movie import Movie
from app.schemas.rating import RatingCreate, RatingOut
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"]
)


@router.post("/", response_model=RatingOut)
def upsert_rating(payload: RatingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create or update the current user's rating for a movie (upsert).
    Body: { "movie_id": int, "rating": float }
    """
    # check movie exists
    movie = db.get(Movie, payload.movie_id)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    # find existing rating
    existing = db.query(Rating).filter(
        Rating.user_id == current_user.id,
        Rating.movie_id == payload.movie_id
    ).first()

    if existing:
        existing.rating = payload.rating
        # optionally update created_at or keep an updated_at column if you add it
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing

    new_rating = Rating(
        user_id=current_user.id,
        movie_id=payload.movie_id,
        rating=payload.rating
    )
    db.add(new_rating)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        # If UNIQUE constraint violation happens unexpectedly, return conflict
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not save rating")
    db.refresh(new_rating)
    return new_rating


@router.get("/me", response_model=list[RatingOut])
def my_ratings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Return all ratings created by the current user."""
    ratings = db.query(Rating).filter(Rating.user_id == current_user.id).all()
    return ratings


@router.delete("/movie/{movie_id}", status_code=status.HTTP_200_OK)
def delete_my_rating(movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete current user's rating for the movie."""
    rating = db.query(Rating).filter(Rating.user_id == current_user.id, Rating.movie_id == movie_id).first()
    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
    db.delete(rating)
    db.commit()
    return {"detail": "Rating deleted"}


@router.get("/movie/{movie_id}/stats")
def movie_rating_stats(movie_id: int, db: Session = Depends(get_db)):
    """
    Public: return average rating and count for a movie.
    Response example: { "movie_id": 12, "avg_rating": 4.3, "count": 42 }
    """
    movie = db.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    avg_val, cnt = db.query(func.avg(Rating.rating), func.count(Rating.id)).filter(Rating.movie_id == movie_id).one()
    avg_val = float(avg_val) if avg_val is not None else None
    return {"movie_id": movie_id, "avg_rating": avg_val, "count": cnt}
