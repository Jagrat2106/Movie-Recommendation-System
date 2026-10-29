import ast
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Locate and load the dataset
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "tmdb_5000_movies.csv"

movies = pd.read_csv(DATA_PATH)

# Select required columns
movies = movies[
    ["title", "genres", "overview", "vote_average", "vote_count"]
].copy()

# Clean missing values
movies = movies.dropna(subset=["title"]).reset_index(drop=True)
movies["overview"] = movies["overview"].fillna("")
movies["genres"] = movies["genres"].fillna("")

# Combine genres and descriptions

def extract_genres(genre_text):
    try:
        genres = ast.literal_eval(genre_text)
        return ", ".join(
            genre["name"] for genre in genres
        )
    except (ValueError, SyntaxError, TypeError, KeyError):
        return ""

movies["genres"] = movies["genres"].apply(extract_genres)

movies["content"] = movies["genres"] + " " + movies["overview"]

# Convert text to TF-IDF vectors
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies["content"])

# Calculate similarity between movies
similarity_matrix = cosine_similarity(tfidf_matrix)


def recommend_movies(movie_title, number_of_recommendations=10):
    # Find the selected movie
    matches = movies[
        movies["title"].str.casefold() == movie_title.casefold()
    ]

    if matches.empty:
        return None

    # Use the first match if titles are duplicated
    movie_index = matches.index[0]

    # Get similarity scores for this movie
    scores = list(enumerate(similarity_matrix[movie_index]))

    # Sort from most similar to least similar
    scores = sorted(scores, key=lambda item: item[1], reverse=True)

    # Exclude the selected movie itself
    scores = [
        item for item in scores
        if item[0] != movie_index
    ]

    # Select the top recommendations
    top_scores = scores[:number_of_recommendations]

    # Return the recommended movies
    results = movies.iloc[[item[0] for item in top_scores]][
        ["title", "genres", "overview", "vote_average", "vote_count"]
    ].copy()

    results["similarity_score"] = [
        round(item[1], 3) for item in top_scores
    ]

    return results


if __name__ == "__main__":
    test_movie = movies.iloc[0]["title"]

    print("Testing recommendations for:", test_movie)

    recommendations = recommend_movies(test_movie)

    if recommendations is not None:
        print("\nRecommended movies:")
        print(
            recommendations[
                ["title", "genres", "similarity_score"]
            ].to_string(index=False)
        )
