import pickle
import streamlit as st
import requests
import os

# ----------------------------
# 🔽 Download similarity.pkl if missing
def download_file_from_google_drive(file_id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)
    token = None

    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value

    if token:
        response = session.get(URL, params={'id': file_id, 'confirm': token}, stream=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

# Google Drive file ID for similarity.pkl (your file)
SIMILARITY_FILE_ID = "1jfPnC3bWKjyb4Hj0ionlNOc9CCQ1dyJb"
SIMILARITY_PATH = "similarity.pkl"

if not os.path.exists(SIMILARITY_PATH):
    st.info("Downloading similarity matrix... Please wait ⏳")
    download_file_from_google_drive(SIMILARITY_FILE_ID, SIMILARITY_PATH)
    st.success("Downloaded similarity matrix successfully ✅")

# ----------------------------
# 🧠 Function to fetch poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f4b1c2ebfade74a6fa56a98f0355dec0&language=en-US"
        response = requests.get(url, timeout=2)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://dummyimage.com/500x750/cccccc/000000&text=No+Image"
    except requests.exceptions.Timeout:
        return "https://dummyimage.com/500x750/cccccc/000000&text=No+Image"
    except requests.exceptions.RequestException as e:
        return "https://dummyimage.com/500x750/cccccc/000000&text=No+Image"

# ----------------------------
# 🎯 Recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# ----------------------------
# 🎬 Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header('🎬 Movie Recommender System')

# Load pickled data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Display recommendations


# Display recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
