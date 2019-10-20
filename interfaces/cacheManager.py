import json

from bottle import abort
from requests import exceptions

ONE_DAY = 60 * 60 * 24
ONE_WEEK = ONE_DAY * 7
ONE_MONTH = ONE_WEEK * 4
ONE_YEAR = ONE_MONTH * 12


class CacheManager:
    def __init__(self, cache_db, key, expiration=ONE_WEEK):
        self.key = key
        self.expiration = expiration
        self.cache_db = cache_db

    def get_or_set(self, request, after_request=None, **kwargs):
        content = self.cache_db.get(self.key)

        if content:
            return json.loads(content)

        try:
            content = request(**kwargs)
        except exceptions.HTTPError:
            return abort(404, 'Not found')

        if after_request:
            content = getattr(content, after_request)()

        self.cache_db.set(self.key, json.dumps(content), ex=self.expiration)

        return content
