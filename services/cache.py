from typing import Optional
import os
import redis


def get_redis() -> redis.Redis:
    url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return redis.from_url(url, decode_responses=True)


def cache_set(key: str, value: str, ttl: int = 300) -> None:
    r = get_redis()
    r.set(key, value, ex=ttl)


def cache_get(key: str) -> Optional[str]:
    r = get_redis()
    return r.get(key)
