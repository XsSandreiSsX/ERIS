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

    roles: Mapped[list["Role"]] = relationship(
        secondary="users_roles",
        lazy="raise",
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


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[IntPk]
    name: Mapped[str] = mapped_column(String(255), unique=True)


class Role(Base):
    id: Mapped[IntPk]
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(String(255), unique=True)

    permissions: Mapped[list["Permission"]] = relationship(
        secondary="roles_permissions",
        lazy="raise",
    )


class RolePermission(Base):
    __tablename__ = "roles_permissions"
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"),
                                         primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id", ondelete="CASCADE"),
                                               primary_key=True)


class UserRole(Base):
    __tablename__ = "users_roles"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),
                                         primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"),
                                         primary_key=True)
