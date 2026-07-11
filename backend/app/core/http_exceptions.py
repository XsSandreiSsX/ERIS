from starlette import status


class HttpException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = "INTERNAL_SERVER_ERROR"
    detail = "Internal Server Error"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail


class ConflictException(HttpException):
    status_code = status.HTTP_409_CONFLICT
    error_code = "CONFLICT"
    detail = "Обьект уже существует"
