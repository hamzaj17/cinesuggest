# ---src/train_cf.py
"""
Train an SVD collaborative filtering model using Surprise.
Saves the trained model to models/cf_svd_model.joblib
"""

import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
import joblib
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
MODEL_DIR = Path(__file__).resolve().parents[1] / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

def main():
    ratings_path = DATA_DIR / "ratings_cleaned.csv"  # produced by preprocess_cf.py
    ml_movies_path = DATA_DIR / "movie_cleaned.csv"

    print("Loading cleaned data...")
    ratings = pd.read_csv(ratings_path, nrows=3000000)
    ml_movies = pd.read_csv(ml_movies_path)

    # Surprise expects a DataFrame with columns: userId, itemId, rating
    # Use rating_scale based on your data (MovieLens commonly 0.5-5.0)
    reader = Reader(rating_scale=(float(ratings['rating'].min()), float(ratings['rating'].max())))
    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

    # Train-test split
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)
    print("Training SVD model...")
    algo = SVD(n_factors=50, n_epochs=25, random_state=42)  # you can tune these
    algo.fit(trainset)

    print("Evaluating on test set...")
    predictions = algo.test(testset)
    rmse = accuracy.rmse(predictions, verbose=True)
    mae = accuracy.mae(predictions, verbose=True)
    print(f"RMSE: {rmse}, MAE: {mae}")

    # Save model to disk
    model_file = MODEL_DIR / "cf_svd_model.joblib"
    joblib.dump(algo, model_file)
    print("Saved model to:", model_file)

    # Also save with pickle
    import pickle
    pickle_file = MODEL_DIR / "cf_svd_model.pkl"
    with open(pickle_file, "wb") as f:
        pickle.dump(algo, f)
    print("Saved model (pickle) to:", pickle_file)    

    # Save movieId->title mapping to disk (used for showing titles later)
    mapping_file = MODEL_DIR / "movieid_to_title.joblib"
    movie_map = pd.Series(ml_movies['title'].values, index=ml_movies['movieId']).to_dict()
    joblib.dump(movie_map, mapping_file)
    print("Saved movie mapping to:", mapping_file)

if __name__ == "__main__":
    main()

