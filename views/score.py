import requests
from bottle import Bottle

from interfaces.cacheManager import CacheManager, ONE_WEEK

score_app = Bottle()


@score_app.get('/score/<query>')
def score_retrieve(query, rdb):
    cache_manager = CacheManager(rdb, f'score-{query}', ONE_WEEK)

    return cache_manager.get_or_set(
        requests.get,
        after_request='json',
        url=f'https://apis.justwatch.com/content/titles/fr_FR/popular?body={{"content_types":["movie"],"page":1,"page_size":1,"query":"{query}"}}'
    )
