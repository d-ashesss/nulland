import requests

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


@lru_cache()
def get_oauth2_scheme() -> OAuth2AuthorizationCodeBearer:
    settings = get_settings()
    return OAuth2AuthorizationCodeBearer(
        authorizationUrl=str(settings.auth_authorization_endpoint),
        tokenUrl="token",
        scopes={
            "openid": "(required) indicate the intent to use OIDC",
            "profile": "(required) include user personal details",
            "email": "(required) include user's email address",
        },
    )


@lru_cache()
def get_public_key(settings: Annotated[Settings, Depends(get_settings)]):
    return requests.get(settings.auth_jwks_url).json()


def get_current_user(
        token: Annotated[str, Depends(get_oauth2_scheme())],
        key: Annotated[dict, Depends(get_public_key)],
):
    try:
        claims = jwt.decode(token, key, options={"verify_aud": False})
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user = User(**claims)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
