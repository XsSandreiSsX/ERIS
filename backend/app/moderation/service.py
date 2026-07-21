from datetime import timedelta, datetime, UTC
from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from app.moderation.schemas.role_application import RoleApplicationCreate, RoleApplicationFilter
from app.users.exceptions import ForbiddenException, RoleAlreadyAssignedException
from app.users.models import User
from app.users.permissions import RoleEnum
from app.moderation.models import ReviewStatus, RoleApplication
from app.moderation.exceptions import RoleApplicationAlreadyExistsException
from app.users.repositories import UserDAO
from app.moderation.exceptions import RoleApplicationRetryTooSoonException
from app.common.schemas import Pagination, PaginationMeta
from app.moderation.exceptions import RoleApplicationAlreadyReviewedException
from app.moderation.repositories import RoleApplicationDAO
from app.sellers.services.onboarding import SellerService


class RoleApplicationService:
    @classmethod
    async def create_application(cls,
                                 session: AsyncSession,
                                 *,
                                 user: User,
                                 application: RoleApplicationCreate) -> RoleApplication:
        # TODO FIX RACE CONDITIONS
        if application.requested_role in {RoleEnum.ADMIN, RoleEnum.MODERATOR}:
            raise ForbiddenException()

        exists_application = await RoleApplicationDAO.get_latest(session,
                                                                 user_id=user.id,
                                                                 role=application.requested_role)

        if exists_application:
            if exists_application.status == ReviewStatus.PENDING:
                raise RoleApplicationAlreadyExistsException()

            if exists_application.status == ReviewStatus.APPROVED:
                if await UserDAO.has_role(session,
                                          user_id=user.id,
                                          role=application.requested_role):
                    raise RoleAlreadyAssignedException()

            if exists_application.status == ReviewStatus.REJECTED:
                retry_at = exists_application.updated_at + timedelta(days=7)
                now = datetime.now(UTC)

                if now < retry_at:
                    remaining = retry_at - now
                    total_seconds = int(remaining.total_seconds())
                    days = total_seconds // 86400
                    hours = (total_seconds % 86400) // 3600
                    raise RoleApplicationRetryTooSoonException(
                        detail=f"Try again in {days} days {hours} hours ."
                    )

        data = application.model_dump()
        data["user_id"] = user.id
        new_application = await RoleApplicationDAO.add(
            session,
            **data,
        )

        return new_application

    @classmethod
    async def get_applications(cls,
                               session: AsyncSession,
                               *,
                               filters: RoleApplicationFilter,
                               pagination: Pagination,
                               user_id: int | None = None
                               ) -> tuple[list[RoleApplication], PaginationMeta]:

        applications, total_items = await RoleApplicationDAO.get_applications(session,
                                                                             filters=filters,
                                                                             user_id=user_id,
                                                                             limit=pagination.limit,
                                                                             offset=pagination.offset)

        total_pages = ceil(total_items / pagination.size)
        meta = PaginationMeta(
            page=pagination.page,
            size=pagination.size,
            total_pages=total_pages,
        )
        return applications, meta


class ModeratorRoleApplicationService:

    @classmethod
    async def reject_application(cls,
                                 session: AsyncSession,
                                 *,
                                 application_id: int,
                                 moderator_id: int,
                                 rejection_reason: str) -> RoleApplication | None:
        updated_application = await RoleApplicationDAO.update_application(
            session,
            application_id=application_id,
            status=ReviewStatus.REJECTED,
            reviewer_id=moderator_id,
            rejection_reason=rejection_reason,
        )

        if not updated_application:
            raise RoleApplicationAlreadyReviewedException()

        return updated_application

    @classmethod
    async def approve_application(cls,
                                 session: AsyncSession,
                                 *,
                                 moderator_id: int,
                                 application_id: int) -> RoleApplication | None:

        role_service = {
            RoleEnum.SELLER: SellerService,
        }

        updated_application = await RoleApplicationDAO.update_application(
            session,
            application_id=application_id,
            status=ReviewStatus.APPROVED,
            reviewer_id=moderator_id,
        )

        if not updated_application:
            raise RoleApplicationAlreadyReviewedException()

        await role_service[updated_application.requested_role].become(session,
                                                              user_id=updated_application.user_id,)

        return updated_application






