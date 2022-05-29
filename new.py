import pickle
import streamlit as st
import requests

#from typing import DefaultDict, List
#from collections import defaultdict, deque
#globalUserData: DefaultDict[str, List[str]] = defaultdict(deque)

# UserData: DefaultDict[str, List[str]] = default-dict(deque)
# UserData["ps"]=['beauty']
# st.write(UserData["ps"])
class User:
    # initialize
    def __init__(self):
        self.Username = ""
        self.watched = ""
        #self.UserData: DefaultDict[str, List[str]] = defaultdict(deque)

    def setName(self, name):
        self.Username = name
        #self.UserData[name] = []

    def getName(self):
        return self.Username

    def setActivity(self, movie_name):
        self.watched = movie_name
        #tempname = self.getName()
        #st.write(globalUserData[tempname])
        ##st.write(globalUserData[tempname])


    def getActivity(self):
        return self.Username, self.watched


st.title("The Movie Store")

st.header("Login")
x = st.text_input('enter your user id', value="", max_chars=25)
p1 = User()
p1.setName(x)
st.button('login', on_click=None)

st.header('Popular Movies')
popular_movies = pickle.load(open('popular_movie_list.pkl', 'rb'))
popular_movie_list = popular_movies['title'].values
count = 0
for values in popular_movies['title']:
    if count < 10:
        st.write(values)
    count = count + 1

st.header('New Releases')
new_movies = pickle.load(open('new_movie_list.pkl', 'rb'))
new_movie_list = new_movies['title'].values
count = 0
for values1 in new_movies['title']:
    if count < 10:
        st.write(values1)
    count = count + 1

st.header('Blockbuster Movies')
blockbuster_movies = pickle.load(open('blockbuster_movie_list.pkl', 'rb'))
blockbuster_movie_list = blockbuster_movies['title'].values
count = 0
for values1 in blockbuster_movies['title']:
    if count < 10:
        st.write(values1)
    count = count + 1


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []

    for value2 in distances[1:6]:
        recommended_movie_names.append(movies.iloc[value2[0]].title)

    return recommended_movie_names


st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
if st.button('Show Recommendation'):
    recommendations = recommend(selected_movie)

    p1.setActivity(selected_movie)
    for i in recommendations:
        st.write(i)

# tempusername, tempwatched = p1.getActivity()
# st.write(tempusername, tempwatched)
# if (st.button('Show Recommendation') and st.button('login')):
#   user_name = p1.getName()
#   st.write(user_name)
# if len(globalUserData)!=0:
#    st.write(globalUserData[tempusername])