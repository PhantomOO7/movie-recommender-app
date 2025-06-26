import streamlit as st
import pandas as pd
import pickle
import requests
import gdown  # ✅ Make sure to include this in requirements.txt

MOVIES_ID = "1fqAvwG40ItYktHhAh_HphfqmgSrpFdwi"
SIMILARITY_ID = "1aQIMTClslgvdhPxtYeF6zNaHtB2sIBGR"

@st.cache_resource(show_spinner="Downloading data from Google Drive...")
def load_data():
    gdown.download(f"https://drive.google.com/uc?id={MOVIES_ID}", "movies.pkl", quiet=False)
    gdown.download(f"https://drive.google.com/uc?id={SIMILARITY_ID}", "similarity.pkl", quiet=False)

    with open("movies.pkl", "rb") as f:
        movies = pd.DataFrame(pickle.load(f))

    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)

    return movies, similarity

def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=ed5d3391d93b228448f662150c9022ae&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

# -------------------------------
# UI
# -------------------------------
st.title('Movie Recommender System')

movies, similarity = load_data()

selected_movie = st.selectbox('search movies', movies['title'].values)

if st.button('recommend movies'):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
