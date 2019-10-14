import os

import bottle_redis
import tmdbsimple
from bottle import Bottle, response

from views.movie import movie_app
from views.people import people_app
from views.score import score_app

DEBUG = os.environ.get('DEBUG', False)
tmdbsimple.API_KEY = os.environ['API_TOKEN']

main_app = Bottle()
redis_plugin = bottle_redis.RedisPlugin(host='localhost', socket_keepalive=True, retry_on_timeout=True)

people_app.install(redis_plugin)
movie_app.install(redis_plugin)
score_app.install(redis_plugin)


@main_app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*' if DEBUG else 'https://onregardequoi.net'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


main_app.merge(people_app)
main_app.merge(movie_app)
main_app.merge(score_app)

if DEBUG:
    main_app.run(host='localhost', port=8080, debug=DEBUG)
