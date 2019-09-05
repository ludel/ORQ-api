import os

import tmdbsimple

tmdbsimple.API_KEY = os.environ['API_TOKEN']
DEBUG = os.environ.get('DEBUG', False)
LANGUAGE = 'fr-FR'
