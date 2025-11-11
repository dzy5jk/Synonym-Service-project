import asyncio, pytest
from app.cache.memory import InMemoryCache

@pytest.mark.asyncio
async def test_memory_cache_ttl():
    c = InMemoryCache()
    await c.set("k","v", ttl_seconds=1)
    assert await c.get("k") == "v"
    await asyncio.sleep(1.1)
    assert await c.get("k") is None
