from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.common.deps import SessionDep, ReadSessionDep, PaginationDep
from app.moderation.schemas.role_application import RoleApplicationCreate, RoleApplicationCreateResponse, RoleApplicationResponse
from app.users.deps import GetUserDep
from app.common.schemas import SuccessResponse, ErrorResponse
from app.moderation.service import RoleApplicationService
from app.common.schemas import PaginatedResponse
from app.moderation.deps import RoleApplicationFilterDep

role_application_router = APIRouter()


@role_application_router.post("/",
                              status_code=status.HTTP_201_CREATED,
                              response_model=SuccessResponse[RoleApplicationCreateResponse],
                              responses={status.HTTP_409_CONFLICT: {"model": ErrorResponse},
                                         status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
                                         status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},})
async def create_role_application(
        session: SessionDep,
        user: GetUserDep,
        application: RoleApplicationCreate
):
    new_application = await RoleApplicationService.create_application(session,
                                                                      user=user,
                                                                      application=application)

    return SuccessResponse(
        data=RoleApplicationCreateResponse.model_validate(new_application, from_attributes=True),
    )


@role_application_router.get("/me",
                             status_code=status.HTTP_200_OK,
                             response_model=SuccessResponse[PaginatedResponse[RoleApplicationResponse]],
                             responses={status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse}})
async def get_my_applications(
        session: ReadSessionDep,
        user: GetUserDep,
        filters: RoleApplicationFilterDep,
        pagination: PaginationDep
):
    my_applications, meta = await RoleApplicationService.get_applications(
        session,
        user_id=user.id,
        filters=filters,
        pagination=pagination
    )

    return SuccessResponse(
        data=PaginatedResponse(
            items=[RoleApplicationResponse.model_validate(item, from_attributes=True) for item in my_applications],
            meta=meta
        ),
    )