from typing import Annotated

from fastapi import Depends

from app.moderation.schemas.role_application import RoleApplicationFilter

RoleApplicationFilterDep = Annotated[RoleApplicationFilter, Depends()]
