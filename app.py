import streamlit as st
import sqlite3
import pandas as pd
import pickle
import requests
import os
import json
import hashlib
from streamlit_lottie import st_lottie

# ✅ TMDB API Key
api_key = os.getenv("TMDB_API_KEY", "c7ec19ffdd3279641fb606d19ceb9bb1")

# ✅ Load Lottie Animations Safely
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Could not load animation {filepath}: {e}")
        return None

# ✅ CSS Styling
def apply_custom_css():
    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 12px;
            padding: 0.6em 1.3em;
            font-weight: bold;
            transition: 0.3s ease;
            margin-top: 12px;
            font-size: 1rem;
        }
        .stButton > button:hover {
            background-color: #e60000;
            transform: scale(1.08);
        }
        .navbar {
            background: linear-gradient(135deg, #ff6b6b, #e60000);
            padding: 1em 1.5em;
            border-radius: 16px;
            margin-top: 30px;
            margin-bottom: 25px;
            box-shadow: 0 8px 20px rgba(230, 0, 0, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            user-select: none;
            transition: box-shadow 0.3s ease;
        }
        .navbar:hover {
            box-shadow: 0 12px 30px rgba(230, 0, 0, 0.7);
        }
        .navbar h2 {
            color: white;
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }
        .welcome-box {
            background-color: #f0f2f6;
            padding: 0.9em 1.3em;
            border-radius: 12px;
            color: #333;
            font-weight: 600;
            margin-top: 15px;
            margin-bottom: 15px;
            display: inline-block;
            font-size: 1.1rem;
        }
        .footer {
            text-align: center;
            padding: 1em 0;
            margin-top: 40px;
            color: #999;
            font-size: 0.95rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ✅ Password Hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ Database Setup
def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# ✅ TMDB Helpers
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get("poster_path")
        return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Image"
    except Exception:
        return "https://via.placeholder.com/300x450?text=Error"

def fetch_movie_info(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        data = requests.get(url).json()
        overview = data.get("overview", "No overview available.")
        release_date = data.get("release_date", "Unknown")
        genres = ", ".join([g["name"] for g in data.get("genres", [])])
        return overview, release_date, genres
    except Exception:
        return "No overview available.", "Unknown", "Unknown"

# ✅ Recommendation Logic
def recommend(movie_title, movies, similarity):
    try:
        movie_title_clean = movie_title.strip().lower()
        match = movies[movies['title'].str.strip().str.lower() == movie_title_clean]
        if match.empty:
            return [], [], [], [], [], []
        movie_idx = match.index[0]
        distances = list(enumerate(similarity[movie_idx]))
        sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:10]
        titles, posters, overviews, dates, genres_list, ids = [], [], [], [], [], []
        for idx, _ in sorted_movies:
            movie_id = int(movies.iloc[idx]['id'])
            title = movies.iloc[idx]['title']
            overview, release_date, genres = fetch_movie_info(movie_id)
            titles.append(title)
            posters.append(fetch_poster(movie_id))
            overviews.append(overview)
            dates.append(release_date)
            genres_list.append(genres)
            ids.append(movie_id)
        return titles, posters, overviews, dates, genres_list, ids
    except Exception as e:
        st.error(f"🚨 Recommendation error: {e}")
        return [], [], [], [], [], []

# ✅ Recommender App
def movie_recommender():
    st.title("🎬 Movie Recommender App")

    if not st.session_state.get("authenticated", False):
        st.info("🔐 Want to save favorites? Login or Signup below.")
        col1, col2 = st.columns(2)
        if col1.button("🔑 Login"):
            st.session_state.page = "login"
            st.stop()
        if col2.button("🆕 Signup"):
            st.session_state.page = "signup"
            st.stop()

    st.markdown(
        """
        <div class="navbar">
            <h2>🎥 Featured Movies</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sample_movie_ids = [1632, 299536, 17455, 2830, 429422, 157336, 603, 24428, 680]
    cols = st.columns(3)
    for i, mid in enumerate(sample_movie_ids):
        url = fetch_poster(mid)
        tmdb_link = f"https://www.themoviedb.org/movie/{mid}"
        with cols[i % 3]:
            st.markdown(f'<a href="{tmdb_link}" target="_blank"><img src="{url}" width="100%"></a>', unsafe_allow_html=True)

    if st.session_state.get("authenticated", False):
        username = st.session_state.get("username", "User")
        st.markdown(f'<div class="welcome-box">👋 Welcome, <b>{username}</b>!</div>', unsafe_allow_html=True)

        try:
            movies = pd.read_csv("dataset.csv")
            with open("similarity.pkl", "rb") as f:
                similarity = pickle.load(f)
        except Exception as e:
            st.error(f"🚨 Error loading movie data: {e}")
            return

        st.subheader("🎯 Find Similar Movies")
        selected_movie = st.selectbox("🎞️ Select a movie you like", sorted(movies['title'].values))

        if st.button("🎯 Recommend Movies"):
            with st.spinner("Fetching your recommendations..."):
                titles, posters, overviews, dates, genres_list, movie_ids = recommend(selected_movie, movies, similarity)

                match = movies[movies['title'].str.strip().str.lower() == selected_movie.strip().lower()]
                if not match.empty:
                    movie_id = int(match.iloc[0]['id'])
                    title = match.iloc[0]['title']
                    overview, release_date, genres = fetch_movie_info(movie_id)
                    selected_poster = fetch_poster(movie_id)
                    titles.insert(0, title)
                    posters.insert(0, selected_poster)
                    overviews.insert(0, overview)
                    dates.insert(0, release_date)
                    genres_list.insert(0, genres)
                    movie_ids.insert(0, movie_id)

            if titles:
                st.subheader("🎥 Top Recommendations For You")
                cols = st.columns(5)
                for i in range(min(10, len(titles))):
                    with cols[i % 5]:
                        st.image(posters[i], use_container_width=True)
                        tmdb_url = f"https://www.themoviedb.org/movie/{movie_ids[i]}"
                        if titles[i].strip().lower() == selected_movie.strip().lower():
                            st.markdown(
                                f"""
                                <a href="{tmdb_url}" target="_blank">
                                    <b style="color:#e60000;"><u>{titles[i]} (Selected)</u></b>
                                </a>
                                """, unsafe_allow_html=True
                            )
                        else:
                            st.markdown(f"[{titles[i]}]({tmdb_url})", unsafe_allow_html=True)
                        st.caption(f"🗓️ {dates[i]}  🎭 {genres_list[i]}")
                        st.write(overviews[i])
            else:
                st.warning("❌ No recommendations found.")

        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.page = "app"
            st.stop()

# ✅ Main App Router
def main():
    st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
    apply_custom_css()
    create_users_table()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "page" not in st.session_state:
        st.session_state.page = "app"

    if st.session_state.page == "signup":
        from signup import signup
        signup()
    elif st.session_state.page in ["login", "forgot_pass_page"]:
        from login import login, forgot_pass_page
        if st.session_state.page == "login":
            login()
        else:
            forgot_pass_page()
    elif st.session_state.page == "app":
        movie_recommender()

    # ✅ Footer
    st.markdown(
        """
        <div class="footer">
            Created by Himanshu, Raunak, Hritwik, & Anand
        </div>
        """,
        unsafe_allow_html=True
    )

# ✅ Run App
if __name__ == "__main__":
    main()
