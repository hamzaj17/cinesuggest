from pydantic import BaseModel, EmailStr
from typing import Optional

# Request body for creating a new user
class UserCreate(BaseModel):
    email: EmailStr
    password: str  # plain text for now (later we’ll hash it)

# Response body for returning user info (excluding password!)
class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        orm_mode = True  # allows returning SQLAlchemy objects directly
