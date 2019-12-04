import os

import bottle_redis
import bottle_sqlite
import tmdbsimple
from bottle import Bottle, response

from models.user import User
from views.movie import movie_app
from views.people import people_app
from views.recommendation import recommendation_app
from views.score import score_app
from views.session import session_app

DEBUG = os.environ.get('DEBUG', False)
tmdbsimple.API_KEY = os.environ['API_TOKEN']
DB_FILE = 'db.sqlite'

main_app = Bottle()

redis_plugin = bottle_redis.RedisPlugin(host='localhost')
sqlite_plugin = bottle_sqlite.SQLitePlugin(dbfile=DB_FILE)

people_app.install(redis_plugin)
movie_app.install(redis_plugin)
score_app.install(redis_plugin)

session_app.install(sqlite_plugin)


@main_app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*' if DEBUG else 'https://onregardequoi.net'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


main_app.merge(people_app)
main_app.merge(movie_app)
main_app.merge(score_app)
main_app.merge(recommendation_app)
main_app.merge(session_app)

User.init(DB_FILE)
if DEBUG:
    main_app.run(host='localhost', port=8080, debug=DEBUG)
