from flask import Flask,render_template,request,redirect,jsonify
import pandas as pd
import pickle
import numpy as np

rating_dict = {}

liked_movies = set()
disliked_movies = set()

with open("similar_movies.pickle", 'rb') as handle:
    similar_movies = pickle.load(handle)

with open("sorted_movies.pickle", 'rb') as handle:
    sorted_movies = pickle.load(handle)

movie_df = pd.read_csv("Movies.csv",index_col=["movie_id"])
# movie_df_rate = pd.read_csv("Movies_rating.csv",index_col=["movie_id"])
movie_rated = list(movie_df.title)


x = (movie_df.loc[sorted_movies[:30]])
x.sort_values("Rating",inplace=True,ascending=False)
high_rated_movies = list(x.title.values)

movie_idx_dict = {}
idx_movie_dict = {}

for idx,row in movie_df.iterrows():
  movie_idx_dict[row["title"]] = idx
  idx_movie_dict[idx] = row["title"]


app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html",high_rated_movies=high_rated_movies[:15],
       liked_movies = liked_movies)


@app.route("/movie",methods=["GET","POST"])
def movie():
    movie_name = request.form.get("movie_name")
    rating = request.form.get("rating")

    if rating is not None:
        rating_dict[movie_name] = rating

    if movie_name not in movie_idx_dict.keys():
        return render_template("failure.html")

    mid = movie_idx_dict[movie_name]
    d_row = movie_df.loc[mid]
    d_row = (d_row["title"],d_row["Rating"])
    recc_movies = [idx_movie_dict[idx] for idx in similar_movies[mid][:15]]

    return render_template("movie.html",data = d_row,reccomended_movies = recc_movies)

@app.route("/search")
def search():
    movies = []
    search_name = request.args.get("movie_name")
    if search_name is None or len(search_name)==0: return jsonify(movies)
    id = 0
    for movie in movie_rated:
        if search_name.lower() in movie.lower():
            tmp = dict()
            tmp["title"] = movie
            movies.append(tmp)
        if len(movies) > 5:
            break
        
    return jsonify(movies)



if __name__ == "__main__":
    app.run(port=1200,debug=True)
