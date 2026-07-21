from enum import StrEnum


class RoleEnum(StrEnum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    SELLER = "seller"
    COURIER = "courier"
    STOREKEEPER = "storekeeper"


class PermissionEnum(StrEnum):
    PRODUCT_CREATE = "products.create"
    PRODUCT_UPDATE = "products.update"
    PRODUCT_DELETE = "products.delete"

    VIEW_APPLICATIONS = "applications.view"
    MODERATE_APPLICATIONS = "applications.moderate"

    EDIT_SELLER_PROFILE = "seller_profiles.edit"
