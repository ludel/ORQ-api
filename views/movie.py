import os

import pandas as pd
import tmdbsimple
from bottle import Bottle, abort

from interfaces.cacheManager import CacheManager
from views.models import Movie

LANGUAGE = os.environ['LANGUAGE']
FILTERS = {
    'upcoming': tmdbsimple.Movies().upcoming,
    'top': tmdbsimple.Movies().top_rated,
    'popular': tmdbsimple.Movies().popular,
    'now-playing': tmdbsimple.Movies().now_playing,
}

movie_app = Bottle()
df = pd.read_csv('data/movie.csv')


@movie_app.get('/movies/<uid:int>')
def movie_retrieve(uid):
    cache_manager = CacheManager(f'movie-{uid}', 60 * 60 * 24 * 7)

    return cache_manager.get_or_set(
        tmdbsimple.Movies(uid).info,
        language=LANGUAGE,
        append_to_response='credits,keywords,videos,reviews,images'
    )


@movie_app.get('/movies/<uid:int>/recommendation/<selection_ids>')
def movie_recommendation(uid, selection_ids):
    cluster = df.loc[df['id'] == uid, 'cluster']

    if cluster.empty:
        return abort(404, 'No result')

    movies_in_cluster = df.loc[df.cluster == int(cluster), 'id'].tolist()
    movies_in_cluster.remove(uid)

    selection_ids = [int(select_id) for select_id in selection_ids.split(',')]

    results, _ = Movie.recommendation(
        selection_ids,
        movies_in_cluster
    )

    return {'ids': [Movie.inflate(row[0]).uid for row in results]}


@movie_app.get(f"/movies/<filter_option:re:{'|'.join(FILTERS.keys())}>/<page:int>")
def movie_filter(filter_option, page):
    return FILTERS[filter_option](page=page, language=LANGUAGE)


@movie_app.get('/movies/search/<query>/<page:int>')
def movie_search(query, page):
    return tmdbsimple.Search().movie(query=query, page=page, language=LANGUAGE)
