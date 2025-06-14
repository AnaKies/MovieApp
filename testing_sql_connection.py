from movie_storage_sql import add_movie, list_movies, delete_movie, update_movie

movie_name = 'Santa Barbara'
# Test adding a movie
add_movie(movie_name, 2010, 8.8)

# Test listing movies
movies = list_movies()
print(movies)

# Test updating a movie's rating
update_movie(movie_name, 99.0)
print(list_movies())

# Test deleting a movie
delete_movie(movie_name)
print(list_movies())  # Should be empty if it was the only movie