from sqlalchemy.orm import Session
from app import models, schemas

def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(
        title=movie.title,
        genre=movie.genre,
        description=movie.description,
        release_year=movie.release_year
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def get_all_movies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Movie).offset(skip).limit(limit).all()

def delete_movie(db: Session, movie_id: int):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie:
        db.delete(movie)
        db.commit()
    return movie
