from datetime import datetime
import random
import colorama
import matplotlib.pyplot as plt
from rapidfuzz import fuzz
import movie_storage_sql as storage
import api_communication as api


SIMILARITY_THRESHOLD_PERCENTAGE = 50
RATING_MAX = 10



def list_all_movies():
    """
    Prints all movies in the list.
    """
    movies_list = storage.list_movies()

    if movies_list is None:
        print(f"{colorama.Fore.RED} Not possible to list the empty list.")
        return

    amount_of_movies = len(movies_list)
    print(f"{amount_of_movies} movies in total")

    for movie in movies_list:
        title, year, rating = movie.values()
        print(f"{colorama.Style.BRIGHT}{title} ({year}): {colorama.Fore.CYAN}{rating}")


def filter_movies():
    """
    Prints the movies from the year range and above minimum rating.
    """
    minimum_rating = ""
    start_year = ""
    end_year = ""
    try:
        minimum_rating = input("Enter minimum rating (leave blank for no minimum rating): ")
        if minimum_rating != "":
            minimum_rating = float(minimum_rating)
        else:
            minimum_rating = 0

        start_year = input("Enter start year (leave blank for no start year): ")
        if start_year != "":
            start_year = int(start_year)
        else:
            start_year = 0

        end_year = input("Enter end year (leave blank for no end year): ")
        if end_year != "":
            end_year = int(end_year)
        else:
            end_year = datetime.today().year
    except (ValueError, TypeError) as error:
        print(f"{colorama.Fore.RED}Value should be a number: {error}")

    movies_list = storage.list_movies()

    for movie in movies_list:
        if movie["rating"] >= minimum_rating and start_year <= movie["year"] <= end_year:
            print(f"{colorama.Style.BRIGHT}"
                  f"{movie['title']} "
                  f"({movie['year']}): "
                  f"{colorama.Fore.CYAN}"
                  f"{movie['rating']}")


def add_new_movie():
    """
    Adds new movie to the list.
    """
    try:
        movie_title = input(f"{colorama.Fore.MAGENTA}Enter new movie title: ")
        title, year, ratings, image_url = api.get_movie_data_from_api(movie_title)
        if not title:
            raise ValueError(f"Movie title '{movie_title}' is unknown.")
        check_movie_title_is_in_db(movie_title, movie_should_exist = False)
        if ratings:
            print(f"Different sources rate the movie {title} at: ")
            for source in ratings:
                print(f"{source['Value']}")
        user_rating = get_user_rating()
        storage.add_movie(title, year, user_rating, image_url)
    except (ValueError, TypeError) as error:
        print(f"{colorama.Fore.RED}Error in movie title: {error}")
    except Exception as error:
        print(f"{colorama.Fore.RED}Error adding movie: {error}")


def get_user_rating():
    """
    Converts the user rating to float and validates the user's rating.
    :return:
    """
    while True:
        user_rating = input(f"{colorama.Fore.MAGENTA}Enter your rating value: ")
        try:
            rating = float(user_rating)
            if not 0 <= rating <= RATING_MAX:
                raise ValueError(f"{colorama.Fore.RED}The rating should be in the range 0 ... 10.")
            return rating
        except Exception:
            raise ValueError(f"{colorama.Fore.RED}Rating value must be a number!")


def delete_movie():
    """
    Delete movie from the list by their title.
    """
    while True:
        try:
            movie_title = input(f"{colorama.Fore.MAGENTA}Enter movie title to delete: ")
            check_movie_title_is_in_db(movie_title, movie_should_exist = True)
            break
        except (ValueError, TypeError) as error:
            print(f"{colorama.Fore.RED}Error in movie title: {error}")

    storage.delete_movie(movie_title)


def update_movie_rating():
    """
    Update rating of a movie to the new one.
    """
    while True:
        try:
            movie_title = input(f"{colorama.Fore.MAGENTA}Enter existing movie title: ")
            check_movie_title_is_in_db(movie_title, movie_should_exist = True)
            break
        except (ValueError, TypeError) as error:
            print(f"{colorama.Fore.RED}Error in movie title: {error}")

    while True:
        try:
            user_rating = get_user_rating()
            break
        except ValueError as error:
            print(error)

    storage.update_movie(movie_title, user_rating)


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


def evaluate_stat():
    """
    Display statistical data: average rating, median rating, the best movie, worst movie.
    """
    movies_list = storage.list_movies()
    rating_list = get_rating_list(movies_list)
    calculate_and_print_average(rating_list)
    calculate_median(rating_list)
    sorted_movies_list_by_rating = sort_movies_by(movies_list, "rating")

    if sorted_movies_list_by_rating is not None:
        print_best_and_worst_movie(sorted_movies_list_by_rating)


