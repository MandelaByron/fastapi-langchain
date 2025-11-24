from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8',extra='ignore')
    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 30  # minutes

    # REFRESH_TOKEN_KEY: str
    # REFRESH_TOKEN_EXP: timedelta = timedelta(days=30)


auth_settings = AuthConfig()