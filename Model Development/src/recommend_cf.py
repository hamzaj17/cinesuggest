"""
Collaborative Filtering (CF) Recommendation System

This file contains:
1. The main CF recommendation function (get_cf_recommendations_for_user) — unchanged prediction logic.
2. A wrapper function (get_cf_recommendations_for_title) for hybrid systems that only provide movie titles.
"""

import joblib
import pandas as pd
from pathlib import Path

# Paths for data & models
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
MODEL_DIR = Path(__file__).resolve().parents[1] / "models"

# ------------------- CORE CF RECOMMENDER (UNCHANGED) -------------------
def get_cf_recommendations_for_user(user_id, algo, ml_movies_df, ratings_df, top_n=10, min_votes=5):
    """
    Recommend movies for a given user using a trained collaborative filtering model.

    Parameters:
        user_id (int): The ID of the user to recommend for.
        algo: The trained CF algorithm (e.g., Surprise SVD).
        ml_movies_df (DataFrame): Movie metadata with 'movieId' and 'title'.
        ratings_df (DataFrame): Ratings data with 'userId', 'movieId', 'rating'.
        top_n (int): Number of recommendations to return.
        min_votes (int): Minimum number of ratings required for cold-start fallback.

    Returns:
        DataFrame: Top-N recommended movies with their predicted ratings.
    """
    all_movie_ids = ml_movies_df['movieId'].unique()

    # Movies the user already rated
    rated_by_user = set(ratings_df[ratings_df['userId'] == user_id]['movieId'].tolist())

    # Cold start: user has no ratings
    if len(rated_by_user) == 0:
        agg = ratings_df.groupby('movieId')['rating'].agg(['mean', 'count']).reset_index()
        agg = agg[agg['count'] >= min_votes].sort_values(by='mean', ascending=False)
        top = agg.head(top_n)
        results = []
        for _, row in top.iterrows():
            mid = int(row['movieId'])
            title_row = ml_movies_df[ml_movies_df['movieId'] == mid]
            title = title_row['title'].values[0] if not title_row.empty else "Unknown"
            results.append({
                'movieId': mid,
                'title': title,
                'avg_rating': round(row['mean'], 3),
                'num_votes': int(row['count'])
            })
        return pd.DataFrame(results)

    # Predict ratings for movies the user hasn't seen
    candidates = [mid for mid in all_movie_ids if mid not in rated_by_user]
    preds = []
    for mid in candidates:
        prediction = algo.predict(user_id, mid)
        preds.append((mid, prediction.est))

    preds_sorted = sorted(preds, key=lambda x: x[1], reverse=True)[:top_n]

    recs = []
    for mid, score in preds_sorted:
        title_row = ml_movies_df[ml_movies_df['movieId'] == mid]
        title = title_row['title'].values[0] if not title_row.empty else "Unknown"
        recs.append({
            'movieId': int(mid),
            'title': title,
            'pred_rating': round(score, 3)
        })
    return pd.DataFrame(recs)


# ------------------- WRAPPER FOR HYBRID SYSTEM -------------------
def get_cf_recommendations_for_title(movie_title, top_n=10):
    """
    Wrapper for hybrid filtering:
    - Loads the trained CF model & data automatically.
    - Finds a sample user who liked this movie (so we can get CF-style similar recommendations).
    - Calls get_cf_recommendations_for_user() internally.
    """
    # Load trained model and datasets
    algo = joblib.load(MODEL_DIR / "cf_svd_model.joblib")
    ml_movies_df = pd.read_csv(DATA_DIR / "movie_cleaned.csv")
    ratings_df = pd.read_csv(DATA_DIR / "ratings_cleaned.csv")

    # Find the movieId for the given title
    movie_row = ml_movies_df[ml_movies_df['title_clean'].str.lower() == movie_title.lower()]
    if movie_row.empty:
        print(f"Movie '{movie_title}' not found in movie dataset.")
        return []

    movie_id = int(movie_row.iloc[0]['movieId'])

    # Find a user who rated this movie highly (≥ 4.0 stars)
    high_rater = ratings_df[(ratings_df['movieId'] == movie_id) & (ratings_df['rating'] >= 4.0)]
    if high_rater.empty:
        print(f"No high-rating users found for '{movie_title}', using a random user.")
        user_id = int(ratings_df.sample(1)['userId'].values[0])
    else:
        user_id = int(high_rater.sample(1)['userId'].values[0])

    # Get CF recommendations for that user
    recs_df = get_cf_recommendations_for_user(user_id, algo, ml_movies_df, ratings_df, top_n=top_n)

    # Return only movie titles for hybrid system
    return recs_df['title'].tolist()

# print(get_cf_recommendations_for_title("Toy Story", top_n=5))