def generate_random_movie():
    """
    Generates and prints a movie suggestions from the movie list.
    """
    movies_list = storage.list_movies()
    generated_movie = random.choice(movies_list)
    title = generated_movie["title"]
    rating = generated_movie["rating"]
    print(f"Your movie for tonight: "
          f"{colorama.Fore.CYAN}"
          f"{title}"
          f"{colorama.Fore.RESET}, "
          f"it's rated {rating}")


def search_movie(part_of_title, movies_list):
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
        if not filter_text.lower() in movie.keys():
            print(f"The key to sort  {filter_text} is not in the dictionary!")
            return None

    sorted_movies_list = sorted(movies_list,
                                key=lambda movie_item: movie_item[filter_text],
                                reverse=reverse_list)
    return sorted_movies_list


def sort_movies_by_rating():
    """
    Sorts the list of movies according to the rating.
    """
    movies_list = storage.list_movies()
    sorted_movies_by_rating = sort_movies_by(movies_list, "rating")
    print_sorted_movies(sorted_movies_by_rating)


def sort_movies_by_year():
    """
    Sorts the list of movies according to the year.
    """
    movies_list = storage.list_movies()

    latest_movie_first_string = input("Do you want the latest movie first? (Y/N): ")
    if "y" in latest_movie_first_string.lower():
        sorted_movies_by_rating = sort_movies_by(movies_list, "year", reverse_list=True)
        print_sorted_movies(sorted_movies_by_rating)
    elif "n" in latest_movie_first_string.lower():
        sorted_movies_by_rating = sort_movies_by(movies_list, "year", reverse_list=False)
        print_sorted_movies(sorted_movies_by_rating)


def create_histogram():
    """
    Generate a histogram: X movie rating, Y amount of movies with a specific rating.
    """
    movies_list = storage.list_movies()
    rating_list = []
    for movie in movies_list:
        rating_list.append(movie["rating"])

    # bins are number of groups of data
    plt.hist(rating_list, bins=30, edgecolor='black')
    plt.xlabel("Rating")
    plt.ylabel("Movies frequency")
    plt.title("Movie Rating Histogram")
    hist_file_title = input(f"{colorama.Fore.MAGENTA}"
                           f"Enter file title for saving the histogram (without extension): ")
    plt.savefig(hist_file_title + ".png")
    print(f"{colorama.Fore.MAGENTA}"
          f"The histogram was saved to the file {hist_file_title}.png")


def find_movie_or_do_suggestions():
    """
    Search an input movie in the given list.
    If no matching, display the suggestions form the movies list.
    """
    users_movie_input = input(f"{colorama.Fore.MAGENTA}Enter part of movie title: ")
    movies_list = storage.list_movies()

    # first check if the part of a title is in the movies titles
    suggestions = search_movie(users_movie_input, movies_list)
    if suggestions:
        for suggestion_movie in suggestions:
            print(f"{colorama.Fore.RED}Did you mean: {suggestion_movie['title']}")
        return

    # then do the leverstein comparison
    similarity_is_found = False
    for movie in movies_list:
        similarity_ratio = fuzz.ratio(users_movie_input, movie["title"])

        if similarity_ratio > SIMILARITY_THRESHOLD_PERCENTAGE:
            similarity_is_found = True
            print(f"{colorama.Fore.RED}Did you mean: {movie['title']}")

    if not similarity_is_found:
        print(f"{colorama.Fore.RED}No match for {users_movie_input}.")


def display_menu():
    """
    Prints the menu items.
    """
    print(colorama.Fore.BLUE + "Menu:" + colorama.Fore.RESET + """
0. Exit
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Movies sorted by year
10. Create Rating Histogram
11. Filter movies
    """)


def process_menu_choice(menu_cmd):
    """
    Calls a function according to the menu choice.
    :param menu_cmd: menu command
    """
    try:
        # offset 1 because the command for exit is managed separatly
        command = int(menu_cmd) - 1
    except (ValueError, TypeError):
        print(colorama.Fore.RED + f"Command {menu_cmd} was not a number!")
        return

    func_list = [
        list_all_movies,
        add_new_movie,
        delete_movie,
        update_movie_rating,
        evaluate_stat,
        generate_random_movie,
        find_movie_or_do_suggestions,
        sort_movies_by_rating,
        sort_movies_by_year,
        create_histogram,
        filter_movies
    ]

    if command > len(func_list):
        print(colorama.Fore.RED + "Not supported number for a command!")
        return
    func_list[command]()


def main():
    """
    Function entry point.
    """
    # Initialise the color module. Automatic reset of a color style in a new line of string.
    colorama.init(autoreset=True)
    storage.connect_to_sql_db()

    print(colorama.Back.MAGENTA + "********** My Movies Database **********\n")
    while True:
        display_menu()
        user_choice = input(f"{colorama.Fore.MAGENTA}"
                            f"Enter choice (1-11): ")
        if user_choice == "0":  # a possibility to stop the infinite loop
            print("Bye!")
            break
        process_menu_choice(user_choice)
        input("\nPress enter to continue")


if __name__ == "__main__":
    main()
