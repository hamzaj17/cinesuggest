import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# 1. Load data          
df = pd.read_csv("D:\cinesuggest\Model Development\data\movies.csv")

# 2. Handle missing values
df = df.dropna(subset=['title', 'genre', 'director', 'stars'])  # Drop rows missing key info
df = df.fillna('')  # Fill other missing values with empty string

# 3. Remove duplicate entries based on title and year
df = df.drop_duplicates(subset=['title', 'year'])

# 4. Extract relevant features

# -- Genres: split by comma and strip spaces
df['genres'] = df['genre'].apply(lambda x: [g.strip() for g in x.split(',')])

# -- Director: extract first name from list string
def extract_director(director_str):
    try:
        names = ast.literal_eval(director_str)
        return names[0] if isinstance(names, list) and len(names) > 0 else ''
    except:
        return ''
df['director_name'] = df['director'].apply(extract_director)

# -- Actors: extract all except first from list string
def extract_actors(stars_str):
    try:
        names = ast.literal_eval(stars_str)
        return names if isinstance(names, list) else []
    except:
        return []
df['actors'] = df['stars'].apply(extract_actors)

#create a combined text feature:
df['combined_features'] = (
    df['title'].fillna('') + ' ' +
    (df['genre'].fillna('') + ' ') * 3 +
    df['director_name'].fillna('') + ' ' 
    # df['stars'].fillna('')
)

# Preview the cleaned DataFrame
# print(df[['title', 'genres', 'director_name', 'actors', 'combined_features']].head(20))


# 1. Vectorize the combined features
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])

# print("TF-IDF matrix shape:", tfidf_matrix.shape)  # (num_movies, num_features)

# 2. Build a reverse mapping of movie titles to DataFrame indices
indices = pd.Series(df.index, index=df['title'].str.lower())

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
titles = df['title'].tolist()

model_path = "D:\cinesuggest\Model Development\models\cb_model.pkl"
# saving the model
with open(model_path, "wb") as f:
    pickle.dump({
        "tfidf": tfidf,
        "tfidf_matrix": tfidf_matrix,
        "indices": indices,
        "df": df
    }, f)

print("✅ Content-Based model trained & saved as cb_model.pkl")