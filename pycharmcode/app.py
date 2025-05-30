import streamlit as st
import pickle
import pandas as pd
import requests

# Apply custom CSS
def apply_css():
    st.markdown("""
    <style>
        /* Animated Gradient Background */
        .stApp {
            background: linear-gradient(-45deg, #1f1c2c, #928DAB, #1f4037, #99f2c8);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }

        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        /* Navbar styling */
        .navbar {
            display: flex;
            justify-content: center;
            background-color: rgba(0, 0, 0, 0.8);
            padding: 1rem;
            border-radius: 0 0 10px 10px;
            margin-bottom: 30px;
        }

        .nav-item {
            margin: 0 20px;
            font-size: 18px;
            color: white;
            text-decoration: none;
            font-weight: bold;
            transition: color 0.3s ease;
        }

        .nav-item:hover {
            color: #ff4b2b;
        }

        h1 {
            text-align: center;
            color: white;
            text-shadow: 2px 2px 4px black;
        }

        .stButton button {
            background-color: #ff4b2b;
            color: white;
            border-radius: 8px;
            font-weight: bold;
            box-shadow: 0 4px 10px black;
        }

        .movie-card {
            padding: 5px;
            border-radius: 12px;
            background-color: rgba(0, 0, 0, 0.5);
            box-shadow: 2px 2px 10px black;
        }

        .movie-title {
            color: white;
            text-align: center;
            margin-top: 8px;
            font-size: 16px;
        }
    </style>
    """, unsafe_allow_html=True)

# Load models
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

# Poster fetcher
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8d751eb6f35b1f2fce01fe0b155a4513&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', '')

# Recommend
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
    names, posters = [], []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return names, posters

# --- UI Starts Here ---
apply_css()

# --- Top Navbar ---
st.markdown("""
<div class="navbar">
    <a class="nav-item" href="?nav=home">Home</a>
    <a class="nav-item" href="?nav=contact">Contact Us</a>
</div>
""", unsafe_allow_html=True)

# --- Navigation Logic ---
nav = st.query_params.get("nav", "home")

# --- Home Page ---
if nav == "home":
    st.title("🎬 Movie Recommender System")
    movie_name = st.selectbox("Search for a movie you like:", movies['title'].values)

    if st.button("Recommend"):
        names, posters = recommend(movie_name)
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"""
                    <div class="movie-card">
                        <img src="{posters[i]}" width="100%">
                        <div class="movie-title">{names[i]}</div>
                    </div>
                """, unsafe_allow_html=True)

# --- Contact Us Page ---
elif nav == "contact":
    st.title("📞 Contact Us")
    st.markdown("""
        **Developer:** Danyal Arshad  
        **Email:** danyalarshad34567@gmail.com  
        **GitHub:** [DanyalDev](https://github.com)  
        **Location:** Pakistan 🇵🇰  

        _Have a suggestion? Reach out!_
    """)

