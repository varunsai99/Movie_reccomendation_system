# Movie reccomendation system

*Data Overview*
  1. There are nearly 100 million data points int the dataset(these are all the rating given by users for a particular movie).
  2. Number of unique users are 480,189
  3. Number of unique movies are 17,770

*About Project* 
  1. Here I have used machine learning concepts like item-item i.e movie-movie simiarity between the movies to find top 50 similar movies for every movie in the data. This data is stored in similar_movies.pickle file. We can give this movies as reccomendations. 
  2. In order to perform user-user similarity there are so many members so it is not feasible to perform using low compute power.
  3. So I sampled some points and apply several machine learning algorithms like Matrix factorization like SVD,SVD++ on this sampled data to get users preference on the movies.
  4. We can sort those ratings and can give those movies as reccomendations. 
  5. I have used Flask to create User interface for this project.
