import redis

def get_redis_connection():
    r = redis.Redis(host="localhost" , port=6379 , db=0)
    return r