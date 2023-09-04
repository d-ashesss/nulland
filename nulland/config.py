import httpx

from enum import StrEnum
from pydantic import PostgresDsn, HttpUrl, BaseModel
from pydantic_settings import BaseSettings


LogFormat = StrEnum("LogFormat", ["DEFAULT", "JSON"])


class AuthSettings(BaseModel):
    """Authentication settings retrieved from OIDC configuration URL.

    Attributes:
        authorization_endpoint: The OIDC authorization endpoint
        token_endpoint: The OIDC token endpoint
        jwks_uri: The OIDC JWKS URL
    """

    authorization_endpoint: HttpUrl | None = None
    token_endpoint: HttpUrl | None = None
    jwks_uri: HttpUrl | None = None


class Settings(BaseSettings):
    """Application settings.

    Attributes:
        auth_openid_configuration_url: The URL of the OIDC configuration endpoint
        database_uri: The URI of the PostgreSQL database
    """

    auth_openid_configuration_url: HttpUrl | None = None
    auth: AuthSettings | None = None

    database_uri: PostgresDsn

    cors_allowed_origins: list[str] = ["*"]

    log_format: LogFormat = "default"

    def __hash__(self):
        return 0


settings = Settings()
if not settings.auth:
    settings.auth = AuthSettings()
    if settings.auth_openid_configuration_url:
        oidc_conf = httpx.get(str(settings.auth_openid_configuration_url)).json()
        settings.auth = AuthSettings(**oidc_conf)
