from fastapi import FastAPI
import pickle
import joblib
import pandas as pd
from pathlib import Path

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

@app.get("/recommend/{user_id}")
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