# --- hybrid.py ---
import pickle
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

# Directories
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

# Load saved CB model
with open(MODEL_DIR / "cb_model.pkl", "rb") as f:
    cb_model = pickle.load(f)

# Load saved CF model (SVD)
with open(MODEL_DIR / "cf_svd_model.pkl", "rb") as f:
    cf_model = pickle.load(f)

# Load movieId → title map
movie_map = joblib.load(MODEL_DIR / "movieid_to_title.joblib")

# Load ratings (needed for CF predictions)
ratings = pd.read_parquet(DATA_DIR / "ratings_cleaned.parquet")


# --- Hybrid Function ---
def hybrid_recommend(movie_title, user_id, top_n=10, weight_cb=0.5, weight_cf=0.5):
    """
    Hybrid Recommendations: combines Content-Based and Collaborative Filtering

    movie_title: str - movie to base recommendations on
    user_id: int - the user for collaborative filtering
    top_n: int - number of recommendations
    weight_cb: float - weight for content-based score
    weight_cf: float - weight for collaborative score
    """

    # --- Content-Based Part ---
    indices = cb_model["indices"]
    df = cb_model["df"]
    tfidf_matrix = cb_model["tfidf_matrix"]

    movie_title = movie_title.lower().strip()
    if movie_title not in indices:
        return []

    idx = indices[movie_title]
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
    sim_scores = list(enumerate(cosine_sim))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n * 2]
    cb_candidates = df['title'].iloc[[i[0] for i in sim_scores]].tolist()
    cb_scores = {movie: (top_n * 2 - rank) for rank, movie in enumerate(cb_candidates)}

    # --- Collaborative Filtering Part ---
    seen_movies = ratings.loc[ratings["userId"] == user_id, "movieId"].tolist()
    all_movies = list(movie_map.keys())

    predictions = []
    for movie_id in all_movies[:5000]:  # 🔹 limit to avoid slowness
        if movie_id not in seen_movies:
            pred = cf_model.predict(user_id, movie_id)
            predictions.append((movie_id, pred.est))

    predictions.sort(key=lambda x: x[1], reverse=True)
    cf_candidates = [movie_map[mid] for mid, _ in predictions[:top_n * 2]]
    cf_scores = {movie: (top_n * 2 - rank) for rank, movie in enumerate(cf_candidates)}

    # --- Merge CB + CF ---
    all_movies = set(cb_scores.keys()) | set(cf_scores.keys())
    final_scores = {}
    for movie in all_movies:
        score_cb = cb_scores.get(movie, 0)
        score_cf = cf_scores.get(movie, 0)
        final_score = (score_cb * weight_cb) + (score_cf * weight_cf)
        final_scores[movie] = final_score

    # Sort final scores
    sorted_movies = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

    return [movie for movie, score in sorted_movies][:top_n]
