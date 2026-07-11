from sqlalchemy.ext.asyncio import AsyncSession

from app.common.repositories import BaseDAO
from app.users.models import User, UserSession


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, *, email: str) -> User | None:
        return await cls.get_one_or_none(session, email=email)

class UserSessionDAO(BaseDAO):
    model = UserSession

    @classmethod
    async def get_session_by_jti(cls, session: AsyncSession, *, jti: str) -> UserSession | None:
        return await cls.get_one_or_none(session, jti=jti)
