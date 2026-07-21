class BaseRoleService:
    @classmethod
    async def become(cls,
                     session,
                     *,
                     user_id: int) -> None:
        raise NotImplementedError