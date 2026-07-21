from app.common.service import BaseRoleService
from app.users.repositories import RoleDAO
from app.users.permissions import RoleEnum
from app.users.repositories import UserRoleDAO
from app.sellers.exceptions import RolesNotInitializedException
from app.sellers.repositories import SellerProfileDAO


class SellerService(BaseRoleService):
    @classmethod
    async def become(cls,
                 session,
                 *,
                 user_id: int) -> None:

        seller_role = await RoleDAO.get_by_name(session,
                                                name=RoleEnum.SELLER)

        if not seller_role:
            raise RolesNotInitializedException()

        user_role = await UserRoleDAO.assign(session,
                                            role_id=seller_role.id,
                                            user_id=user_id)

        if not user_role:
            return

        initial_store_name = initial_store_slug = f"store_{user_id}"
        await SellerProfileDAO.create(
            session,
            user_id=user_id,
            store_name=initial_store_name,
            store_slug=initial_store_slug
        )




