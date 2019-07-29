import os

import tmdbsimple
from bottle import run, get

tmdbsimple.API_KEY = os.environ['TOKEN_KEY']
debug = os.environ.get('DEBUG', False)
language = 'fr-FR'


def movie():
    instance = tmdbsimple.Movies

    @get('/movies/<uid:int>')
    def movie_uid(uid):
        return instance(uid).info(append_to_response='credits,keywords,videos,reviews')

    @get('/movies/top/<page:int>')
    def movie_top(page):
        return instance().top_rated(page=page, language=language)

    @get('/movies/popular/<page:int>')
    def movie_popular(page):
        return instance().popular(page=page, language=language)

    @get('/movies/now-playing/<page:int>')
    def movie_now_playing(page):
        return instance().popular(page=page, language=language)


def people():
    instance = tmdbsimple.People

    @get('/peoples/<uid:int>')
    def movie_uid(uid):
        return instance(uid).info()

    @get('/peoples/<uid:int>/movies')
    def movie_uid(uid):
        return instance(uid).movie_credits(language=language)


if __name__ == '__main__':
    movie()
    people()
    run(host='localhost', port=8080, debug=debug)
