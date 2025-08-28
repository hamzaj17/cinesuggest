from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user_preference import UserPreference
from app.schemas.user_preference import UserPreferenceCreate, UserPreferenceOut
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/preference", tags=["User Preferences"])

@router.post("/", response_model=UserPreferenceOut)
def create_or_update_preference(
    preference_in: UserPreferenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # check if preference already exists
    preference = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()

    if preference:
        # update
        preference.favorite_genres = preference_in.favorite_genres
        preference.min_rating = preference_in.min_rating
    else:
        # create
        preference = UserPreference(
            user_id=current_user.id,
            favorite_genres=preference_in.favorite_genres,
            min_rating=preference_in.min_rating
        )
        db.add(preference)

    db.commit()
    db.refresh(preference)
    return preference

# Get Current User Preference
@router.get("/", response_model=UserPreferenceOut)
def get_my_preference(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    preference = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()

    if not preference:
        raise HTTPException(status_code=404, detail="Preferences not found")

    return preference