# routers/watchlist.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.watchlist import Watchlist
from app.schemas.watchlist import WatchlistCreate, WatchlistOut
from app.db import get_db
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/watchlist", tags=["watchlist"])

@router.post("/", response_model=WatchlistOut)
def add_to_watchlist(
    watchlist: WatchlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_entry = Watchlist(user_id=current_user.id, movie_id=watchlist.movie_id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.get("/", response_model=list[WatchlistOut])
def get_watchlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Watchlist).filter(Watchlist.user_id == current_user.id).all()

@router.delete("/{movie_id}")
def remove_from_watchlist(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entry = db.query(Watchlist).filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if entry:
        db.delete(entry)
        db.commit()
        return {"message": "Removed from watchlist"}
    return {"error": "Movie not in watchlist"}
