import redis

# It's recommended to load this from environment variables
REDIS_HOST = "localhost"
REDIS_PORT = 6379

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

def set_token(token: str, email: str, expiration_seconds: int):
    redis_client.setex(token, expiration_seconds, email)

def get_email_by_token(token: str):
    return redis_client.get(token)

def delete_token(token: str):
    redis_client.delete(token)
