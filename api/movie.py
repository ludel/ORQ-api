import os

import pandas as pd
import tmdbsimple
from bottle import Bottle, abort

LANGUAGE = os.environ['LANGUAGE']
FILTERS = {
    'upcoming': tmdbsimple.Movies().upcoming,
    'top': tmdbsimple.Movies().top_rated,
    'popular': tmdbsimple.Movies().popular,
    'now-playing': tmdbsimple.Movies().now_playing,
}

movie_app = Bottle()


def add_is_clustered_attr(response):
    df = pd.read_csv('data/movie.csv')

    for index, movie in enumerate(response['results']):
        is_clustered = 'true' if df.id.isin([movie['id']]).any() else 'false'
        response['results'][index]['is_clustered'] = is_clustered

    return response


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


@movie_app.get(f"/movies/<filter_option:re:{'|'.join(FILTERS.keys())}>/<page:int>")
def movie_filter(filter_option, page):
    resp = FILTERS[filter_option](page=page, language=LANGUAGE)
    return add_is_clustered_attr(resp)
