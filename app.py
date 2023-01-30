from flask import Flask,request,jsonify

import pickle
import pandas as pd
import requests

movies=pickle.load(open('./movies.pkl','rb'))
movies=pd.DataFrame(movies)
similarity=pickle.load(open('./similarity.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

def get_posters(movie_id):
    data=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=5177b3d25448b9eec5d4b28b8dfabc83&language=en-US".format(movie_id))
    response=data.json()
    poster_path = response['poster_path']
    
    return "https://image.tmdb.org/t/p/w500/" + poster_path

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)), reverse=True ,key=lambda x:x[1])[1:6]
    recommended=[]
    movie_ids=[]
    posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        print(movies.iloc[i[0]].title)
        movie_ids.append(movies.iloc[i[0]].movie_id)
        recommended.append((movies.iloc[i[0]].title))
        posters.append(get_posters(movie_id))
    return recommended,movie_ids,posters

@app.route('/predict',methods=['POST'])
def predict():
    movieName = request.form.get('movieName')

    recommendMovie,movieID,moviePosters = recommend(movieName)

    movie1Name = recommendMovie[0]
    movie1Id = movieID[0]
    poster1 = moviePosters[0]

    movie2Name = recommendMovie[1]
    movie2Id = movieID[1]
    poster2 = moviePosters[1]

    movie3Name = recommendMovie[2]
    movie3Id = movieID[2]
    poster3 = moviePosters[2]

    movie4Name = recommendMovie[3]
    movie4Id = movieID[3]
    poster4 = moviePosters[3]

    movie5Name = recommendMovie[4]
    movie5Id = movieID[4]
    poster5 = moviePosters[4]

    return jsonify({'movieName': str(movie1Name), 'movieId': str(movie1Id), 'poster': str(poster1)},{ 'movieName': str(movie2Name), 'movieId': str(movie2Id),'poster': str(poster2)},
    { 'movieName': str(movie3Name), 'movieId': str(movie3Id), 'poster': str(poster3)},{'movieName': str(movie4Name), 'movieId': str(movie4Id), 'poster': str(poster4)},{'movieName': str(movie5Name), 'movieId': str(movie5Id), 'poster': str(poster5)})

if __name__ == '__main__':
    app.run(debug=True)