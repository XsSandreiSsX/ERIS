from typing import Annotated

from fastapi import Depends, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.users.models import User
from app.common.deps import ReadSessionDep
from app.users.service import JWTService
from app.users.repositories import UserDAO
from app.users.exceptions import NotAuthenticatedException, ForbiddenException
from app.users.schemas import JWTPayload
from app.users.permissions import PermissionEnum

bearer_security = HTTPBearer()


async def get_current_user(
        session: ReadSessionDep,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_security),

) -> User | None:
    token = credentials.credentials
    payload = JWTService.verify_token(token, "access")
    user = await UserDAO.get_one_or_none(session, id=payload.sub)
    if not user:
        raise NotAuthenticatedException()

    return user


async def get_refresh_token(
    refresh_token: Annotated[str | None, Cookie(alias="refresh_token")] = None,
) -> JWTPayload:
    if not refresh_token:
        raise NotAuthenticatedException()
    payload = JWTService.verify_token(refresh_token, "refresh")
    return payload


class HasPermission:
    def __init__(self, permission: PermissionEnum):
        self.permission = permission

    async def __call__(self,
                 session: ReadSessionDep,
                 current_user = Depends(get_current_user)
                ) -> User | None:
        is_permitted = await UserDAO.has_permission(session,
                                                    user_id=current_user.id,
                                                    permission=self.permission)

        if not is_permitted:
            raise ForbiddenException()

        return current_user


GetUserDep = Annotated[User, Depends(get_current_user)]
RefreshTokenDep = Annotated[JWTPayload, Depends(get_refresh_token)]