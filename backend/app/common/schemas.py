from typing import Self, TypeVar, Generic, Any

from pydantic import BaseModel, Field

DataT = TypeVar("T")
DataB = TypeVar("B")


class SuccessResponse(BaseModel, Generic[DataT]):
    data: DataT | None


class ErrorResponse(BaseModel):
    error_code: str
    detail: str


class Pagination(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)

    @property
    def limit(self) -> int:
        return self.size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


class PaginationMeta(BaseModel):
    page: int
    size: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[DataB]):
    items: list[DataB]
    meta: PaginationMeta
