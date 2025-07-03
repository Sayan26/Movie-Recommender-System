import pickle
import streamlit as st
import requests


# Function to safely fetch poster from TMDB API
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f4b1c2ebfade74a6fa56a98f0355dec0&language=en-US"
        response = requests.get(url, timeout=2)
        response.raise_for_status()
        data = response.json()
        st.text(data)
        poster_path = data['poster_path']
        st.text(poster_path)
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except requests.exceptions.Timeout:
        print(f"Timeout while fetching movie {movie_id}")
        return "https://dummyimage.com/500x750/cccccc/000000&text=No+Image"

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "https://dummyimage.com/500x750/cccccc/000000&text=No+Image"





# Recommendation logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movies_id = movies.iloc[i[0]].movie_id
        st.text(f"Movie ID: {movies_id}")
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movies_id))
        #time.sleep(1.5)  # wait to avoid TMDB rate limiting or disconnection
    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header('🎬 Movie Recommender System')

# Load preprocessed data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl','rb'))



movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

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
