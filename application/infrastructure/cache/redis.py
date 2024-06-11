from contextlib import asynccontextmanager
from typing import Optional, AsyncGenerator

from redis import asyncio as aioredis, RedisError

from application.config import settings
from application.exceptions import RedisConnectError
from application.infrastructure.cache.store import CacheStore


class RedisCacheStore(CacheStore):
    """ Redis реализация репозитория для хранения данных ключ-значение """
    _prefix: str
    _ttl: int
    _client: Optional[aioredis.Redis]

    def __init__(self, prefix: str) -> None:
        self._ttl = settings.redis.REDIS_DEFAULT_TTL
        self._prefix = prefix
        self._client = None

    async def connect(self):
        try:
            self._client = await aioredis.from_url(url=settings.redis.url)

        except RedisError:
            raise RedisConnectError

    def key_name(self, key: str) -> str:
        return f"{self._prefix}:{key}" if self._prefix else str(key)

    async def get(self, key):
        value: Optional[str] = await self._client.get(name=self.key_name(key))
        return value

    async def get_multi(self, *keys):
        with self._client as client:
            keys = tuple(map(self.key_name, keys))
            values = await client.mget(keys=keys)
            if not values:
                return []
            return values

    async def delete(self, key):
        await self._client.delete(self.key_name(key))

    async def delete_multi(self, *keys):
        keys = tuple(map(self.key_name, keys))
        with self._client as client:
            await client.delete(*keys)

    async def set(self, key, value, expire_at: Optional[int] = None):
        ttl = max(expire_at, 0) if expire_at else self._ttl
        await self._client.set(name=self.key_name(key), value=value, ex=ttl)

    async def set_multi(self, expire_at: Optional[int] = None, **key_vals):
        for key, val in key_vals.items():
            await self.set(key, val, expire_at=expire_at)

    async def search(self, match):
        with self._client as client:
            keys = await client.keys(pattern=self.key_name(match))
            values = await client.mget(keys=keys)
            if not values:
                return []
            return values

    async def shutdown(self):
        await self._client.close()


@asynccontextmanager
async def get_cache_client(cache_store: CacheStore) -> AsyncGenerator[CacheStore, None]:
    await cache_store.connect()
    try:
        yield cache_store
    finally:
        await cache_store.shutdown()


def with_redis_store(prefix):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            store = RedisCacheStore(prefix=prefix)
            async with get_cache_client(store) as redis_store:
                return await func(redis_store, *args, **kwargs)

        return wrapper

    return decorator
