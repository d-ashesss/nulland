import httpx
import logging

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2AuthorizationCodeBearer
from functools import lru_cache
from jose import jwt, JOSEError
from pydantic import ValidationError
from typing import Annotated

from nulland.schemas.auth import User
from nulland.config import settings


logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=str(settings.auth.authorization_endpoint),
    tokenUrl="token",
    scopes={
        "openid": "(required) indicate the intent to use OIDC",
        "profile": "(required) include user personal details",
        "email": "(required) include user's email address",
    },
)


@lru_cache()
def get_public_key():
    """Loads the public key from the OIDC provider."""
    if not settings.auth.jwks_uri:
        logger.error("No JWT key source provided, authentication will not work.")
        return None
    logger.info("Loading public key from %s", settings.auth.jwks_uri)
    try:
        return httpx.get(str(settings.auth.jwks_uri)).json()
    except httpx.HTTPError as exc:
        logger.critical("Failed to load public key: %s", exc)
        raise


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Parses the JWT token and returns the user object constructed from it."""
    try:
        key = get_public_key()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service Unavailable",
        )
    try:
        claims = jwt.decode(token, key, options={"verify_aud": False})
    except JOSEError as exc:
        logger.warning("Failed to decode auth token: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user = User(**claims)
    except ValidationError as exc:
        logger.error("Auth token contains incompatible claims: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
