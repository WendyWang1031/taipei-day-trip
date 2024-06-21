from db.redis_connection import get_redis_connection


class CacheService:
    def __init__(self):
        self.redis = get_redis_connection()

    def set_value(self, key, value, expiry=None):
        if expiry:
            self.redis.setex(key, expiry, value)
        else:
            self.redis.set(key, value)

    def get_value(self, key):
        return self.redis.get(key)

    def delete_value(self, key):
        self.redis.delete(key)