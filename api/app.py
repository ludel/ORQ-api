import os

import requests
import tmdbsimple
from bottle import Bottle, response
from movie import movie_app
from people import people_app

DEBUG = os.environ.get('DEBUG', False)
tmdbsimple.API_KEY = os.environ['API_TOKEN']

main_app = Bottle()


@main_app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = os.environ.get('ALLOW_ORIGIN', '')
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


def check_data():
    if not os.path.exists('data/movie.csv'):
        url = os.environ['DATA_URL']

        with open('data/movie.csv', 'wb') as f:
            f.write(requests.get(url).content)


if __name__ == '__main__':
    check_data()
    main_app.merge(people_app)
    main_app.merge(movie_app)
    main_app.run(host='localhost', port=8080, debug=DEBUG)
