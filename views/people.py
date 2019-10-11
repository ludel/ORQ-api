import os

import tmdbsimple
from bottle import Bottle

from interfaces.cacheManager import CacheManager

LANGUAGE = os.environ['LANGUAGE']

people_app = Bottle()


@people_app.get('/peoples/<uid:int>')
def peoples_retrieve(uid, rdb):
    cache_manager = CacheManager(rdb, f'people-{uid}', 60 * 60 * 24)

    return cache_manager.get_or_set(
        tmdbsimple.People(uid).info,
        language=LANGUAGE,
        append_to_response='combined_credits,images'
    )


@people_app.get('/peoples/popular/<page:int>')
def peoples_popular(page):
    return tmdbsimple.People().popular(page=page)


@people_app.get('/peoples/<uid:int>/movies')
def peoples_movies(uid):
    return tmdbsimple.People(uid).movie_credits(language=LANGUAGE)


@people_app.get('/peoples/search/<query>/<page:int>')
def peoples_search(query, page):
    return tmdbsimple.Search().person(query=query, page=page, language=LANGUAGE)
