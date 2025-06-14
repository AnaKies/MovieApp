import os
import requests
from dotenv import load_dotenv

# load variables (API-key) from the environment into the script
load_dotenv()

HTTP_CODE_OK = 200
API_KEY = os.getenv('API_KEY')
API_URL = 'http://www.omdbapi.com/?'
title = 'Inception'

url = f"{API_URL}apikey={API_KEY}&t={title}"

response = requests.get(url)
if response.status_code == HTTP_CODE_OK:
    response_json = response.json()
    print(response_json)
