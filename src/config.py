
# src.config
from pydantic import PostgresDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings



class Config(BaseSettings):
    DATABASE_URL: str

    # REDIS_URL: RedisDsn

    # SITE_DOMAIN: str = "myapp.com"


    # SENTRY_DSN: str | None = None

    # CORS_ORIGINS: list[str]
    # CORS_ORIGINS_REGEX: str | None = None
    # CORS_HEADERS: list[str]

    # APP_VERSION: str = "1.0"


settings = Config(_env_file='dev.env', _env_file_encoding='utf-8')