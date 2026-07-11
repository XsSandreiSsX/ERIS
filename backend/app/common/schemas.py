from typing import Self, TypeVar, Generic, Any

from pydantic import BaseModel


DataT = TypeVar("DataT")

class SuccessResponse(BaseModel, Generic[DataT]):
    data: DataT | None
    meta: dict[str, Any] | None

    @classmethod
    def empty(cls) -> Self:
        return cls(data=None, meta=None)


class ErrorResponse(BaseModel):
    error_code: str
    detail: str
