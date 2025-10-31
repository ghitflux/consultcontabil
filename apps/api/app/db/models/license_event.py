"""
License Event model for tracking license history.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.models.base import Base
from app.schemas.license import LicenseEventType


class LicenseEvent(Base):
    """
    License Event model.
    Represents an event in the license lifecycle (created, renewed, expired, etc.).
    Provides complete audit trail for all license changes.
    """

    __tablename__ = "license_events"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Foreign keys
    license_id = Column(
        UUID(as_uuid=True),
        ForeignKey("licenses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Licença associada",
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="Usuário que executou a ação",
    )

    # Event details
    event_type = Column(
        Enum(LicenseEventType),
        nullable=False,
        index=True,
        comment="Tipo de evento",
    )
    description = Column(
        Text,
        nullable=False,
        comment="Descrição do evento",
    )

    # Timestamp
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
        comment="Data/hora do evento",
    )

    # Relationships
    license = relationship("License", back_populates="events")
    user = relationship("User", foreign_keys=[user_id])

    # Indexes
    __table_args__ = (
        Index("ix_license_events_license_created", "license_id", "created_at"),
        Index("ix_license_events_type_created", "event_type", "created_at"),
    )

    def __repr__(self) -> str:
        return (
            f"<LicenseEvent(id={self.id}, "
            f"type={self.event_type}, "
            f"license_id={self.license_id})>"
        )
