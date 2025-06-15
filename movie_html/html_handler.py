from movie_storage import movie_storage_sql as storage


def serialize_movie(movie):
    """
    Serialize a movie into HTML formatted string.
    :param movie: movie to serialize
    :return: HTML formatted string with movie data
    """
    # _ means ignore rating
    title, year, _, poster_url = movie.values()
    serialized_movie = ("<li>\n"
                        "<div class='movie'>\n"
                        "<img class='movie-poster'\n"
                        f"src='{poster_url}'/>\n"
                        f"<div class='movie-title'>{title}</div>\n"
                        f"<div class='movie-year'>{year}</div>\n"
                        f"</div>\n"
                        f"</li>\n")
    return serialized_movie


def serialise_all_movies():
    """
    Serialize all movie data to the HTML.
    :return: String with the serialized movie data.
    """
    all_movies_data = storage.list_movies()
    serialized_movies = ""

    for movie in all_movies_data:
        serialized_movies += serialize_movie(movie)

    return serialized_movies


def get_template():
    """
    Reads the content of the template HTML file.
    :return: Content of the template HTML file.
    """
    file_name = "static/index_template.html"
    try:
        with open(file_name, "r", encoding="utf-8") as html_file:
            html_template = html_file.read()
            return html_template

    except FileNotFoundError as error:
        print(f"Error: File {file_name} is not found.\n{error}")
    except Exception as error:
        print(f"Error: Unexpected error at reading {file_name}.\n{error}")
    return None


def insert_movie_data_into_html_template(html_template, placeholder, insert_data):
    """
    Replaces HTML content with new text.
    :param placeholder: Placeholder text to be replaced.
    :param html_template: HTML template with placeholders for data
    :param insert_data: HTML formatted string
    :return: Filled HTML template as string.
    """
    if placeholder not in html_template:
        raise Exception("Error: the "
                        f"{placeholder} "
                        "is not in the template.")

    filled_template = html_template.replace(placeholder, insert_data)

    return filled_template


def create_html_file(file_name, html_content):
    """
    Writes the content of the HTML file to the HTML file.
    :param file_name: Name of the HTML file.
    :param html_content: HTML content of the HTML file as string.
    :return: None
    """
    try:
        # use encoding for correct representation of
        # such special symbols like an apostrophe
        with open(file_name, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)

    except FileNotFoundError as error:
        print(f"Error: File {file_name} is not found.\n{error}")
    except Exception as error:
        print(f"Error: Unexpected error at writing {file_name}.\n{error}")
