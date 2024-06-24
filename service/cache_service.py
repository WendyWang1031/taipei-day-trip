import redis

def get_redis_connection():
    r = redis.Redis(host="localhost" , port=6379 , db=0)
    return r


class CacheService:
    def __init__(self, redis_connection):
        print("get ready to connect redis")
        self.redis = redis_connection
        print("already connect redis")

    def set_value(self, key, value, expiry=None):
        if expiry:
            self.redis.setex(key, expiry, value)
        else:
            self.redis.set(key, value)

    def get_value(self, key):
        return self.redis.get(key)

    def delete_value(self, key):
        self.redis.delete(key)


