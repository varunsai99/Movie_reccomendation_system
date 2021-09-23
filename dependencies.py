import pandas as pd
import pickle
import numpy as np
from scipy import sparse
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from models import *

def get_average_ratings(sparse_matrix, of_users):
  ax = 1 if of_users else 0  # 1 - User axes,0 - Movie axes
  sum_of_ratings = sparse_matrix.sum(axis=ax).A1
  is_rated = sparse_matrix!=0
  no_of_ratings = is_rated.sum(axis=ax).A1
  u,m = sparse_matrix.shape
  average_ratings = { i : sum_of_ratings[i]/no_of_ratings[i] for i in range(u if of_users else m) if no_of_ratings[i] !=0 }
  return average_ratings

def get_ratings(predictions):
    actual = np.array([pred.r_ui for pred in predictions])
    pred = np.array([pred.est for pred in predictions])
    return actual, pred

def get_vector(movie):
    try:   
        user_sim = cosine_similarity(sample_train_sparse_matrix[user], sample_train_sparse_matrix).ravel()
        top_sim_users = user_sim.argsort()[::-1][1:20] 
        top_ratings = sample_train_sparse_matrix[top_sim_users, movie].toarray().ravel()
        top_sim_users_ratings = list(top_ratings[top_ratings != 0][:5])
        top_sim_users_ratings.extend([sample_train_averages['movie'][movie]]*(5 - len(top_sim_users_ratings)))

    except (IndexError, KeyError):
        top_sim_users_ratings.extend([sample_train_averages['global']]*(5 - len(top_sim_users_ratings)))

    #--------------------- Ratings by "user"  to similar movies of "movie" ---------------------
    try: 
        movie_sim = cosine_similarity(sample_train_sparse_matrix[:,movie].T, sample_train_sparse_matrix.T).ravel()
        top_sim_movies = movie_sim.argsort()[::-1][1:] 
        top_ratings = sample_train_sparse_matrix[user, top_sim_movies].toarray().ravel()
        top_sim_movies_ratings = list(top_ratings[top_ratings != 0][:5])
        top_sim_movies_ratings.extend([sample_train_averages['user'][user]]*(5-len(top_sim_movies_ratings))) 
        
    except (IndexError, KeyError):
        top_sim_movies_ratings.extend([sample_train_averages['global']]*(5-len(top_sim_movies_ratings)))

    row = list()
    row.append(sample_train_averages['global'])
    row.extend(top_sim_users_ratings)
    row.extend(top_sim_movies_ratings)
    try:
        row.append(sample_train_averages['user'][user])
    except KeyError:
        row.append(sample_train_averages['global'])

    try:
        row.append(sample_train_averages['movie'][movie])
    except KeyError:
        row.append(sample_train_averages['global'])
    return row

def calculate_predictions(m_list):
    pred_list = []
    for movie_id in m_list:
        vec = get_vector(movie_id)
        vec.append(get_ratings(bsl.test([(user,movie_id,0)]))[1][0])
        vec.append(get_ratings(svd.test([(user,movie_id,0)]))[1][0])
        vec.append(get_ratings(svdpp.test([(user,movie_id,0)]))[1][0])
        # pred_list.append((xgb_final.predict([vec],validate_features=False)[0],movie_id))
        pred_list.append((rf.predict([vec])[0],movie_id))

    pred_list.sort()
    return pred_list

        
user = 130172

rating_dict = {}
predicted_rating = {}
actual_rating = {}
liked_movies = [-1]

sample_train_sparse_matrix = sparse.load_npz("./data/sample_train_sparse_matrix.npz")

rated_movies = sample_train_sparse_matrix[user].nonzero()[1]
rating = sample_train_sparse_matrix[user].toarray()[0][rated_movies]

sample_train_averages = dict()
global_average = sample_train_sparse_matrix.sum()/sample_train_sparse_matrix.count_nonzero()
sample_train_averages['global'] = global_average
sample_train_averages['user'] = get_average_ratings(sample_train_sparse_matrix, of_users=True)
sample_train_averages['movie'] =  get_average_ratings(sample_train_sparse_matrix, of_users=False)

with open("./data/similar_movies.pickle", 'rb') as handle:
    similar_movies = pickle.load(handle)

with open("./data/sorted_movies.pickle", 'rb') as handle:
    sorted_movies = pickle.load(handle)

movie_df = pd.read_csv("./data/Movies.csv",index_col=["movie_id"])
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

movie_list = pd.read_csv('./data/sample_movies.csv')
movie_list = np.array(movie_list.iloc[:,0])

user_list = pd.read_csv('./data/sample_users.csv')
user_list = np.array(user_list.iloc[:,0])