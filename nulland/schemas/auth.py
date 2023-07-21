from dataclasses import dataclass
from fastapi import Form
from pydantic import BaseModel, Field


@dataclass
class TokenRequest():
    grant_type: str = Form(...)
    code: str = Form(...)
    client_id: str | None = Form(default=None)
    client_secret: str | None = Form(default=None)
    redirect_uri: str = Form(...)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: str = Field(alias="sub")
    name: str
    email: str
