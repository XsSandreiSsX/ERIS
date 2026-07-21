from datetime import datetime

from pydantic import BaseModel, Field

from app.users.permissions import RoleEnum
from app.moderation.models import ReviewStatus


class RoleApplicationFilter(BaseModel):
    status: ReviewStatus | None = Field(
        default=ReviewStatus.PENDING,
    )
    role: RoleEnum | None = Field(
        default=None
    )


class RoleApplicationCreate(BaseModel):
    requested_role: RoleEnum = Field(default=RoleEnum.SELLER)
    full_name: str = Field(max_length=128)
    phone: str = Field(min_length=10, max_length=16)
    description: str = Field(max_length=512)


class RoleApplicationCreateResponse(BaseModel):
    id: int
    status: ReviewStatus
    created_at: datetime


class RoleApplicationResponse(BaseModel):
    id: int
    user_id: int

    requested_role: RoleEnum
    full_name: str
    phone: str
    description: str

    status: ReviewStatus
    rejection_reason: str | None

    created_at: datetime
    updated_at: datetime


class RejectRoleApplication(BaseModel):
    rejection_reason: str = Field(max_length=1024)