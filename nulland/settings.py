from functools import lru_cache
from pydantic import PostgresDsn, HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_uri: PostgresDsn


@lru_cache()
def get_settings() -> Settings:
    return Settings()
