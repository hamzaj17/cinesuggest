from pydantic import BaseModel, EmailStr
from datetime import datetime

# --- Base Schema ---
class UserBase(BaseModel):
    email: EmailStr

# --- Create Schema (request body when registering user) ---
class UserCreate(UserBase):
    password: str

# --- Response Schema (returned in API responses) ---
class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # allows SQLAlchemy model -> Pydantic schema
