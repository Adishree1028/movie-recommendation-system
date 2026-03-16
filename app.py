import pickle
import streamlit as st
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Constants
OMDB_API_KEY = "52227b6b"  # Your OMDb API key

# Function to fetch poster from OMDb
def fetch_poster_omdb(movie_title):
    try:
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise error for bad responses
        data = response.json()
        if data['Response'] == 'True':  # Check if the movie was found
            return data['Poster']  # Return the poster URL
        return None
    except Exception as e:
        logging.error(f"OMDb API Error: {e}")
        return None

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:  # Get top 5 recommendations
        movie_title = movies.iloc[i[0]].title
        poster_url = fetch_poster_omdb(movie_title)
        if poster_url:
            recommended_movie_posters.append(poster_url)
            recommended_movie_names.append(movie_title)
    return recommended_movie_names, recommended_movie_posters

# Streamlit App
st.header('Movie Recommender System')

# Load movie data and similarity matrix
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Dropdown for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Button to show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    if recommended_movie_names and recommended_movie_posters:
        # Create dynamic columns based on available recommendations
        cols = st.columns(min(len(recommended_movie_names), 5))
        for idx, col in enumerate(cols):
            with col:
                st.text(recommended_movie_names[idx])
                st.image(recommended_movie_posters[idx])
    else:
        st.error("No recommendations available or error fetching data")