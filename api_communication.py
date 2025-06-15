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
        return None, None, None, None
    response_json = response.json()
    title = response_json.get('Title')
    year = response_json.get('Year')
    image_url = response_json.get('Poster')
    ratings = response_json.get('Ratings')
    return title, year, ratings, image_url
