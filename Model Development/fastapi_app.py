from fastapi import FastAPI, Query
import pickle
import joblib
import pandas as pd
from pathlib import Path
from typing import List
from src.model_cb import recommend as cb_recommend
from src.hybrid import hybrid_recommend

MODEL_DIR = Path(__file__).resolve().parents[0] / "models"
DATA_DIR = Path(__file__).resolve().parents[0] / "data"

# Load trained SVD model
with open(MODEL_DIR / "cf_svd_model.pkl", "rb") as f:
    model = pickle.load(f)

# Load movieId -> title mapping
movie_map = joblib.load(MODEL_DIR / "movieid_to_title.joblib")

# Load ratings data to know what each user has rated
ratings = pd.read_csv(DATA_DIR / "ratings_cleaned.csv")

app = FastAPI()

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.get("/recommend/cf/{user_id}")
def recommend(user_id: int, n: int = 5):
    # Movies user has already rated
    seen_movies = ratings.loc[ratings["userId"] == user_id, "movieId"].tolist()
    
    # All movie IDs in dataset
    all_movies = list(movie_map.keys())
    
    # Predict rating for each unseen movie
    predictions = []
    for movie_id in all_movies:
        if movie_id not in seen_movies:
            pred = model.predict(user_id, movie_id)
            predictions.append((movie_id, pred.est))
    
    # Sort by predicted rating (highest first)
    predictions.sort(key=lambda x: x[1], reverse=True)
    
    # Take top-N recommendations
    top_n = predictions[:n]
    
    # Map to titles
    recommendations = [{"movieId": mid, "title": movie_map[mid]} for mid, _ in top_n]
    
    return {
        "user_id": user_id,
        "recommendations": recommendations
    }


@app.get("/recommend/cb/{movie_title}")
def recommend_content(movie_title: str, n: int = 5):
    recs = cb_recommend(movie_title, num_recommendations=n)
    return {
        "movie_title": movie_title,
        "recommendations": recs
    }


@app.get("/recommend/hybrid/{title}")
def recommend_hybrid(
    title: str,
    top_n: int = Query(5, ge=1, le=20),
    weight_cb: float = Query(0.5, ge=0.0, le=1.0),
    weight_cf: float = Query(0.5, ge=0.0, le=1.0)
):
    """
    Hybrid Recommendation Endpoint
    """
    try:
        recommendations = hybrid_recommend(title, top_n=top_n, weight_cb=weight_cb, weight_cf=weight_cf)
        return {
            "movie_title": title,
            "recommendations": recommendations
        }
    except Exception as e:
        return {"error": str(e)}
