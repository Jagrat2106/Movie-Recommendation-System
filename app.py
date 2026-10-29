import pandas as pd
import streamlit as st
from recommender import movies, recommend_movies

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommendation System")
st.write("Discover movies similar to the ones you love!")

st.subheader("Find your next movie")

# Let the user select a movies
movie_titles = sorted(movies["title"].unique())

selected_movie = st.selectbox(
    "Choose a movie you like:",
    movie_titles
)

# Let the user choose how many recommendations to see
number_of_recommendations = st.slider(
    "Number of recommendations",
    min_value=5,
    max_value=10,
    value=10
)

# Generate recommendations when the button is clicked
if st.button("Recommend Movies", type="primary"):
    with st.spinner("Finding movies you may like..."):
        recommendations = recommend_movies(
            selected_movie,
            number_of_recommendations
        )

    if recommendations is not None and not recommendations.empty:
        st.subheader("Movies recommended for you")

        for _, movie in recommendations.iterrows():
            with st.container(border=True):
                st.markdown(f"### {movie['title']}")

                st.write(f"**Genres:** {movie['genres']}")
                rating = movie["vote_average"]
                if pd.notna(rating) and rating > 0:
                    st.write(f"**Average rating:** {rating}/10")
                else:
                    st.write("**Average rating:** Not available")

                overview = movie["overview"]

                if overview:
                    st.write(overview)
                else:
                    st.write("No plot description available.")

    else:
        st.warning("No recommendations found. Try another movie.")
