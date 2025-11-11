from __future__ import annotations
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from redis.asyncio import Redis
import structlog

# ---- local imports (your project structure) ----
# If your settings/logging/modules live under app/core/* keep these:
from app.core.settings import settings
from app.core.logging import configure_logging
from app.cache.memory import InMemoryCache
from app.cache.redis_backend import RedisCache
from app.db.repository import SynonymRepository
from app.services.synonyms import SynonymService
from app.api.routes import router

log = structlog.get_logger()
container: dict[str, Any] = {}

def _engine_url_from_settings() -> str:
    """
    Build a SQLAlchemy URL for SQL Server with ODBC Driver 18 and trust server cert.
    Prefers DSN if provided; otherwise builds from discrete env vars.
    """
    if settings.sqlserver_dsn:
        return f"mssql+pyodbc:///?odbc_connect={settings.sqlserver_dsn}"

    host = settings.sqlserver_host or "localhost"
    port = settings.sqlserver_port or 1433
    db = settings.sqlserver_db or "SynonymsDB"
    user = settings.sqlserver_user or "sa"
    pwd = settings.sqlserver_password or "YourStrong!Passw0rd"

    # TrustServerCertificate=yes avoids local SSL CA issues (dev only)
    return (
        f"mssql+pyodbc://{user}:{pwd}@{host}:{port}/{db}"
        f"?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    )

@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging(settings.log_level)
    log.info("starting_app", app=settings.app_name)

    # Repository (DB)
    repo = SynonymRepository(_engine_url_from_settings())

    # Cache (redis or in-memory)
    if settings.cache_backend == "redis":
        redis_url = settings.redis_url or "redis://redis:6379"
        client = Redis.from_url(redis_url, decode_responses=False)
        cache = RedisCache(client)
    else:
        cache = InMemoryCache()

    # Service
    svc = SynonymService(repo=repo, cache=cache, ttl_seconds=settings.cache_ttl_seconds)

    container["syn_service"] = svc
    container["repo"] = repo
    container["cache"] = cache

    try:
        yield
    finally:
        log.info("shutting_down")
        repo.dispose()
        await cache.close()
        log.info("shutdown_complete")

app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(router)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
