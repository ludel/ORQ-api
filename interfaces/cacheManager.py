import json
import os

from views import cache


class CacheManager:
    def __init__(self, key, expiration=86400):
        self.key = key
        self.expiration = expiration

    def get_or_set(self, request, **kwargs):
        content = cache.get(self.key)

        if content:
            content = json.loads(content)
        else:
            content = request(**kwargs)
            cache.set(self.key, json.dumps(content), ex=self.expiration)

        return content
