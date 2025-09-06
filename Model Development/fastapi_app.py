from fastapi import FastAPI, Query
import pickle
import joblib
import pandas as pd
from pathlib import Path
from src.hybrid import hybrid_recommend   # hybrid still uses CB + CF
from src.recommend_cb import recommend   # CB recommendation function

MODEL_DIR = Path(__file__).resolve().parents[0] / "models"
DATA_DIR = Path(__file__).resolve().parents[0] / "data"

# Load trained CF model (SVD)
with open(MODEL_DIR / "cf_svd_model.pkl", "rb") as f:
    model_cf = pickle.load(f)

# Load trained CB model (your single pickle file)
with open(MODEL_DIR / "cb_model.pkl", "rb") as f:
    model_cb = pickle.load(f)

# Load movieId -> title mapping
movie_map = joblib.load(MODEL_DIR / "movieid_to_title.joblib")

# Load ratings data (needed for CF user filtering)
from pathlib import Path
import pandas as pd

data_dir = Path(r"D:\cinesuggest\Model Development\data")
ratings = pd.read_parquet(data_dir / "ratings_cleaned.parquet")
app = FastAPI()

@app.get("/ping")
async def ping():
    return {"message": "pong"}

# ---------------- CF Endpoint ----------------
@app.get("/recommend/cf/{user_id}")
def recommend_cf(user_id: int, n: int = 5):
    """
    Collaborative Filtering Recommendations
    """
    seen_movies = ratings.loc[ratings["userId"] == user_id, "movieId"].tolist()
    all_movies = list(movie_map.keys())

    predictions = []
    for movie_id in all_movies:
        if movie_id not in seen_movies:
            pred = model_cf.predict(user_id, movie_id)
            predictions.append((movie_id, pred.est))

    predictions.sort(key=lambda x: x[1], reverse=True)
    top_n = predictions[:n]

    recommendations = [{"movieId": mid, "title": movie_map[mid]} for mid, _ in top_n]
    return {"user_id": user_id, "recommendations": recommendations}

# ---------------- CB Endpoint ----------------
@app.get("/recommend/cb/{movie_title}")
def recommend_cb(movie_title: str, n: int = 5):
    """
    Content-Based Recommendations (using saved cb_model.pkl)
    """
    try:
        recs = recommend(movie_title, num_recommendations=n)
        if not recs:
            return {"error": f"Movie '{movie_title}' not found in dataset."}
        return {
            "movie_title": movie_title,
            "recommendations": recs
        }
    except Exception as e:
        return {"error": str(e)} 

# ---------------- Hybrid Endpoint ----------------
@app.get("/recommend/hybrid/{title}")
def recommend_hybrid(
    title: str,
    top_n: int = Query(5, ge=1, le=20),
    weight_cb: float = Query(0.5, ge=0.0, le=1.0),
    weight_cf: float = Query(0.5, ge=0.0, le=1.0)
):
    try:
        recommendations = hybrid_recommend(
            title,
            top_n=top_n,
            weight_cb=weight_cb,
            weight_cf=weight_cf
        )
        return {"movie_title": title, "recommendations": recommendations}
    except Exception as e:
        return {"error": str(e)}
