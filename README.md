# Movie Recommendation System

A movie recommendation web application built using Python, Streamlit, pandas, and scikit-learn.

## Features
- Select a movie from the available dataset.
- Get recommendations based on movie genres and plot descriptions.
- View movie genres, descriptions, ratings, and similarity scores.

## Technologies Used
- Python
- Streamlit
- pandas
- scikit-learn
- TF-IDF Vectorization
- Cosine Similarity

## How It Works
The system converts movie genres and plot descriptions into TF-IDF vectors and uses cosine similarity to recommend movies with similar content.

## Setup

1. Install Python.
2. Install the required libraries:

   pip install -r requirements.txt

3. Place the dataset at:

   data/tmdb_5000_movies.csv

4. Run the application:

   streamlit run app.py

## Dataset
TMDB 5000 Movie Dataset. The dataset must be obtained separately from an authorized source and placed in the data folder.

## Purpose
Developed as an academic and portfolio project.
