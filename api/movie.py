import pandas as pd
import tmdbsimple
from bottle import Bottle, abort

from api import LANGUAGE

movie_app = Bottle()


@movie_app.get('/movies/<uid:int>')
def movie_retrieve(uid):
    return tmdbsimple.Movies(uid).info(append_to_response='credits,keywords,videos,reviews')


@movie_app.get('/movies/<uid:int>/recommendation')
def movie_recommendation(uid):
    df = pd.read_csv('data/movie.csv')
    cluster = df.loc[df['id'] == uid].cluster

    if cluster.any():
        return df.loc[df['cluster'] == int(cluster)].to_dict()

    return abort(404, 'No result')


@movie_app.get('/movies/top/<page:int>')
def movie_top(page):
    return tmdbsimple.Movies().top_rated(page=page, language=LANGUAGE)


@movie_app.get('/movies/popular/<page:int>')
def movie_popular(page):
    return tmdbsimple.Movies().popular(page=page, language=LANGUAGE)


@movie_app.get('/movies/now-playing/<page:int>')
def movie_now_playing(page):
    return tmdbsimple.Movies().popular(page=page, language=LANGUAGE)
