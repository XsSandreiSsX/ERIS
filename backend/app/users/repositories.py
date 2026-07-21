from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.repositories import BaseDAO
from app.users.models import User, UserSession, Permission, RolePermission, UserRole, Role
from app.users.permissions import RoleEnum


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, *, email: str) -> User | None:
        return await cls.get_one_or_none(session, email=email)

    @classmethod
    async def has_permission(cls,
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

    @classmethod
    async def has_role(cls,
                       session: AsyncSession,
                       *,
                       user_id: int,
                       role: RoleEnum) -> bool:

        stmt = (
            select(Role.id)
            .join(UserRole,
                  UserRole.role_id == Role.id)
            .where(
                UserRole.user_id == user_id,
                Role.name == role,
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


class UserRoleDAO(BaseDAO):
    model = UserRole

    @classmethod
    async def assign(cls,
                     session: AsyncSession,
                     *,
                     user_id: int,
                     role_id: int) -> UserRole | None:
        stmt = (
            insert(UserRole)
            .values(
                user_id=user_id,
                role_id=role_id,
            )
            .on_conflict_do_nothing(
                index_elements=[
                    UserRole.user_id,
                    UserRole.role_id,
                ]
            )
            .returning(UserRole)
        )

        result = await session.execute(stmt)
        return result.scalar_one_or_none()


class RoleDAO(BaseDAO):
    model = Role

    @classmethod
    async def get_by_name(cls,
                          session: AsyncSession,
                          *,
                          name: RoleEnum) -> Role | None:
        return await cls.get_one_or_none(session, name=name.value)