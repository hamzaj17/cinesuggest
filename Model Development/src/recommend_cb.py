# --- recommend_cb.py ---
import pickle
from sklearn.metrics.pairwise import cosine_similarity

model_path = "D:\cinesuggest\Model Development\models\cb_model.pkl"

# Load the trained model
with open(model_path, "rb") as f:
    model_data = pickle.load(f)

tfidf = model_data["tfidf"]
tfidf_matrix = model_data["tfidf_matrix"]
indices = model_data["indices"]
df = model_data["df"]

def recommend(title, num_recommendations=5):
    """
    Recommend movies similar to the given title
    """
    title = title.lower().strip()
    if title not in indices:
        print("❌ Movie not found in dataset.")
        return []
    
    idx = indices[title]  # index of movie in dataframe
    
    # Compute similarity only for this one movie row
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix)
    
    sim_scores = list(enumerate(cosine_sim.flatten()))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations+1]  # skip itself
    
    movie_indices = [i[0] for i in sim_scores]
    
    return df['title'].iloc[movie_indices].tolist()

# # Example usage
if __name__ == "__main__":
    print("Recommendations for 'The Godfather':")
    print(recommend("The Godfather", num_recommendations=10))
