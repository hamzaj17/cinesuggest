from fastapi import FastAPI, Query
import pickle
import joblib
import pandas as pd
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from src.hybrid import hybrid_recommend   # hybrid still uses CB + CF

# ---------------- Paths ----------------
MODEL_DIR = Path(__file__).resolve().parents[0] / "models"
DATA_DIR = Path(__file__).resolve().parents[0] / "data"

# ---------------- Load Models ----------------
# Collaborative Filtering model
with open(MODEL_DIR / "cf_svd_model.pkl", "rb") as f:
    model_cf = pickle.load(f)

# Content-Based model
with open(MODEL_DIR / "cb_model.pkl", "rb") as f:
    model_cb = pickle.load(f)

# MovieId -> Title mapping
movie_map = joblib.load(MODEL_DIR / "movieid_to_title.joblib")

# Ratings (for CF)
ratings = pd.read_parquet(DATA_DIR / "ratings_cleaned.parquet")

# ---------------- FastAPI App ----------------
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

# ---------------- CB Logic (from saved pickle) ----------------
def recommend_cb_logic(movie_title: str, n: int = 5):
    """
    Recommend movies using saved cb_model.pkl
    """
    indices = model_cb["indices"]
    df = model_cb["df"]
    tfidf_matrix = model_cb["tfidf_matrix"]

    movie_title = movie_title.lower().strip()

    if movie_title not in indices:
        return []

    idx = indices[movie_title]

    # Compute similarity between this movie and all others
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()

    sim_scores = list(enumerate(cosine_sim))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Skip itself, take top-N
    sim_scores = sim_scores[1:n+1]
    movie_indices = [i[0] for i in sim_scores]

    return df['title'].iloc[movie_indices].tolist()

# ---------------- CB Endpoint ----------------
@app.get("/recommend/cb/{movie_title}")
def recommend_cb(movie_title: str, n: int = 5):
    """
    Content-Based Recommendations (using cb_model.pkl only)
    """
    try:
        recs = recommend_cb_logic(movie_title, n=n)
        if not recs:
            return {"error": f"Movie '{movie_title}' not found in dataset."}
        return {"movie_title": movie_title, "recommendations": recs}
    except Exception as e:
        return {"error": str(e)}

# ---------------- Hybrid Endpoint ----------------
@app.get("/recommend/hybrid/{user_id}/{title}")
def recommend_hybrid(
    title: str,
    user_id: int,
    top_n: int = Query(5, ge=1, le=20),
    weight_cb: float = Query(0.6, ge=0.0, le=1.0),
    weight_cf: float = Query(0.4, ge=0.0, le=1.0)
):
    try:
        recommendations = hybrid_recommend(
            title,
            user_id=user_id,
            top_n=top_n,
            weight_cb=weight_cb,
            weight_cf=weight_cf
        )
        return {"movie_title": title, "recommendations": recommendations}
    except Exception as e:
        return {"error": str(e)}
