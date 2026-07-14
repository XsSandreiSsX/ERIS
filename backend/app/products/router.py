from fastapi import APIRouter, Depends
from starlette import status

from app.users.deps import HasPermission
from app.users.models import User
from app.users.permissions import PermissionEnum

product_router = APIRouter()

has_permission = HasPermission

@product_router.post("/create",
                     status_code=status.HTTP_201_CREATED,)
async def create_product(
        user: User = Depends(has_permission(PermissionEnum.PRODUCT_CREATE))
):
    return {"ok": True}