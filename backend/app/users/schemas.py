from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field

from app.users.config import Limits


class JWTPayload(BaseModel):
    sub: int
    jti: str | None = None
    type: Literal["access", "refresh"]
    exp: datetime


class UserCredentials(BaseModel):
    email: EmailStr = Field(max_length=Limits.EMAIL_MAX_LENGTH)
    password: str = Field(
        min_length=Limits.PASSWORD_MIN_LENGTH,
        max_length=Limits.PASSWORD_MAX_LENGTH)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class AccessTokenResponse(BaseModel):
    access_token: str

class TokenPairResponse(AccessTokenResponse):
    refresh_token: str


