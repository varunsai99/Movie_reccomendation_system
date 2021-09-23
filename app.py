from flask import Flask,render_template,request,redirect,jsonify
from numpy.lib.financial import rate
from numpy.lib.function_base import append
import pandas as pd
import numpy as np
from dependencies import *


app = Flask(__name__)

# try reloading the chrome using ctrl + shift + R for CSS to work

@app.route("/",methods=["GET","POST"])
def index():
    sample_train_sparse_matrix = sparse.load_npz("./data/sample_train_sparse_matrix.npz")
    rated_movies = sample_train_sparse_matrix[user].nonzero()[1]
    rating = sample_train_sparse_matrix[user].toarray()[0][rated_movies]
    recc_liked = []
    liked_movie_name = ""
    # Movies that are liked by the user
    if liked_movies[0] != -1:
        liked_movie_name = idx_movie_dict[liked_movies[0]]
        recc_liked = [idx_movie_dict[idx] for idx in similar_movies[liked_movies[0]][:15]]

    # For computing the Ratings by Machine Learning model
    m_ids = []
    for i in range(len(rated_movies)):
        if(rating[i]>=3): m_ids.append(rated_movies[i])

    recc_movies_model = set()
    recc_names_model = []
    if len(m_ids)!=0:
        idx=0
        while len(recc_movies_model) < 10:
            for m_id in m_ids:
                recc_movies_model.add(similar_movies[m_id][idx])
            idx+=1

        model_list = calculate_predictions(recc_movies_model)
        for x in model_list:
            if x[0] < 3: break
            recc_names_model.append(idx_movie_dict[x[1]])
    # print(recc_names_model)
    return render_template("index.html",high_rated_movies=high_rated_movies[:15],
        liked_movie_name = liked_movie_name,liked_movie=recc_liked,model_movies=recc_names_model)


@app.route("/movie",methods=["GET","POST"])
def movie():
    movie_name = request.form.get("movie_name")
    rating = request.form.get("rating")
    mid = movie_idx_dict[movie_name]
    tmp = sample_train_sparse_matrix[user].toarray()[0]
    if rating is not None:
        tmp[mid] = rating
        if rating > '3': liked_movies[0] = mid
        sample_train_sparse_matrix[user] = csr_matrix(tmp)
        sparse.save_npz('./data/sample_train_sparse_matrix.npz', sample_train_sparse_matrix)

    if movie_name not in movie_idx_dict.keys():
        return render_template("failure.html")

    rated = tmp[mid]
    d_row = movie_df.loc[mid]
    d_row = (d_row["title"],round(d_row["Rating"],2))
    recc_movies = [idx_movie_dict[idx] for idx in similar_movies[mid][:15]]

    return render_template("movie.html",data = d_row,reccomended_movies = recc_movies,rated=rated)

@app.route("/search",methods=["GET","POST"])
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
