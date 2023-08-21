from functools import lru_cache
from pydantic import PostgresDsn, HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings.
    
    Attributes:
        database_uri: The URI of the PostgreSQL database
    """

    auth_authorization_endpoint: HttpUrl
    auth_token_endpoint: HttpUrl
    auth_jwks_url: HttpUrl
    auth_openid_configuration_url: HttpUrl

    database_uri: PostgresDsn

    def __hash__(self):
        return 0


@lru_cache()
def get_settings() -> Settings:
    """Load application settings as a singleton."""
    return Settings()
