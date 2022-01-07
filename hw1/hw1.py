# Python program to demonstrate
# defaultsect
from collections import defaultdict


# HW1
# @author by Tianle Chen tc822  & Yuchen Zhao yz1116

# a function takes in a ratings file, and returns a dictionary.
# The dictionary should have movie as key.
# The corresponding list of ratings as value.
def read_ratings_data(f):
    ratings_data = {}
    for line in open(f):
        movie, rates, user_id = line.split('|')
        if movie not in ratings_data:
            ratings_data[movie.strip()] = []
        ratings_data[movie.strip()].append(float(rates))
    return ratings_data


# a function that takes in a movies file and returns a dictionary.
# The dictionary should have a one-to-one mapping between movie and genre.
def read_movie_genre(f):
    movie_genre = {}
    for line in open(f):
        genre_movie, movie_id, movie = line.split('|')
        movie_genre[movie.strip()] = genre_movie.strip()
    return movie_genre


# a function that takes as a parameter a movie-to-genre dictionary.
# the function return a dictionary in which a genre is mapped to all the movies in that genre.
def create_genre_dict(d):
    genre_dict = {}
    for key, val in d.items():
        if val not in genre_dict:
            genre_dict[val] = []
        genre_dict[val].append(key)
    return genre_dict


# a function that takes as a parameter a ratings dictionary.
# it return a dictionary where the movie is mapped to its average rating computed from the ratings list.
def calculate_average_rating(d):
    average_rating = {}
    for key, val in d.items():
        average_rating[key] = round(sum(val) / float(len(val)), 2)
    return average_rating


# a function that takes as parameters a dictionary of movie-to-average rating.
# it return a dictionary of top n(10) movies based on the average ratings.
def get_popular_movies(d, n):
    popular_movies = dict(sorted(d.items(), key=lambda key: key[1], reverse=True))
    # n = 10
    if len(d.values()) > n:
        return popular_movies[:n]
    else:
        return popular_movies


# a function filter_movies that takes as parameters a dictionary of movie-to-average rating.
# it should filter movies based on the threshold rating, and return a dictionary with same structure as the input.
def filter_movies(d, t):
    # t = 3  # threshold
    filterMovies = dict((key, val) for key, val in d.items() if val >= t)
    return filterMovies


# a function that given a genre, a genre-to-movies dictionary, a dictionary of movie:average rating,
# an integer n (default 5), returns the top n most popular movies in that genre based on the average ratings.
# the return value is a dictionary of movie-to-average rating of movies that make the cut.
def get_popular_in_genre(g, genre_dict, average_dict, n):
    popular_in_genre = {}
    if g in genre_dict:
        pg = {g: genre_dict[g]}
    for key in pg.values():
        for i in range(len(key)):
            popular_in_genre[key[i]] = average_dict[key[i]]
    if len(popular_in_genre) > n:
        return get_popular_movies(popular_in_genre, len(popular_in_genre))[:n]
    else:
        return get_popular_movies(popular_in_genre, len(popular_in_genre))


# a function that takes given a genre, a genre-to-movies dictionary, a dictionary of movie:average rating,
# returns the average rating of the movies in the given genre.
def get_genre_rating(g, genre_dict, average_dict):
    j = 0
    if g in genre_dict:
        pg = {g: genre_dict[g]}
    for key in pg.values():
        for i in range(len(key)):
            j += average_dict[key[i]]
    return round(j / len(key), 2)


# a function that takes as parameters a genre-to-movies dictionary, a movie-to-average
# rating dictionary, and n, and returns the top-n rated genres as a dictionary of genre:average rating.
def genre_popularity(genre_dict, average_dict, n):
    genre_popular = {}
    for key in genre_dict:
        if key not in genre_popular:
            genre_popular[key] = get_genre_rating(key, genre_dict, average_dict)
    if len(genre_popular) > n:
        return get_popular_movies(genre_popular, len(genre_popular))[:n]
    else:
        return get_popular_movies(genre_popular)


