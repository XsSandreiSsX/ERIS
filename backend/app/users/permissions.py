from enum import StrEnum


class RoleEnum(StrEnum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    SELLER = "seller"
    COURIER = "courier"
    STOREKEEPER = "storekeeper"


class PermissionEnum(StrEnum):
    PRODUCT_CREATE = "seller.product_create"
    PRODUCT_UPDATE = "seller.product_update"
    PRODUCT_DELETE = "seller.product_delete"