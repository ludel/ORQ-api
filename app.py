import os

import tmdbsimple
from bottle import Bottle, response

from views.movie import movie_app
from views.people import people_app

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


main_app.merge(people_app)
main_app.merge(movie_app)

if DEBUG:
    main_app.run(host='localhost', port=8080, debug=DEBUG)
