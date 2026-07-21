from fastapi import APIRouter, Depends
from starlette import status

from app.common.deps import ReadSessionDep, PaginationDep, SessionDep
from app.users.deps import HasPermission
from app.users.permissions import PermissionEnum
from app.users.models import User
from app.moderation.deps import RoleApplicationFilterDep
from app.common.schemas import SuccessResponse, PaginatedResponse
from app.moderation.schemas.role_application import RoleApplicationResponse
from app.moderation.service import RoleApplicationService
from app.moderation.service import ModeratorRoleApplicationService
from app.moderation.schemas.role_application import RejectRoleApplication

moderator_role_application_router = APIRouter()
get_moderator_user = HasPermission


@moderator_role_application_router.get("/",
                                       status_code=status.HTTP_200_OK,
                                       response_model=SuccessResponse[PaginatedResponse[RoleApplicationResponse]])
async def get_applications(
        session: ReadSessionDep,
        filters: RoleApplicationFilterDep,
        pagination: PaginationDep,
        user: User = Depends(get_moderator_user(PermissionEnum.VIEW_APPLICATIONS)),
):
    applications, meta = await RoleApplicationService.get_applications(
        session,
        filters=filters,
        pagination=pagination
    )

    return SuccessResponse(
        data=PaginatedResponse(
            items=[RoleApplicationResponse.model_validate(item, from_attributes=True) for item in applications],
            meta=meta
        ),
    )


@moderator_role_application_router.post("/{application_id}/approve/",
                                        status_code=status.HTTP_204_NO_CONTENT)
async def approve_application(
        application_id: int,
        session: SessionDep,
        user: User = Depends(get_moderator_user(PermissionEnum.MODERATE_APPLICATIONS))
):
    await ModeratorRoleApplicationService.approve_application(
        session,
        application_id=application_id,
        moderator_id=user.id,
    )


@moderator_role_application_router.post("/{application_id}/reject/",
                                        status_code=status.HTTP_204_NO_CONTENT)
async def reject_application(
        application_id: int,
        session: SessionDep,
        payload: RejectRoleApplication,
        user: User = Depends(get_moderator_user(PermissionEnum.MODERATE_APPLICATIONS))
) -> None:
    await ModeratorRoleApplicationService.reject_application(
        session,
        application_id=application_id,
        moderator_id=user.id,
        rejection_reason=payload.rejection_reason,
    )
