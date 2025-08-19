from fastapi import FastAPI
from app.api.v1.health import router as health_router
from app.api.v1.users import router as users_router

app = FastAPI(
    title="CineSuggest API (Phase 2 - Setup)",
    version="0.1.0",
    description="Backend foundation: routing + Pydantic models",
)

# Mount routers under a versioned API prefix
app.include_router(health_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")

# A quick root route (optional)
@app.get("/")
def read_root():
    return {"message": "CineSuggest backend is up. See /docs for Swagger UI."}
