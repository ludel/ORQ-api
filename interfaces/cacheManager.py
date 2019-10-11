import json

from bottle import abort
from requests import exceptions


class CacheManager:
    def __init__(self, cache_db, key, expiration=86400):
        self.key = key
        self.expiration = expiration
        self.cache_db = cache_db

    def get_or_set(self, request, **kwargs):
        content = self.cache_db.get(self.key)

        if content:
            return json.loads(content)

        try:
            content = request(**kwargs)
        except exceptions.HTTPError:
            return abort(404, 'Not found')
        else:
            self.cache_db.set(self.key, json.dumps(content), ex=self.expiration)

        return content
