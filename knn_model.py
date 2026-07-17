import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
import warnings
import os

# Suppress sklearn tokenizer warning
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

# Construct dataset path relative to this file
csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'indian movies.csv')

# Load the dataset
try:
    movies = pd.read_csv(csv_path)
except FileNotFoundError:
    raise FileNotFoundError("Dataset 'indian movies.csv' not found. Please place it in the 'backend/data/' folder.")

# Clean and standardize column names
movies.columns = movies.columns.str.strip().str.lower()

# Ensure required columns exist
required_columns = ['movie name', 'genre']
missing = [col for col in required_columns if col not in movies.columns]
if missing:
    raise ValueError(f"Missing required columns: {', '.join(missing)}")

# Drop rows with missing values
movies = movies.dropna(subset=['movie name', 'genre'])

# Vectorize genre column
vectorizer = CountVectorizer(tokenizer=lambda x: x.split('|'))
genre_matrix = vectorizer.fit_transform(movies['genre'])

# Fit KNN model
knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
knn_model.fit(genre_matrix)

# Recommendation function
def get_recommendations(movie_title, k=5):
    matches = movies[movies['movie name'].str.contains(movie_title, case=False, na=False)]
    if matches.empty:
        return ["Movie not found."]
    
    movie_index = matches.index[0]
    distances, indices = knn_model.kneighbors(genre_matrix[movie_index], n_neighbors=k + 1)
    recommended_movies = movies.iloc[indices[0][1:]]['movie name'].tolist()
    
    return recommended_movies
