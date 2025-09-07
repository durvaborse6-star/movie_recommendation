# app.py

import streamlit as st
import pickle
import pandas as pd
from difflib import get_close_matches  # ✅ Make sure this is here!

# Load saved data
movies_dict = pickle.load(open('data/movies_dict.pkl', 'rb'))
similarity = pickle.load(open('data/similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

def recommend(title):
    title = title.lower()
    movies_lower = movies['title'].str.lower()
    if title not in movies_lower.values:
        matches = get_close_matches(title, movies_lower.values)
        if matches:
            title = matches[0]
        else:
            return ["Movie not found!"]
    idx = movies_lower[movies_lower == title].index[0]
    distances = list(enumerate(similarity[idx]))
    sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)
    recommended = []
    for i in sorted_movies[1:6]:
        recommended.append(movies.iloc[i[0]].title)
    return recommended

st.title("Movie Recommendation System")

movie_name = st.text_input("Enter a movie name")

if st.button("Recommend"):
    if movie_name:
        recommendations = recommend(movie_name)
        st.write(f"Recommendations like '{movie_name}':")
        for movie in recommendations:
            st.write("- " + movie)
    else:

        st.write("Please enter a movie name.")
