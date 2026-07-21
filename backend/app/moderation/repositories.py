from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.repositories import BaseDAO
from app.moderation.models import RoleApplication, ReviewStatus
from app.users.permissions import RoleEnum
from app.moderation.schemas.role_application import RoleApplicationFilter


class RoleApplicationDAO(BaseDAO):
    model = RoleApplication

    @classmethod
    async def get_latest(cls,
                         session: AsyncSession,
                         *,
                         user_id: int,
                         role: RoleEnum) -> RoleApplication | None:

        stmt = (
            select(RoleApplication)
            .where(RoleApplication.user_id == user_id,
                   RoleApplication.requested_role == role)
            .order_by(RoleApplication.updated_at.desc())
            .limit(1)
        )

        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def get_applications(
            cls,
            session: AsyncSession,
            *,
            limit: int,
            offset: int,
            filters: RoleApplicationFilter,
            user_id: int | None = None,
    ) -> tuple[list[RoleApplication], int]:
        stmt = select(RoleApplication)

        if user_id is not None:
            stmt = stmt.where(
                RoleApplication.user_id == user_id
            )

        if filters.role is not None:
            stmt = stmt.where(
                RoleApplication.requested_role == filters.role
            )

        if filters.status is not None:
            stmt = stmt.where(
                RoleApplication.status == filters.status
            )

        count_stmt = (
            stmt
            .with_only_columns(func.count())
            .order_by(None)
        )

        total_items = await session.scalar(count_stmt) or 0

        stmt = (
            stmt
            .order_by(RoleApplication.created_at.asc())
            .limit(limit)
            .offset(offset)
        )

        result = await session.scalars(stmt)
        applications = list(result.all())

        return applications, total_items

    @classmethod
    async def update_application(cls,
                                 session: AsyncSession,
                                 *,
                                 application_id: int,
                                 status: ReviewStatus,
                                 reviewer_id: int,
                                 rejection_reason: str | None = None,
                                 ) -> RoleApplication | None:
        stmt = (
            update(RoleApplication)
            .where(RoleApplication.id == application_id,
                   RoleApplication.status == ReviewStatus.PENDING)
            .values(
                status=status,
                reviewed_by_id=reviewer_id,
                rejection_reason=rejection_reason
            )
            .returning(RoleApplication)
        )

        result = await session.execute(stmt)
        return result.scalar_one_or_none()




