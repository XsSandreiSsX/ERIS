from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.repositories import BaseDAO
from app.sellers.models import SellerProfile


class SellerProfileDAO(BaseDAO):
    model = SellerProfile

    @classmethod
    async def create(cls,
                     session: AsyncSession,
                     *,
                     user_id: int,
                     store_name: str,
                     store_slug: str) -> SellerProfile:

        return await cls.add(session,
                             user_id=user_id,
                             store_name=store_name,
                             store_slug=store_slug)

    @classmethod
    async def get_by_slug(cls,
                          session: AsyncSession,
                          *,
                          slug: str) -> SellerProfile | None:
        return await cls.get_one_or_none(session,
                                         store_slug=slug)

    @classmethod
    async def update_profile(cls,
                             session: AsyncSession,
                             user_id: int,
                             **data) -> SellerProfile | None:

        await cls._check_model_fields(data)

        stmt = (
            update(SellerProfile)
            .where(SellerProfile.user_id == user_id)
            .values(**data)
            .returning(SellerProfile)
        )

        result = await session.execute(stmt)
        return result.scalar_one_or_none()



