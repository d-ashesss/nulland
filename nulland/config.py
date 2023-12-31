import httpx

from enum import StrEnum
from pydantic import PostgresDsn, HttpUrl, BaseModel
from pydantic_settings import BaseSettings
from typing import ClassVar


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
        auth: The authentication settings
        database_uri: The URI of the PostgreSQL database
        cors_allowed_origins: The list of allowed CORS origins
        log_format: The log format: default, json
        event_producer: The type of event producer: none, stdout, kafka
        kafka_client_id: The Kafka client ID
        kafka_bootstrap_servers: The Kafka bootstrap servers
        kafka_sasl_username: The Kafka username
        kafka_sasl_password: The Kafka password
    """
    LogFormat: ClassVar = StrEnum("LogFormat", ["DEFAULT", "JSON"])
    EventProducer: ClassVar = StrEnum("EventProducer", ["NONE", "STDOUT", "KAFKA"])

    auth_openid_configuration_url: HttpUrl | None = None
    auth: AuthSettings | None = None

    database_uri: PostgresDsn

    cors_allowed_origins: list[str] = ["*"]

    log_format: LogFormat = LogFormat.DEFAULT

    event_producer: EventProducer = EventProducer.STDOUT
    kafka_client_id: str = "notes-service"
    kafka_bootstrap_servers: str | None = None
    kafka_sasl_username: str | None = None
    kafka_sasl_password: str | None = None

    def __hash__(self):
        return 0


settings = Settings()
if not settings.auth:
    settings.auth = AuthSettings()
    if settings.auth_openid_configuration_url:
        oidc_conf = httpx.get(str(settings.auth_openid_configuration_url)).json()
        settings.auth = AuthSettings(**oidc_conf)
