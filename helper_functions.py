import colorama
import movie_storage_sql as storage





def check_movie_title_is_in_db(movie_title, movie_should_exist):
    """
    Checks if a movie exists in the list of movies.
    :param movie_title: title of the movie to check
    :param movie_should_exist: if True, the error message appears for not existing movie.
    If False, the error message appears for existing movie.
    """
    if movie_title == "":
        raise ValueError(f"{colorama.Fore.RED}Empty string for the movie title are not allowed.")

    movies_list = storage.list_movies()
    movie_is_found = find_key_in_movie(movies_list, "title", movie_title)

    if movie_should_exist and not movie_is_found:
        raise ValueError(f"{colorama.Fore.RED}Movie {movie_title} doesn't exist.")
    if not movie_should_exist and movie_is_found:
        raise ValueError(f"{colorama.Fore.RED}Movie {movie_title} already exists.")


def find_key_in_movie(movies_list, key, value):
    """
    Finds if a key with given value is in the  list of movies.
    :param movies_list: list with movies as dictionaries
    :param key: key for searching a given value in the movies
    :param value: value which should be found in the movies under the given key
    :return: Flag True if the value was found, index of a movie
    """
    for movie in movies_list:
        if value == movie[key]:
            value_is_found = True
            return value_is_found
    return False


def sort_movies_by(movies_list, filter_text, reverse_list=True):
    """
    Sorts the list of movies according to the filter text.
    :param reverse_list: If False, sort ascending. Default is True (sort descending).
    :param movies_list: list with movies as dictionaries
    :param filter_text: text to be used as a filter to sort movies.
    The text is equal to a key in a movie dictionary.
    :return: movies list sorted by a defined key
    """
    for movie in movies_list:
        if filter_text not in movie.keys():
            print(f"The key to sort  {filter_text} is not in the dictionary!")
            return None

    sorted_movies_list = sorted(movies_list,
                                key=lambda movie_item: movie_item[filter_text],
                                reverse=reverse_list)
    return sorted_movies_list


def calculate_median(values_list):
    """
    Display median rating value for movies in the list.
    :param values_list: values for median rating calculation
    """

    values_list.sort()  # calculate median

    if len(values_list) % 2 == 0:
        median = (values_list[len(values_list) // 2] + values_list[len(values_list) // 2 - 1]) / 2
    else:
        median = values_list[len(values_list) // 2]
    print(f"Median rating: {colorama.Fore.CYAN}{median}{colorama.Fore.RESET}")


def print_best_and_worst_movie(movies_sorted_by_rating):
    """
    Display the best and the worst movie.
    :param movies_sorted_by_rating: list of movies as dictionaries, which are sorted by rating.
    """
    best_movie = movies_sorted_by_rating[0]
    worst_movie = movies_sorted_by_rating[-1]

    print(f"Best movie: {best_movie['title']}, {colorama.Fore.CYAN}{best_movie['rating']}")
    print(f"Worst movie: {worst_movie['title']}, {colorama.Fore.CYAN}{worst_movie['rating']}")


def get_rating_list(movies_list):
    """
    Extracts rating from a list of movies.
    :param movies_list: list of dictionaries (movies)
    :return: list with rating of all movies
    """
    sum_rating = 0
    rating_list = []

    for movie in movies_list:
        sum_rating += movie["rating"]
        rating_list.append(movie["rating"])
    return rating_list


def calculate_and_print_average(rating_list):
    """
    Calculates and displays the average rating of movies in the list.
    :param rating_list: list with rating of all movies
    """
    average = sum(rating_list) / len(rating_list)
    print(f"Average rating: {colorama.Fore.CYAN}{average:.1f}")


def search_movie_with_suggestions(part_of_title, movies_list):
    """
    Searches for a movie and does title suggestions if the movie was not entered exactly.
    :param movies_list: list of dictionaries (movies)
    :param part_of_title: title of the movie to search
    :return: tuple with user input and boolean indicating if the movie was found
    """
    suggestions = []
    # no need on fuzzy logic if a part of a title is in the movie title
    # this step is also important, because the leverstein similarity not always
    # overlays with the human feeling of a similarity
    for movie in movies_list:
        if part_of_title.lower() in movie["title"].lower():
            suggestions.append(movie)

    return suggestions


def print_sorted_movies(sorted_movies_list):
    """
    Print the sorted list of movies.
    :param sorted_movies_list: movies list sorted by some criteria
    """
    for movie in sorted_movies_list:
        title = movie["title"]
        rating = movie["rating"]
        year = movie["year"]
        print(f"{colorama.Style.BRIGHT}"
              f"{title} ({year})"
              f"{colorama.Style.RESET_ALL}: "
              f"{colorama.Fore.CYAN}"
              f"{rating}")
