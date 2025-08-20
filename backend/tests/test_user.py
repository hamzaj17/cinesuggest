import pytest
from sqlalchemy.orm import Session
from app.db import Base, engine, SessionLocal
from app.models.user import User
from app.crud import user as crud_user
from app.schemas.user import UserCreate

# --- Setup a fresh test DB ---
@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)   # create tables
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)     # drop tables after tests


def test_create_user(db: Session):
    user_data = UserCreate(email="hamza@example.com", password="test123")
    new_user = crud_user.create_user(db, user_data)
    assert new_user.id is not None
    assert new_user.email == "hamza@example.com"

def test_get_user(db: Session):
    user = crud_user.get_user_by_email(db, "hamza@example.com")
    assert user is not None
    assert user.email == "hamza@example.com"

def test_update_user(db: Session):
    user = crud_user.get_user_by_email(db, "hamza@example.com")
    updated = crud_user.update_user(db, user.id, {"email": "hamza_updated@example.com"})
    assert updated.email == "hamza_updated@example.com"

def test_delete_user(db: Session):
    user = crud_user.get_user_by_email(db, "hamza_updated@example.com")
    crud_user.delete_user(db, user.id)
    deleted_user = crud_user.get_user_by_email(db, "hamza_updated@example.com")
    assert deleted_user is None
