from datetime import datetime, UTC, timedelta
from typing import Literal
from uuid import uuid4, UUID

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.exceptions import EmailExistsException
from app.users.models import User
from app.users.repositories import UserDAO, UserSessionDAO
from app.users.schemas import UserCredentials, TokenPairResponse, JWTPayload
from app.core.settings import settings
from app.users.exceptions import InvalidCredentialsException, ExpiredTokenException
from app.users.exceptions import NotAuthenticatedException

password_hash = PasswordHash.recommended()


class JWTService:
    @classmethod
    async def generate_access_token(cls, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "type": "access",
            "exp": datetime.now(UTC) + timedelta(milliseconds=settings.JWT_ACCESS_TOKEN_TTL_MS)
        }

        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return jwt_token

    @classmethod
    async def generate_refresh_token(cls, expires_at: datetime, jti: UUID, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "jti": str(jti),
            "exp": expires_at
        }

        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return jwt_token

    @classmethod
    async def verify_token(cls, token: str, token_type: Literal["access", "refresh"]) -> JWTPayload:
        required = {
            "access": ["sub", "exp", "type"],
            "refresh": ["sub", "exp", "type", "jti"],
        }
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=settings.JWT_ALGORITHM,
                options={"require": required[token_type]},
            )

        except ExpiredSignatureError:
            raise ExpiredTokenException()
        except InvalidTokenError:
            raise NotAuthenticatedException()

        return JWTPayload.model_validate(payload)


class UserService:
    @classmethod
    async def register_user(cls, *, session: AsyncSession, credentials: UserCredentials) -> User:
        user = await UserDAO.get_user_by_email(session, email=credentials.email)
        if user:
            raise EmailExistsException()

        hashed_password = password_hash.hash(credentials.password)

        user = await UserDAO.add(session,
                                 email=credentials.email,
                                 password_hash=hashed_password)

        return user

    @classmethod
    async def login_user(cls, *, session: AsyncSession, credentials: UserCredentials) -> TokenPairResponse:
        user = await UserDAO.get_user_by_email(session, email=credentials.email)
        if not user:
            raise InvalidCredentialsException()

        if not password_hash.verify(credentials.password, user.password_hash):
            raise InvalidCredentialsException()

        session_jti = uuid4()
        session_expires_at = datetime.now(UTC) + timedelta(milliseconds=settings.JWT_REFRESH_TOKEN_TTL_MS)

        await UserSessionDAO.add(session, user_id=user.id,
                                 jti=session_jti, expires_at=session_expires_at)

        access_token = await JWTService.generate_access_token(user.id)
        refresh_token = await JWTService.generate_refresh_token(session_expires_at, session_jti, user.id)

        return TokenPairResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @classmethod
    async def get_access_token(cls, *, session: AsyncSession, refresh_token: JWTPayload) -> str:
        user_session = await UserSessionDAO.get_session_by_jti(session, jti=refresh_token.jti)
        if not user_session:
            raise NotAuthenticatedException()

        if datetime.now(UTC) >= user_session.expires_at:
            raise NotAuthenticatedException()

        if user_session.revoked_at is not None:
            raise NotAuthenticatedException()

        return await JWTService.generate_access_token(refresh_token.sub)

    @classmethod
    async def logout(cls, *, session: AsyncSession, refresh_token: JWTPayload) -> None:
        user_session = await UserSessionDAO.get_session_by_jti(session, jti=refresh_token.jti)
        if not user_session:
            raise NotAuthenticatedException()

        await UserSessionDAO.update_obj(session, {"revoked_at": datetime.now(UTC)}, obj=user_session)





