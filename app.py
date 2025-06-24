import streamlit as st
import pandas as pd
import pickle
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

apiKey = os.getenv("API_KEY")


# Load data
movie = pickle.load(open('movies_df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Add placeholder option
movie_list = ["Select movie you like"] + movie['movie_name'].values.tolist()

# Recommendation function
def recommend(movie_name):
    index = movie[movie['movie_name'] == movie_name].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_names = []
    recommended_posters = []  # <-- You should store posters in your DataFrame
    for i in movies_list:
        movie_id = i[0]
        recommended_names.append(movie.iloc[movie_id].movie_name)
        # Here, replace 'poster_url' with your actual column name in movies_df
        # print(movie.iloc[movie_id])
        recommended_posters.append(movie.iloc[movie_id])
    return recommended_names, recommended_posters


def getPoster(id):
    return f"http://www.omdbapi.com/?i={id}&apikey={apiKey}"

# Streamlit UI
st.title("Movie Recommendation System")
selected_movie = st.selectbox("Select Movie You Like", movie_list)

if selected_movie != "Select movie you like" and st.button("Recommend"):
    names, posters = recommend(selected_movie)  # posters = imdb_ids

    cols = st.columns(5)  # create 5 columns for better layout

    for idx, (name, imdb_id) in enumerate(zip(names, posters)):
        # print(name, imdb_id['movie_id'])
        url = f"http://www.omdbapi.com/?i={imdb_id['movie_id']}&apikey=6bb8558c"
        response = requests.get(url)
        data = response.json()

        if data.get('Response') == 'True':
            with cols[idx % 5]:  # loop over 5 columns
                st.image(data.get('Poster'), use_column_width=True)
                st.markdown(f"<div style='text-align:center'><b>{name}</b></div>", unsafe_allow_html=True)
        else:
            with cols[idx % 5]:
                st.warning("Poster not found")

