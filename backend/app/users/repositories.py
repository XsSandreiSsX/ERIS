from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.repositories import BaseDAO
from app.users.models import User, UserSession, Permission, RolePermission, UserRole


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, *, email: str) -> User | None:
        return await cls.get_one_or_none(session, email=email)

    @classmethod
    async def check_permission(cls,
                               session: AsyncSession,
                               *,
                               user_id: int,
                               permission: str) -> bool:
        stmt = (
            select(Permission.id)
            .join(RolePermission,
                  RolePermission.permission_id == Permission.id)
            .join(UserRole,
                  UserRole.role_id == RolePermission.role_id)
            .where(
                UserRole.user_id == user_id,
                Permission.name == permission,
            )
            .limit(1)
        )

        result = await session.execute(stmt)
        return result.scalar() is not None

class UserSessionDAO(BaseDAO):
    model = UserSession

    @classmethod
    async def get_session_by_jti(cls, session: AsyncSession, *, jti: str) -> UserSession | None:
        return await cls.get_one_or_none(session, jti=jti)