# a function that take ratings file as the parameter.
# return a user-to-movies dictionary that maps user ID to the associated movies and the corresponding ratings.
def read_user_ratings(f):
    user_ratings = defaultdict(list)
    for line in open(f):
        movie, rates, user_id = line.split('|')
        val = tuple((movie.strip(), float(rates.strip())))
        user_ratings[user_id.strip()].append(val)
    return dict(user_ratings)


# a function that takes as parameters a user id, the user-to-movies dictionary, and the movie-to-genre dictionary,
# and returns the top genre that the user likes based on the user's ratings.
def get_user_genre(uid, user_rates, movie_genre):
    user_genre_rates = {}
    max_avg = 0
    if str(uid) in user_rates:
        m = user_rates[str(uid)]
        for i in range(len(m)):
            if m[i][0] in movie_genre and movie_genre[m[i][0]] not in user_genre_rates:
                user_genre_rates[movie_genre[m[i][0]]] = []
            user_genre_rates[movie_genre[m[i][0]]].append(m[i][1])
        for key in user_genre_rates:
            user_genre_rates[key] = sum(user_genre_rates[key]) / len(user_genre_rates[key])
            if user_genre_rates[key] > max_avg:
                genre = key
                max_avg = user_genre_rates[key]
    return genre


# a function that takes a parameters a user id, the user-to-movies dictionary,
# the movie-to-genre dictionary, and the movie-to-average rating dictionary.
# The function should return a dictionary of movie-to-average rating.
def recommend_movies(uid, user_to_movies, movie_to_genre, movie_to_average):
    top_genre = get_user_genre(uid, user_to_movies, movie_to_genre)
    movie_name = []
    popular_in_genre = {}
    rated_movie = []
    uid = str(uid)
    if uid in user_to_movies and top_genre in create_genre_dict(read_movie_genre()):
        for i in range(len(user_to_movies[uid])):
            rated_movie.append(user_to_movies[uid][i][0])
        pg = list(create_genre_dict(read_movie_genre())[top_genre])
    for key in pg:
        if key not in rated_movie:
            movie_name.append(key)
            popular_in_genre[key] = movie_to_average[key]
    if len(movie_name) > 3:
        return get_popular_movies(popular_in_genre)[:3]
    else:
        return get_popular_movies(popular_in_genre)



print(read_ratings_data('movieRatingSample.txt'))  # 1.1
print(read_movie_genre('genreMovieSample.txt'))  # 1.2
print(create_genre_dict(read_movie_genre('genreMovieSample.txt')))  # 2.1
print(calculate_average_rating(read_ratings_data('movieRatingSample.txt')))  # 2.2
print(get_popular_movies(calculate_average_rating(read_ratings_data('movieRatingSample.txt'))))  # 3.1
print(filter_movies(calculate_average_rating(read_ratings_data('movieRatingSample.txt'))))  # 3.2
print(
    get_popular_in_genre('Comedy', create_genre_dict(read_movie_genre('genreMovieSample.txt')),
                         calculate_average_rating(read_ratings_data('movieRatingSample.txt')), 5))  # 3.3
print(get_genre_rating('Comedy', create_genre_dict(read_movie_genre('genreMovieSample.txt')),
                       calculate_average_rating(read_ratings_data('movieRatingSample.txt'))))  # 3.4
print(genre_popularity(create_genre_dict(read_movie_genre('genreMovieSample.txt')),
                       calculate_average_rating(read_ratings_data('movieRatingSample.txt')), 5))  # 3.5
print(read_user_ratings('movieRatingSample.txt'))  # 4.1
print(get_user_genre(1, read_user_ratings('movieRatingSample.txt'), read_movie_genre('genreMovieSample.txt')))  # 4.2
print(recommend_movies(1, read_user_ratings('movieRatingSample.txt'), read_movie_genre('genreMovieSample.txt'),
                       calculate_average_rating(read_ratings_data('movieRatingSample.txt')), ))  # 4.3