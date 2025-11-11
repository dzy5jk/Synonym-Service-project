from __future__ import annotations
from typing import Any, Iterable, TypedDict
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from ..cache.interfaces import CacheBackend

log = structlog.get_logger()

class SynonymDTO(TypedDict):
    id: int
    word: str
    synonyms: list[str]

class SynonymService:
    def __init__(self, repo, cache: CacheBackend, ttl_seconds: int) -> None:
        self._repo = repo
        self._cache = cache
        self._ttl = ttl_seconds

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.2, min=0.2, max=2.0))
    async def get_all(self) -> dict[str, Any]:
        key = "synonyms:all"
        cached = await self._cache.get(key)
        if cached is not None:
            return {"source": "cache", "items": cached}
        # DB access is sync in this minimal example; could be async with async driver
        items: list[SynonymDTO] = list(self._repo.list_all())
        await self._cache.set(key, items, self._ttl)
        return {"source": "database", "items": items}

    async def invalidate(self) -> None:
        await self._cache.delete("synonyms:all")
