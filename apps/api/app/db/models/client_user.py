"""
ClientUser model for client-user relationship.
"""

from enum import Enum
from uuid import uuid4

from sqlalchemy import Enum as SQLEnum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base, TimestampMixin, UUIDMixin


class ClientAccessLevel(str, Enum):
    """Access level for client-user relationship."""

    OWNER = "OWNER"
    MANAGER = "MANAGER"
    VIEWER = "VIEWER"


class ClientUser(Base, UUIDMixin, TimestampMixin):
    """ClientUser model for N:N relationship between clients and users."""

    __tablename__ = "client_users"

    client_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    access_level: Mapped[ClientAccessLevel] = mapped_column(
        SQLEnum(ClientAccessLevel, name="client_access_level", create_type=False),
        nullable=False,
        default=ClientAccessLevel.VIEWER
    )

    # Relationships
    client = relationship("Client", back_populates="client_users")
    user = relationship("User", back_populates="client_users")

    __table_args__ = (
        UniqueConstraint("client_id", "user_id", name="uq_client_users_client_user"),
    )

    def __repr__(self) -> str:
        return f"<ClientUser client_id={self.client_id} user_id={self.user_id} level={self.access_level}>"
