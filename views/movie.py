import os

import tmdbsimple
from bottle import Bottle

from interfaces.cacheManager import CacheManager, ONE_MONTH

LANGUAGE = os.environ['LANGUAGE']
FILTERS = {
    'upcoming': tmdbsimple.Movies().upcoming,
    'top': tmdbsimple.Movies().top_rated,
    'popular': tmdbsimple.Movies().popular,
    'now-playing': tmdbsimple.Movies().now_playing,
}

movie_app = Bottle()


@movie_app.get('/movies/<uid:int>')
def movie_retrieve(uid, rdb):
    cache_manager = CacheManager(rdb, f'movie-{uid}', ONE_MONTH)

    return cache_manager.get_or_set(
        tmdbsimple.Movies(uid).info,
        language=LANGUAGE,
        append_to_response='credits,keywords,videos,reviews,images'
    )


@movie_app.get(f"/movies/<filter_option:re:{'|'.join(FILTERS.keys())}>/<page:int>")
def movie_filter(filter_option, page):
    return FILTERS[filter_option](page=page, language=LANGUAGE)


@movie_app.get('/movies/search/<query>/<page:int>')
def movie_search(query, page):
    return tmdbsimple.Search().movie(query=query, page=page, language=LANGUAGE)

