import logging

from authlib.integrations.httpx_client import AsyncOAuth2Client
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi import status
from typing import Annotated

from nulland.schemas.auth import TokenRequest, TokenResponse
from nulland.config import settings


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/token", include_in_schema=False)
async def get_token(req: Annotated[TokenRequest, Depends()]):
    """Part of the OAuth2 flow.

    This endpoint is used to exchange the authorization code for an access token from the OAuth provider.

    Since it is supposed that authentication and token aquiring will be fully managed by the external API user
    this endpoint exists only to support authentication for OpenAPI UI at /docs.
    """
    async with AsyncOAuth2Client(
        client_id=req.client_id,
        client_secret=req.client_secret,
        # token_endpoint_auth_method='client_secret_jwt'
    ) as client:
        try:
            token = await client.fetch_token(
                str(settings.auth.token_endpoint),
                grant_type=req.grant_type,
                code=req.code,
                redirect_uri=req.redirect_uri,
            )
        except Exception as exc:
            logger.error("Failed to fetch auth token: %s", exc)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to fetch the token")
        if "id_token" not in token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Received invalid token")
    return TokenResponse(access_token=token["id_token"], token_type=token["token_type"])
