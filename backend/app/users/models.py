from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.annotations import IntPk, CreatedAt, UpdatedAt
from app.core.database import Base
from app.users.config import Limits


class User(Base):
    __tablename__ = "users"

    id: Mapped[IntPk]

    email: Mapped[str] = mapped_column(
        String(Limits.EMAIL_MAX_LENGTH),
        unique=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(Limits.PASSWORD_MAX_LENGTH)
    )

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]


class UserSession(Base):
    __tablename__ = "user_sessions"

    id: Mapped[IntPk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    jti: Mapped[str] = mapped_column(UUID)

    created_at: Mapped[CreatedAt]
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )

