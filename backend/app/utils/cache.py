import redis
import json

from app.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

def set_cache(key: str, value: dict, expire_seconds: int = 600):
    redis_client.set(
        key,
        json.dumps(value),
        ex=expire_seconds
    )

def get_cache(key: str):
    data = redis_client.get(key)
    
    if data:
        return json.loads(data)
    
    return None