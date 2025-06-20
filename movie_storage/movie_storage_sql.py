from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
# echo=True tells SQLAlchemy to print all SQL statements it runs
engine = create_engine(DB_URL)

def connect_to_sql_db():
    """
    Establish connection to the SQL database.
    """
    try:
        # Create the movies table if it does not exist
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT UNIQUE NOT NULL,
                    year INTEGER NOT NULL,
                    rating REAL NOT NULL,
                    poster_url TEXT NOT NULL)
            """))
            conn.commit()
    except Exception:
        raise Exception("Could not connect to SQL database.")

def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("""SELECT 
                                                title, 
                                                year, 
                                                rating, 
                                                poster_url 
                                            FROM movies"""))
        movies = result.fetchall()

    return [{"title": row[0],
             "year": row[1],
             "rating": row[2],
             "poster_url": row[3]} for row in movies]

def add_movie(title, year, rating, poster_url):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            query = """INSERT INTO movies (title, year, rating, poster_url) 
                       VALUES (:title, :year, :rating, :poster_url)"""
            connection.execute(text(query),
            {"title": title, "year": year, "rating": rating, "poster_url": poster_url})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")

def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            query = """DELETE FROM movies
                        WHERE title = :title"""
            connection.execute(text(query),
                               {"title": title})
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")

def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            query = """UPDATE movies
            SET 
                rating = :rating
            WHERE movies.title = :title"""
            connection.execute(text(query),
                               {"title": title, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
