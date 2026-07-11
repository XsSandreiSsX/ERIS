from fastapi import APIRouter, Cookie, Depends, Response
from starlette import status

from app.users.schemas import UserCredentials, UserResponse, AccessTokenResponse
from app.common.deps import SessionDep, ReadSessionDep
from app.common.schemas import ErrorResponse
from app.users.service import UserService
from app.users.schemas import TokenPairResponse
from app.users.deps import GetUserDep, RefreshTokenDep
from app.core.settings import settings

users_router = APIRouter()


@users_router.post("/register",
                   response_model=UserResponse,
                   status_code=status.HTTP_201_CREATED,
                   responses={status.HTTP_409_CONFLICT: {"model": ErrorResponse}})
async def register(
        session: SessionDep,
        credentials: UserCredentials):
    user = await UserService.register_user(session=session, credentials=credentials)
    return UserResponse.model_validate(user, from_attributes=True)


@users_router.post("/login",
                   response_model=TokenPairResponse,
                   status_code=status.HTTP_200_OK,
                   responses={status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse}})
async def login(
        session: SessionDep,
        credentials: UserCredentials,
        response: Response
):
    tokens = await UserService.login_user(session=session, credentials=credentials)

    response.set_cookie(key="refresh_token",
                        value=tokens.refresh_token,
                        httponly=True,
                        secure=settings.JWT_REFRESH_COOKIE_SECURE,
                        samesite="lax",
                        max_age=settings.JWT_REFRESH_TOKEN_TTL_MS,
                        path="/auth"
                        )
    return tokens


@users_router.post("/refresh",
                   response_model=AccessTokenResponse,
                   status_code=status.HTTP_200_OK,
                   responses={status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse}})
async def refresh(
        session: ReadSessionDep,
        refresh_token: RefreshTokenDep,
):
    access_token = await UserService.get_access_token(session=session, refresh_token=refresh_token)
    return AccessTokenResponse(access_token=access_token)


@users_router.post("/logout",
                   status_code=status.HTTP_204_NO_CONTENT,
                   responses={status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse}})
async def logout(
        session: SessionDep,
        refresh_token: RefreshTokenDep,
        response: Response

):
    await UserService.logout(session=session, refresh_token=refresh_token)
    response.delete_cookie(key="refresh_token", path="/auth/refresh")
    return None

@users_router.get("/me",
                   response_model=UserResponse,
                   status_code=status.HTTP_200_OK,
                   responses={status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse}})
async def me(
        user: GetUserDep,
):
    return UserResponse.model_validate(user, from_attributes=True)
