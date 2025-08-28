from fastapi import FastAPI
from app.routers import user, movie, rating, watchlist, user_preference   # <-- keep this one, remove app.api.v1.users if duplicate
from app.routers import auth   # <-- keep this one, remove app.api.v1.auth if duplicate
from app.core import deps


app = FastAPI(
    title="CineSuggest API (Phase 2 - Setup)",
    version="0.1.0",
    description="Backend foundation: routing + Pydantic models",
)

# Mount routers under a versioned API prefix
app.include_router(user.router)
app.include_router(movie.router)
app.include_router(auth.router)
app.include_router(rating.router)
app.include_router(watchlist.router)
app.include_router(user_preference.router)


# A quick root route (optional)
@app.get("/")
def read_root():
    return {"message": "CineSuggest backend is up. See /docs for Swagger UI."}
