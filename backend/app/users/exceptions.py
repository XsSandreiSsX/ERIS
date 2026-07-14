from starlette import status

from app.core.http_exceptions import ConflictException, HttpException


class EmailExistsException(ConflictException):
    error_code = "USER_EMAIL_EXISTS"
    detail = "A user with this email already exists."


class NotAuthenticatedException(HttpException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "NOT_AUTHENTICATED"
    detail = "Authorization required"

class InvalidCredentialsException(NotAuthenticatedException):
    error_code = "INVALID_CREDENTIALS"
    detail = "Invalid email or password"


class ExpiredTokenException(NotAuthenticatedException):
    error_code = "EXPIRED_TOKEN"
    detail = "Token has expired"


class ForbiddenException(HttpException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "FORBIDDEN"
    detail = "You do not have permission to perform this action"