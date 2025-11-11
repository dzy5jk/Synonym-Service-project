from __future__ import annotations
import orjson
from typing import Any
from redis.asyncio import Redis
from .interfaces import CacheBackend

class RedisCache(CacheBackend):
    def __init__(self, client: Redis) -> None:
        self._client = client

    async def get(self, key: str) -> Any | None:
        data = await self._client.get(key)
        if data is None:
            return None
        return orjson.loads(data)

    async def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        await self._client.set(key, orjson.dumps(value), ex=ttl_seconds)

    async def delete(self, key: str) -> None:
        await self._client.delete(key)

    async def close(self) -> None:
        await self._client.aclose()
