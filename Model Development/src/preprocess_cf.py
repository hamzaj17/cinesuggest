#--- src/preprocess_cf.py
"""
Load movie.csv and ratings.csv (MovieLens format), do light cleaning,
and save cleaned CSVs (optional). This prepares data for CF training.
"""

import pandas as pd
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def split_title_year(ml_title):
    """
    Split "Toy Story (1995)" -> ("Toy Story", 1995)
    If year not found, return (original_title, None)
    """
    s = str(ml_title).strip()
    match = re.match(r'^(.*)\s+\((\d{4})\)$', s)
    if match:
        return match.group(1).strip(), int(match.group(2))
    else:
        return s, None

def reorder_article(title):
    """
    Move trailing articles (The, A, An) to the front.
    e.g. "Godfather, The" -> "The Godfather"
    """
    if pd.isna(title):
        return title
    match = re.match(r'^(.*),\s+(The|A|An)$', title)
    if match:
        return f"{match.group(2)} {match.group(1)}"
    return title

def normalize_title(t):
    """
    Normalize a title to improve matching later.
    Lowercase, remove punctuation, collapse whitespace.
    """
    if pd.isna(t):
        return ''
    s = str(t).lower().strip()
    s = re.sub(r'[^a-z0-9\s]', '', s)   # remove punctuation
    s = re.sub(r'\s+', ' ', s)          # normalize spaces
    return s

def main():
    movie_path = DATA_DIR / "movie.csv"
    ratings_path = DATA_DIR / "ratings.csv"

    print("Loading files...")
    movies = pd.read_csv(movie_path)
    ratings = pd.read_csv(ratings_path)

    # Extract title and year from MovieLens title column
    print("Splitting title and year...")
    movies[['title_clean', 'year']] = movies['title'].apply(
        lambda t: pd.Series(split_title_year(t))
    )

    # Reorder articles to match CB dataset format
    print("Reordering articles in titles...")
    movies['title_clean'] = movies['title_clean'].apply(reorder_article)

    # Normalize titles for matching later
    print("Normalizing titles...")
    movies['title_norm'] = movies['title_clean'].apply(normalize_title)

    # Create a movie_key (title_norm + year) to be used later for merging with metadata
    movies['movie_key'] = movies.apply(
        lambda r: f"{r['title_norm']}_{int(r['year'])}" if pd.notna(r['year']) else r['title_norm'],
        axis=1
    )

    # Optional quick stats
    print("Movies loaded:", len(movies))
    print("Ratings loaded:", len(ratings))

    # Save cleaned versions (optional)
    out_movies = DATA_DIR / "movie_cleaned.csv"
    out_ratings = DATA_DIR / "ratings_cleaned.csv"
    movies.to_csv(out_movies, index=False)
    ratings.to_csv(out_ratings, index=False)
    print("Cleaned files saved to:", out_movies, out_ratings)

if __name__ == "__main__":
    main()
