from src.model_cb import recommend as recommend_cb
from src.recommend_cf import get_cf_recommendations_for_title as recommend_cf

def hybrid_recommend(movie_title, top_n=10, weight_cb=0.5, weight_cf=0.5):
    """
    Combine Content-Based and Collaborative Filtering results.
    
    movie_title: str - movie title
    top_n: int - number of final recommendations
    weight_cb: float - weight for content-based score
    weight_cf: float - weight for collaborative score
    """
    
    # Get recommendations from content-based
    cb_results = recommend_cb(movie_title, num_recommendations=top_n*2)
    cb_scores = {movie: (top_n*2 - rank) for rank, movie in enumerate(cb_results)}

    # Get recommendations from collaborative filtering
    cf_results = recommend_cf(movie_title, top_n=top_n*2)
    cf_scores = {movie: (top_n*2 - rank) for rank, movie in enumerate(cf_results)}

    # Merge scores
    all_movies = set(cb_scores.keys()) | set(cf_scores.keys())
    final_scores = {}
    for movie in all_movies:
        score_cb = cb_scores.get(movie, 0)
        score_cf = cf_scores.get(movie, 0)
        final_score = (score_cb * weight_cb) + (score_cf * weight_cf)
        final_scores[movie] = final_score

    # Sort by final score
    sorted_movies = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

    return [movie for movie, score in sorted_movies][:top_n]


# run it with: python -m src.hybrid