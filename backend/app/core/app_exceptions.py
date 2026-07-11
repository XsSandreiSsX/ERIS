class AppException(Exception):
    detail = "Internal Server Error"

    def __init__(self, detail: str | None = None) -> None:
        if detail is not None:
            self.detail = detail


class UnknownFieldError(AppException):
    """Raised when an unknown field is encountered"""


class NoFilterError(AppException):
    """Raised when no filter is applied"""


class NothingToUpdateError(AppException):
    """Raised when no fields are passed for update"""