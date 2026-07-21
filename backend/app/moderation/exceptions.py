from app.core.http_exceptions import ConflictException


class RoleApplicationAlreadyExistsException(ConflictException):
    error_code = "ROLE_APPLICATION_EXISTS"
    detail = "A pending application for this role already exists."


class RoleApplicationRetryTooSoonException(ConflictException):
    error_code = "ROLE_APPLICATION_RETRY_TOO_SOON"
    detail = "Try again a little later."


class RoleApplicationAlreadyReviewedException(ConflictException):
    error_code = "ROLE_APPLICATION_ALREADY_REVIEWED"
    detail = "Role application has already been reviewed."