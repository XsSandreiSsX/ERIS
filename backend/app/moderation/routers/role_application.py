from fastapi import APIRouter

from app.common.deps import SessionDep
from app.moderation.schemas.role_application import RoleApplicationCreate
from app.users.deps import GetUserDep

role_application_router = APIRouter()

@role_application_router.post("/")
async def create_role_application(
        session: SessionDep,
        user: GetUserDep,
        application: RoleApplicationCreate
):
    ...