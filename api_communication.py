import os
import requests
from dotenv import load_dotenv

# load variables (API-key) from the environment into the script
load_dotenv()

HTTP_CODE_OK = 200
API_KEY = os.getenv('API_KEY')
API_URL = 'http://www.omdbapi.com/?'


def get_movie_data_from_api(movie_title):
    url = f"{API_URL}apikey={API_KEY}&t={movie_title}"

    response = requests.get(url)
    if response.status_code != HTTP_CODE_OK:
        return None, None, None
    response_json = response.json()

    title = response_json.get('Title')
    year = response_json.get('Year')
    ratings = response_json.get('Ratings')
    # use the rating data only from the first source "Internet Movie Database"
    rating_from_internet_movies = ratings[0]['Value']
    # The "Internet Movie Database" has the original rating in this form "7.6/10"
    if '/' not in rating_from_internet_movies:
        return None, None, None
    formatted_rating = rating_from_internet_movies.split('/')[0]
    return title, year, formatted_rating
