import os
import colorama
import requests
from dotenv import load_dotenv


# load variables (API-key) from the environment into the script
load_dotenv()

HTTP_CODE_OK = 200
API_KEY = os.getenv('API_KEY')
API_URL = 'http://www.omdbapi.com/?'
RATING_MAX = 10


def get_movie_data_from_api(movie_title):
    """
    Fetches movie data from API.
    :param movie_title: Part of the title.
    :return: A tuple (title, year, movie ratings and url to the poster).
    """
    # protect the API key from the injection using parameters
    parameters = {
        'apikey': API_KEY,
        't': movie_title
    }
    try:
        response = requests.get(API_URL, params = parameters, timeout=10)
        response_json = response.json()

        raw_year = response_json.get('Year')
        year = get_year(raw_year)
        title = response_json.get('Title')
        image_url = response_json.get('Poster')
        multiple_ratings = response_json.get('Ratings')
        rating = get_rating(multiple_ratings, title)

        return title, year, rating, image_url
    except Exception:
        raise Exception(f"{colorama.Fore.RED}Could not connect to OMDb API.")


def get_year(raw_year):
    """
    Extracts the year from the JSON formatted response.
    If the year is not in the valid format, asks the user th enter the year manually.
    :param raw_year: Year data  as string directly from the API
    :return: Formatted year as an integer.
    """
    try:
        year = int(raw_year)
    except Exception:
        # For example there are movies with 2013-2017
        print(f"{colorama.Fore.RED}Year of the movie is not valid: {raw_year}.")
        while True:
            try:
                year = int(input(f"{colorama.Fore.MAGENTA}Enter the year of the movie manually: "))
                break
            except ValueError:
                print(f"{colorama.Fore.RED}Invalid year.")
    return year


def get_rating(multiple_ratings, title):
    """
    Get the rating from the JSON formatted response.
    If there are more than one rating, the user should enter the rating manually.
    :param multiple_ratings: List of multiple ratings.
    :param title: Movie title.
    :return: Single rating as float.
    """
    if len(multiple_ratings) == 1:
        raw_rating = multiple_ratings[0]['Value']
        user_rating = raw_rating.split('/')[0]
        try:
            user_rating = float(user_rating)
            return user_rating
        except ValueError:
            print(f"{colorama.Fore.RED}The rating of {title} is not valid.")
    elif len(multiple_ratings) > 1:
        print(f"Different sources rate the movie {title} at: ")
        for source in multiple_ratings:
            print(f"{source['Value']}")
    elif len(multiple_ratings) == 0:
        print(f"{colorama.Fore.RED}The movie {title} has no rating.")
    user_rating = get_user_rating()
    return user_rating


def get_user_rating():
    """
    Converts the user rating to float and validates the user's rating.
    :return: User rating as a float.
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
