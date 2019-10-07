import os

import tmdbsimple
from neomodel import config
import redis

cache = redis.Redis(host='localhost', port=6379, db=0)
tmdbsimple.API_KEY = os.environ['API_TOKEN']
config.DATABASE_URL = os.environ['BOLT']
