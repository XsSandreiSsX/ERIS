from common.repositories import BaseDAO
from moderation.models import RoleApplication


class RoleApplicationDAO(BaseDAO):
    model = RoleApplication
