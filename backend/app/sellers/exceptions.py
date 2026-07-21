from app.core.app_exceptions import AppException
from app.core.http_exceptions import ConflictException


class RolesNotInitializedException(AppException):
    """Required roles are not initialized in the database."""

class StoreNameAlreadyExistsException(ConflictException):
    error_code = "STORE_NAME_ALREADY_EXISTS"
    detail = "Store with this name already exists"
