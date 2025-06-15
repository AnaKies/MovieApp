# Animal Project

This project consists of a back-end system that interacts with a SQL database to retrieve and store data using the SQLAlchemy library. 
It also integrates with an API to fetch movie information. 
The system dynamically generates an HTML web page, populating it with visualized data retrieved from the SQL database.
The following API is used to handle the movie data: https://www.omdbapi.com/

## Installation

To install this project, simply clone the repository from https://github.com/AnaKies/MovieApp.git
Install the dependencies in requirements.txt using `pip install -r requirements.txt`

## Usage

To use this project, run the following command - `python main.py`.
The script prints the name of the HTML file to the console, which should be opened in a browser to view the result.
The generated HTML file is located in the project root. 
If the API key is expired, go to https://www.omdbapi.com/ sign up and request your own API key. 
Create your environment folder .env and put there the key in the variable API_KEY.

## Contributing

This is a personal educational project created for learning purposes.  
Contributions are not expected, but if you have suggestions or notice any issues, feel free to open an issue or submit a pull request.
