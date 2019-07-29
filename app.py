import os

import pandas as pd
import tmdbsimple
from bottle import run, get,abort

tmdbsimple.API_KEY = os.environ['TOKEN_KEY']
DEBUG = os.environ.get('DEBUG', False)
LANGUAGE = 'fr-FR'


def movie():
    instance = tmdbsimple.Movies

    @get('/movies/<uid:int>')
    def retrieve(uid):
        return instance(uid).info(append_to_response='credits,keywords,videos,reviews')

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
        return instance().top_rated(page=page, language=LANGUAGE)

    @get('/movies/popular/<page:int>')
    def popular(page):
        return instance().popular(page=page, language=LANGUAGE)

    @get('/movies/now-playing/<page:int>')
    def now_playing(page):
        return instance().popular(page=page, language=LANGUAGE)


def people():
    instance = tmdbsimple.People

    @get('/peoples/<uid:int>')
    def retrieve(uid):
        return instance(uid).info()

    @get('/peoples/<uid:int>/movies')
    def movies(uid):
        return instance(uid).movie_credits(language=LANGUAGE)


if __name__ == '__main__':
    movie()
    people()
    run(host='localhost', port=8080, debug=DEBUG)
