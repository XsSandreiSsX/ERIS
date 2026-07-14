from enum import StrEnum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.annotations import IntPk, CreatedAt, UpdatedAt
from app.core.database import Base
from app.users.permissions import RoleEnum


class ReviewStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class RoleApplication(Base):
    __tablename__ = "roles_applications"
    id: Mapped[IntPk]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    requested_role: Mapped[RoleEnum]
    full_name: Mapped[str] = mapped_column(String(128))
    phone: Mapped[str] = mapped_column(String(16))

    status: Mapped[ReviewStatus] = mapped_column(default=ReviewStatus.PENDING)
    rejection_reason: Mapped[str | None]
    reviewed_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]
