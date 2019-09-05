import tmdbsimple
from bottle import Bottle

from api import LANGUAGE

people_app = Bottle()


@people_app.get('/peoples/<uid:int>')
def people_retrieve(uid):
    return tmdbsimple.People(uid).info(language=LANGUAGE)


@people_app.get('/peoples/<uid:int>/movies')
def people_movies(uid):
    return tmdbsimple.People(uid).movie_credits(language=LANGUAGE)
