from sqlalchemy.orm import Session
from app import models, schemas

def add_rating(db: Session, rating: schemas.RatingCreate):
    db_rating = models.Rating(
        user_id=rating.user_id,
        movie_id=rating.movie_id,
        rating=rating.rating
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_ratings_for_movie(db: Session, movie_id: int):
    return db.query(models.Rating).filter(models.Rating.movie_id == movie_id).all()

def get_ratings_by_user(db: Session, user_id: int):
    return db.query(models.Rating).filter(models.Rating.user_id == user_id).all()
