from datetime import datetime
import random
import colorama
import matplotlib.pyplot as plt
from rapidfuzz import fuzz
import movie_storage_sql as storage
import api_communication as api
import html_handler
import helper_functions as helper


SIMILARITY_THRESHOLD_PERCENTAGE = 50


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
        # _ignore poster_url
        title, year, rating, _ = movie.values()
        print(f"{colorama.Style.BRIGHT}{title} ({year}): {colorama.Fore.CYAN}{rating}")


def add_new_movie():
    """
    Adds new movie to the list.
    """
    try:
        movie_title = input(f"{colorama.Fore.MAGENTA}Enter new movie title: ")
        title, year, rating, image_url = api.get_movie_data_from_api(movie_title)
        if not title:
            raise ValueError(f"Movie title '{movie_title}' is unknown.")
        helper.check_movie_title_is_in_db(movie_title, movie_should_exist = False)
        storage.add_movie(title, year, rating, image_url)
    except (ValueError, TypeError) as error:
        print(f"{colorama.Fore.RED}Error in movie title: {error}")
    except Exception as error:
        print(f"{colorama.Fore.RED}Error adding movie: {error}")


def delete_movie():
    """
    Delete movie from the list by their title.
    """
    while True:
        try:
            movie_title = input(f"{colorama.Fore.MAGENTA}Enter movie title to delete: ")
            helper.check_movie_title_is_in_db(movie_title, movie_should_exist = True)
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
            helper.check_movie_title_is_in_db(movie_title, movie_should_exist = True)
            break
        except (ValueError, TypeError) as error:
            print(f"{colorama.Fore.RED}Error in movie title: {error}")

    while True:
        try:
            user_rating = api.get_user_rating()
            break
        except ValueError as error:
            print(error)

    storage.update_movie(movie_title, user_rating)


def evaluate_stat():
    """
    Display statistical data: average rating, median rating, the best movie, worst movie.
    """
    movies_list = storage.list_movies()
    rating_list = helper.get_rating_list(movies_list)
    helper.calculate_and_print_average(rating_list)
    helper.calculate_median(rating_list)
    sorted_movies_list_by_rating = helper.sort_movies_by(movies_list, "rating")

    if sorted_movies_list_by_rating is not None:
        helper.print_best_and_worst_movie(sorted_movies_list_by_rating)


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


def search_movie():
    """
    Search an input movie in the given list.
    If no matching, display the suggestions form the movies list.
    """
    users_movie_input = input(f"{colorama.Fore.MAGENTA}Enter part of movie title: ")
    movies_list = storage.list_movies()

    # first check if the part of a title is in the movies titles
    suggestions = helper.search_movie_with_suggestions(users_movie_input, movies_list)
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


def sort_movies_by_rating():
    """
    Sorts the list of movies according to the rating.
    """
    movies_list = storage.list_movies()
    sorted_movies_by_rating = helper.sort_movies_by(movies_list, "rating")
    helper.print_sorted_movies(sorted_movies_by_rating)


def sort_movies_by_year():
    """
    Sorts the list of movies according to the year.
    """
    movies_list = storage.list_movies()

    latest_movie_first_string = input("Do you want the latest movie first? (Y/N): ")
    if "y" in latest_movie_first_string.lower():
        sorted_movies_by_rating = helper.sort_movies_by(movies_list, "year", reverse_list=True)
        helper.print_sorted_movies(sorted_movies_by_rating)
    elif "n" in latest_movie_first_string.lower():
        sorted_movies_by_rating = helper.sort_movies_by(movies_list, "year", reverse_list=False)
        helper.print_sorted_movies(sorted_movies_by_rating)


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


def generate_website():
    """
    Generate a website from the movies in database.
    """
    html_file_name = 'index.html'
    serialized_movies = html_handler.serialise_all_movies()
    html_template = html_handler.get_template()
    template_filled_with_title = html_handler.insert_movie_data_into_html_template(
        html_template, '__TEMPLATE_TITLE__', 'Movie App of Anastasia')
    filled_template = html_handler.insert_movie_data_into_html_template(
        template_filled_with_title, '__TEMPLATE_MOVIE_GRID__', serialized_movies)
    html_handler.create_html_file(html_file_name, filled_template)
    print(f"Website {html_file_name} is created.")


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
12. Generate website
    """)


def process_menu_choice(menu_cmd):
    """
    Calls a function according to the menu choice.
    :param menu_cmd: menu command
    """
    try:
        # offset 1 because the command for exit is managed separately
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
        search_movie,
        sort_movies_by_rating,
        sort_movies_by_year,
        create_histogram,
        filter_movies,
        generate_website
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
                            f"Enter choice (1-12): ")
        if user_choice == "0":  # a possibility to stop the infinite loop
            print("Bye!")
            break
        process_menu_choice(user_choice)
        input("\nPress enter to continue")


if __name__ == "__main__":
    main()
