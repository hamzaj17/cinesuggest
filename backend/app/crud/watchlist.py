from sqlalchemy.orm import Session
from app import models, schemas

def add_to_watchlist(db: Session, watchlist_item: schemas.WatchlistCreate):
    db_item = models.Watchlist(
        user_id=watchlist_item.user_id,
        movie_id=watchlist_item.movie_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_watchlist(db: Session, user_id: int):
    return db.query(models.Watchlist).filter(models.Watchlist.user_id == user_id).all()

def remove_from_watchlist(db: Session, user_id: int, movie_id: int):
    item = db.query(models.Watchlist).filter(
        models.Watchlist.user_id == user_id,
        models.Watchlist.movie_id == movie_id
    ).first()
    if item:
        db.delete(item)
        db.commit()
    return item
