from fastapi import APIRouter
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users"])

# Temporary in-memory "storage" just to show request/response flow.
_FAKE_USERS: list[UserOut] = []

@router.post("/signup", response_model=UserOut, status_code=201)
def signup(payload: UserCreate):
    """
    Beginner-friendly demo endpoint:
    - Accepts a UserCreate body (validated by Pydantic)
    - Returns a UserOut (no DB yet; that comes later)
    """
    new_user = UserOut(
        id=len(_FAKE_USERS) + 1,
        email=payload.email,
        role="user",
    )
    _FAKE_USERS.append(new_user)
    return new_user
