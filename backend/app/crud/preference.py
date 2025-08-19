from sqlalchemy.orm import Session
from app import models, schemas

def set_user_preference(db: Session, preference: schemas.UserPreferenceCreate):
    db_pref = models.UserPreference(
        user_id=preference.user_id,
        preferred_genres=preference.preferred_genres
    )
    db.add(db_pref)
    db.commit()
    db.refresh(db_pref)
    return db_pref

def get_user_preference(db: Session, user_id: int):
    return db.query(models.UserPreference).filter(models.UserPreference.user_id == user_id).first()
