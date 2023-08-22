from authlib.integrations.requests_client import OAuth2Session
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi import status
from typing import Annotated

from nulland.schemas.auth import TokenRequest, TokenResponse
from nulland.settings import Settings, get_settings


router = APIRouter()


@router.post("/token", include_in_schema=False)
async def get_token(settings: Annotated[Settings, Depends(get_settings)], req: Annotated[TokenRequest, Depends()]):
    """Part of the OAuth2 flow.

    This endpoint is used to exchange the authorization code for an access token from the OAuth provider.

    Since it is supposed that authentication and token aquiring will be fully managed by the external API user
    this endpoint exists only to support authentication for OpenAPI UI at /docs.
    """
    oauth_sess = OAuth2Session(
        client_id=req.client_id,
        client_secret=req.client_secret,
    )
    try:
        token = oauth_sess.fetch_token(
            settings.auth.token_endpoint,
            grant_type=req.grant_type,
            code=req.code,
            redirect_uri=req.redirect_uri,
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to fetch the token")
    if "id_token" not in token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Received invalid token")
    return TokenResponse(access_token=token["id_token"], token_type=token["token_type"])
