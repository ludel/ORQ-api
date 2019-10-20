import os

import tmdbsimple
from neomodel import config

tmdbsimple.API_KEY = os.environ['API_TOKEN']
config.DATABASE_URL = os.environ['BOLT']
