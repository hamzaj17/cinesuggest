from pydantic import BaseModel

class UserPreferenceCreate(BaseModel):
    user_id: int
    genre: str

class UserPreferenceOut(BaseModel):
    id: int
    user_id: int
    genre: str

    class Config:
        orm_mode = True
