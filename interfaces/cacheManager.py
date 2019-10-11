import json


class CacheManager:
    def __init__(self, cache_db, key, expiration=86400):
        self.key = key
        self.expiration = expiration
        self.cache_db = cache_db

    def get_or_set(self, request, **kwargs):
        content = self.cache_db.get(self.key)

        if content:
            content = json.loads(content)
        else:
            content = request(**kwargs)
            self.cache_db.set(self.key, json.dumps(content), ex=self.expiration)

        return content
