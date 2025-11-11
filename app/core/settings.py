from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # App
    app_name: str = "synonym-service"
    log_level: str = "INFO"
    port: int = 8000

    # DB (SQL Server via ODBC)
    sqlserver_dsn: str | None = None
    sqlserver_host: str | None = None
    sqlserver_port: int | None = 1433
    sqlserver_user: str | None = None
    sqlserver_password: str | None = None
    sqlserver_db: str | None = None

    # Cache
    cache_backend: str = Field(default="memory", description="memory | redis")
    cache_ttl_seconds: int = 600
    redis_url: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
