from fastapi import FastAPI
from app.routers import user, movie   # <-- keep this one, remove app.api.v1.users if duplicate

app = FastAPI(
    title="CineSuggest API (Phase 2 - Setup)",
    version="0.1.0",
    description="Backend foundation: routing + Pydantic models",
)

# Mount routers under a versioned API prefix
app.include_router(user.router)
app.include_router(movie.router)

# A quick root route (optional)
@app.get("/")
def read_root():
    return {"message": "CineSuggest backend is up. See /docs for Swagger UI."}
