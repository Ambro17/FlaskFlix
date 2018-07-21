import os
import sqlite3

import tmdbsimple as tmdb
from flask import Flask, render_template
from constantes import TMDB_KEY
app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'db')
db_connection = sqlite3.connect(os.path.join(DB_PATH, 'movies.db'), check_same_thread=False)
db_cursor = db_connection.cursor()

# Seleccionar 20 peliculas de mi DB
movies = db_cursor.execute("""SELECT id, title, overview, popularity, rating, released_on, genders, actors, poster, imdb_link, yt_trailer, magnet_link 
							  FROM movies LIMIT 20;""")

data_key = ('id', 'title', 'overview', 'popularity', 'rating', 'released_on', 'genders', 'actors', 'poster', 'imdb_link', 'yt_trailer', 'magnet_link')
movies = [{k:v for k,v in zip(data_key, movie_tuple)} for movie_tuple in movies ]


def search_movie(some_id):
	print(f"search_movie id: {some_id}")
	query = """SELECT id, title, overview, popularity, rating, released_on, genders, actors, poster, imdb_link, yt_trailer, magnet_link FROM movies WHERE id={};""".format(some_id)
	movie_tuple = db_cursor.execute(query).fetchone()
	if movie_tuple is None:
		return None
	# Create a dictionary with the movie attributes as keys and values from the query to the table
	movie = {k:v for k,v in zip(data_key, movie_tuple)}
	return movie

@app.route('/')
def home():
    return render_template('index.html', movies=movies)


@app.route('/movies/<movie_id>')
def movie(movie_id):
	print(movie_id)
	movie = search_movie(movie_id)
	if movie is None:
		return f"Tut mir leid. Could not get data for movie {movie_id}"
	else:
		return render_template('movie.html', movie=movie)


