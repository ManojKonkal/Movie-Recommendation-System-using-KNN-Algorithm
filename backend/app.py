from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
import warnings
import os

# Suppress sklearn tokenizer warning
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Health check route
@app.route('/')
def home():
    return "✅ Movie Recommendation System is running!"

# Define path to dataset
csv_path = os.path.join(os.path.dirname(__file__), 'data', 'indian movies.csv')

# Load dataset with error handling
try:
    movies = pd.read_csv(csv_path)
except FileNotFoundError:
    raise FileNotFoundError("Dataset 'indian movies.csv' not found. Please ensure it exists in the 'data/' directory.")

# Standardize column names
movies.columns = movies.columns.str.strip().str.lower()

# Validate required columns
required_columns = ['movie name', 'genre', 'language', 'rating(10)', 'votes']
missing_columns = [col for col in required_columns if col not in movies.columns]
if missing_columns:
    raise ValueError(f"The dataset is missing required columns: {', '.join(missing_columns)}")

# Drop rows with any missing required data
movies.dropna(subset=required_columns, inplace=True)

# Convert rating and votes to numeric types
movies['rating(10)'] = pd.to_numeric(movies['rating(10)'], errors='coerce')
movies['votes'] = pd.to_numeric(movies['votes'], errors='coerce')
movies.dropna(subset=['rating(10)', 'votes'], inplace=True)

# Genre vectorization for KNN model (optional but kept for future use)
vectorizer = CountVectorizer(tokenizer=lambda x: x.split('|'))
genre_matrix = vectorizer.fit_transform(movies['genre'])
knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
knn_model.fit(genre_matrix)

# API route for movie recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    language = data.get('language')
    sort_by = data.get('sort_by', 'rating')
    genre_filter = data.get('genre', 'All')

    if not language:
        return jsonify({'error': 'Language not provided. Please specify a language to get recommendations.'}), 400

    # Filter dataset by language
    filtered_movies = movies[movies['language'].str.lower() == language.lower()]

    # Filter by genre if selected
    if genre_filter and genre_filter != 'All':
        filtered_movies = filtered_movies[filtered_movies['genre'].str.contains(genre_filter, case=False, na=False)]

    if filtered_movies.empty:
        return jsonify({'recommendations': []})

    # Sort movies
    if sort_by == 'rating':
        filtered_movies = filtered_movies.sort_values(by='rating(10)', ascending=False)
    elif sort_by == 'votes':
        filtered_movies = filtered_movies.sort_values(by='votes', ascending=False)
    elif sort_by == 'name':
        filtered_movies = filtered_movies.sort_values(by='movie name', ascending=True)

    recommendations = filtered_movies[['movie name', 'rating(10)', 'votes', 'genre']].to_dict(orient='records')
    return jsonify({'recommendations': recommendations})

# Run the Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
