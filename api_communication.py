import os
import requests
from dotenv import load_dotenv

# load variables (API-key) from the environment into the script
load_dotenv()

HTTP_CODE_OK = 200
API_KEY = os.getenv('API_KEY')
API_URL = 'http://www.omdbapi.com/?'



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

        title = response_json.get('Title')
        year = response_json.get('Year')
        image_url = response_json.get('Poster')
        ratings = response_json.get('Ratings')

        return title, year, ratings, image_url
    except Exception:
        raise Exception("Could not connect to OMDb API.")

