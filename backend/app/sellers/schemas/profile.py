from pydantic import BaseModel, Field


class SellerProfileUpdate(BaseModel):
    store_name: str | None = Field(min_length=3, max_length=32,
                                   default=None)
    description: str | None = Field(min_length=16, max_length=256,
                                    default=None)


class SellerProfileUpdateResponse(BaseModel):
    store_name: str
    store_slug: str
    description: str