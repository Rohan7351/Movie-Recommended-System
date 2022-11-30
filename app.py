import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
movies=pd.DataFrame(movies_dict)
st.title('Movie Recommend system')
def fetch_poster(movie_id):
    responce=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=d811332ab27d69e9010a349f171f2b9a&language=en-US".format(movie_id))
    data=responce.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
    
def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6] 
    recommend_movie=[]
    recommend_movies_poster=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        #fetch poster from api
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommend_movie,recommend_movies_poster

option = st.selectbox(
    'How would you like to be contacted?',
   movies['title'].values )


st.write('You selected:', option)
if st.button('Recommend'):
    val,posters=recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(val[0])
        st.image(posters[0])

    with col2:
        st.text(val[1])
        st.image(posters[1])

    with col3:
        st.text(val[2])
        st.image(posters[2])
    
    with col4:
        st.text(val[3])
        st.image(posters[3])
    
    with col5:
        st.text(val[4])
        st.image(posters[4])
