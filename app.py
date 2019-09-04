import os

import pandas as pd
import requests
import tmdbsimple
from bottle import run, get, abort

tmdbsimple.API_KEY = os.environ['TOKEN_KEY']
DEBUG = os.environ.get('DEBUG', False)
LANGUAGE = 'fr-FR'


@get('/movies/<uid:int>')
def movie_retrieve(uid):
    return tmdbsimple.Movies(uid).info(append_to_response='credits,keywords,videos,reviews')


@get('/movies/<uid:int>/recommendation')
def recommendation(uid):
    df = pd.read_csv('data/movie.csv')
    cluster = df.loc[df['id'] == uid].cluster
    response = None

    if cluster.any():
        response = df.loc[df['cluster'] == int(cluster)].to_dict()

    return response or abort(404, 'No result')


@get('/movies/top/<page:int>')
def top(page):
    return tmdbsimple.Movies().top_rated(page=page, language=LANGUAGE)


@get('/movies/popular/<page:int>')
def popular(page):
    return tmdbsimple.Movies().popular(page=page, language=LANGUAGE)


@get('/movies/now-playing/<page:int>')
def now_playing(page):
    return tmdbsimple.Movies().popular(page=page, language=LANGUAGE)


@get('/peoples/<uid:int>')
def people_retrieve(uid):
    return tmdbsimple.People(uid).info()


@get('/peoples/<uid:int>/movies')
def people_movies(uid):
    return tmdbsimple.People(uid).movie_credits(language=LANGUAGE)


if __name__ == '__main__':
    if not os.path.exists('data/movie.csv'):
        url = os.environ['DATA_URL']

        with open('data/movie.csv', 'wb') as f:
            f.write(requests.get(url).content)

    run(host='localhost', port=8080, debug=DEBUG)
