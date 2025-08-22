# routers/movies.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieOut

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)

# --- POST: Add a new movie ---
@router.post("/", response_model=MovieOut)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    # Check if movie already exists
    db_movie = db.query(Movie).filter(Movie.title == movie.title).first()
    if db_movie:
        raise HTTPException(status_code=400, detail="Movie already exists")

    new_movie = Movie(
        title=movie.title,
        genre=movie.genre,
        description=movie.description,
        release_year=movie.release_year,
        imdb_rating=movie.imdb_rating
    )
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie


# --- GET: Fetch all movies ---
@router.get("/", response_model=list[MovieOut])
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    return movies


# --- GET: Fetch a movie by ID ---
@router.get("/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
