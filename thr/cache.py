class Cache:
    pass

class InMemoryCache(Cache):
    def __init__(self):
        self.key_cache = {}

    def get_or_call(self, identity: str, func):
        key = self.key_cache.get(identity)
        if key is None:
            key = func(identity)
            self.key_cache[identity] = key
        return key