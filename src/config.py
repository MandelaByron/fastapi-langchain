
# src.config
from pydantic import PostgresDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict



class Config(BaseSettings):
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8',extra='ignore')
    DATABASE_URL: str

    # REDIS_URL: RedisDsn

    # SITE_DOMAIN: str = "myapp.com"


    # SENTRY_DSN: str | None = None

    # CORS_ORIGINS: list[str]
    # CORS_ORIGINS_REGEX: str | None = None
    # CORS_HEADERS: list[str]

    # APP_VERSION: str = "1.0"


settings = Config()