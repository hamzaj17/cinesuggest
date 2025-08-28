# routers/user.py
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserRoleUpdate

from app.core.deps import get_current_user, require_admin  # <- import the shared dependency

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# --- Password hashing utility ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# --- Routes ---

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # hash password before saving
    hashed_pw = hash_password(user.password)

    new_user = User(
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Protected: only authenticated users can list users
@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    users = db.query(User).all()
    return users

@router.patch("/{user_id}/role", response_model=UserOut, dependencies=[Depends(require_admin)])
def update_user_role(
    user_id: int = Path(..., gt=0),
    payload: UserRoleUpdate = ...,
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.role not in {"user", "admin"}:
        raise HTTPException(status_code=422, detail="Invalid role")

    user.role = payload.role
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
