# app/core/deps.py
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from app.core.security import decode_token

# Make sure tokenUrl matches your login route (here it's "/login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
router = APIRouter(tags=["Auth"])

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Dependency that:
    - extracts token from Authorization header (Bearer ...)
    - decodes it and gets the 'sub' (user id)
    - loads the user from DB and returns the SQLAlchemy User object
    Raises 401 / 404 appropriately.
    """
    try:
        payload = decode_token(token)  # raises JWTError if invalid/expired
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        user_id = int(sub)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    user = db.get(User, user_id)  # SQLAlchemy Session.get (1.4+)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

