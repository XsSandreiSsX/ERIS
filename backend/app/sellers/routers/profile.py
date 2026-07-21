from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from starlette import status

from app.sellers.schemas.profile import SellerProfileUpdate, SellerProfileUpdateResponse
from app.sellers.services.profile import SellerProfileService
from app.common.deps import SessionDep
from app.common.schemas import SuccessResponse, ErrorResponse
from app.users.deps import HasPermission
from app.users.models import User
from app.users.permissions import PermissionEnum

profile_seller_router = APIRouter()

EditSellerProfileDep = Annotated[User, Depends(HasPermission(PermissionEnum.EDIT_SELLER_PROFILE))]
AvatarFile = Annotated[UploadFile, File(description="Seller avatar",)]

DEFAULT_PROFILE_RESPONSES = {
    status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
    status.HTTP_403_FORBIDDEN: {"model": ErrorResponse}
}


@profile_seller_router.patch("/profile",
                             status_code=status.HTTP_200_OK,
                             response_model=SuccessResponse[SellerProfileUpdateResponse],
                             responses={**DEFAULT_PROFILE_RESPONSES,
                                        status.HTTP_409_CONFLICT: {"model": ErrorResponse}})
async def update_profile(session: SessionDep,
                         payload: SellerProfileUpdate,
                         user: EditSellerProfileDep):
    updated_profile = await SellerProfileService.update_profile(session,
                                              seller_id=user.id,
                                              payload=payload)

    return SuccessResponse(
        data=SellerProfileUpdateResponse.model_validate(updated_profile, from_attributes=True),
    )


@profile_seller_router.patch("/profile/avatar",
                             status_code=status.HTTP_204_NO_CONTENT,
                             responses={**DEFAULT_PROFILE_RESPONSES,})
async def update_profile_avatar(session: SessionDep,
                                avatar: AvatarFile,
                                user: EditSellerProfileDep):
    print(avatar.headers)
    print(avatar.size)
    print(avatar.content_type)
    print(avatar.filename)


@profile_seller_router.get("/{slug}")
async def get_seller_profile(slug: str):
    ...