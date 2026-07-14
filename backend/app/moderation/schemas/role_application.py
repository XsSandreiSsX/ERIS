from pydantic import BaseModel, Field

from app.users.permissions import RoleEnum


class RoleApplicationCreate(BaseModel):
    requested_role: RoleEnum = Field(default=RoleEnum.SELLER)
    full_name: str = Field(max_length=128)
    phone: str = Field(min_length=10, max_length=16)