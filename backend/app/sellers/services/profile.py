from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from app.sellers.models import SellerProfile
from app.sellers.schemas.profile import SellerProfileUpdate
from app.sellers.exceptions import StoreNameAlreadyExistsException
from app.sellers.repositories import SellerProfileDAO


class SellerProfileService:
    @classmethod
    async def update_profile(cls,
                             session: AsyncSession,
                             *,
                             seller_id: int,
                             payload: SellerProfileUpdate) -> SellerProfile | None:
        data_to_update = payload.model_dump(exclude_unset=True)
        store_name = data_to_update.pop("store_name", None)
        if store_name:
            store_slug = slugify(store_name)
            exists = await SellerProfileDAO.get_by_slug(session,
                                                        slug=store_slug)
            if exists and exists.user_id != seller_id:
                raise StoreNameAlreadyExistsException()

            data_to_update["store_name"] = store_name
            data_to_update["store_slug"] = store_slug

        updated_profile = await SellerProfileDAO.update_profile(
            session,
            user_id=seller_id,
            **data_to_update
        )

        if not updated_profile:
            raise StoreNameAlreadyExistsException()

        return updated_profile

