import streamlit as st
import pickle
import pandas as pd

# ------------------------------
# Load Data
# ------------------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))  # similarity matrix

# ------------------------------
# Streamlit App
# ------------------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

# ------------------------------
# Recommendation Function
# ------------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]  # top 5 similar movies (excluding itself)

    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# ------------------------------
# UI
# ------------------------------
selected_movie_name = st.selectbox(
    "🎥 Select a movie:",
    movies['title'].values
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.write("### 🍿 Recommended Movies:")

    # Display recommendations in 2 columns
    cols = st.columns(2)
    for idx, movie in enumerate(recommendations):
        with cols[idx % 2]:
            st.markdown(
                f"""
                <div style="
                    background-color:#f9f9f9;
                    padding:15px;
                    border-radius:12px;
                    margin-bottom:12px;
                    box-shadow:2px 2px 8px rgba(0,0,0,0.1);">
                    <h4 style="color:#222; margin:0;">🎬 {movie}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )
