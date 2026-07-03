from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    app_name: str = "NSM"
    secret_key: str = Field(default="change-me-in-production")
    access_token_expire_minutes: int = 60

    postgres_dsn: str = "postgresql+asyncpg://nsm:nsm@postgres:5432/nsm"
    redis_dsn: str = "redis://redis:6379/0"

    hiddify_api_url: str = "http://hiddify:9000"
    hiddify_api_key: str = ""
    hiddify_proxy_path: str = ""
    panel_config_path: str = "config/panels.json"

    cors_origins: list[str] = ["http://localhost:3000"]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
