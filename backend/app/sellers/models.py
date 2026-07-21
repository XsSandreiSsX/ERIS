from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.common.annotations import CreatedAt, UpdatedAt


class SellerProfile(Base):
    __tablename__ = "seller_profiles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="seller_profile",
        lazy="raise",
    )

    store_name: Mapped[str] = mapped_column(String(32))
    store_slug: Mapped[str] = mapped_column(String(64),
                                            unique=True)
    description: Mapped[str | None] = mapped_column(String(256), default="")

    avatar_id: Mapped[int | None] = mapped_column(default=None)
    banner_id: Mapped[int | None] = mapped_column(default=None)

    #achievements:  TODO

    products_count: Mapped[int] = mapped_column(default=0)
    sales_count: Mapped[int] = mapped_column(default=0)
    average_rating: Mapped[float] = mapped_column(default=0)
    reviews_count: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]