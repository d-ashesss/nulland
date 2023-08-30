import httpx
import logging

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2AuthorizationCodeBearer
from functools import lru_cache
from jose import jwt, JWTError
from pydantic import ValidationError
from typing import Annotated

from nulland.schemas.auth import User
from nulland.settings import Settings, get_settings

_logger = logging.getLogger(__name__)
_settings = get_settings()
_oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=str(_settings.auth.authorization_endpoint),
    tokenUrl="token",
    scopes={
        "openid": "(required) indicate the intent to use OIDC",
        "profile": "(required) include user personal details",
        "email": "(required) include user's email address",
    },
)


@lru_cache()
def get_public_key(settings: Annotated[Settings, Depends(get_settings)]):
    """Loads the public key from the OIDC provider."""
    _logger.info("Loading public key from %s", settings.auth.jwks_uri)
    return httpx.get(str(settings.auth.jwks_uri)).json()


def get_current_user(
        token: Annotated[str, Depends(_oauth2_scheme)],
        key: Annotated[dict, Depends(get_public_key)],
):
    """Parses the JWT token and returns the user object constructed from it."""
    try:
        claims = jwt.decode(token, key, options={"verify_aud": False})
    except JWTError as exc:
        _logger.warning("Failed to decode auth token: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user = User(**claims)
    except ValidationError as exc:
        _logger.error("Auth token contains incompatible claims: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
