from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User  # SQLAlchemy User model
from app.schemas.user import UserCreate

# --- Password hashing context ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Generate a bcrypt hash for the password."""
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate):
    """Create a new user in the database."""
    hashed_pw = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    """Fetch a user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Fetch a user by email."""
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    """Fetch all users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()

def delete_user(db: Session, user_id: int):
    """Delete a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

def update_user(db: Session, user_id: int, update_data: dict):
    """Update user fields safely."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in update_data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
