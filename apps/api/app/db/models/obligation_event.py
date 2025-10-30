"""
ObligationEvent model for tracking obligation history/timeline.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.models.base import Base


class ObligationEvent(Base):
    """
    Obligation Event model.
    Tracks all events/actions performed on an obligation (timeline).
    """

    __tablename__ = "obligation_events"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Foreign keys
    obligation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("obligations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Obrigação associada",
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="Usuário que executou a ação",
    )

    # Event details
    event_type = Column(
        String(50), nullable=False, comment="Tipo de evento (created, started, completed, etc)"
    )
    description = Column(Text, nullable=False, comment="Descrição do evento")
    extra_data = Column(
        JSONB, nullable=True, comment="Dados adicionais do evento (JSON)"
    )

    # Timestamps
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # Relationships
    obligation = relationship("Obligation", back_populates="events")
    user = relationship("User")

    def __repr__(self):
        return f"<ObligationEvent {self.id}: {self.event_type}>"

    @classmethod
    def create_event(
        cls,
        obligation_id: UUID,
        event_type: str,
        description: str,
        user_id: UUID | None = None,
        extra_data: dict | None = None,
    ) -> "ObligationEvent":
        """
        Factory method to create an event.

        Args:
            obligation_id: Obligation ID
            event_type: Type of event
            description: Event description
            user_id: User who triggered the event (optional)
            extra_data: Additional data (optional)

        Returns:
            ObligationEvent: New event instance
        """
        return cls(
            obligation_id=obligation_id,
            event_type=event_type,
            description=description,
            user_id=user_id,
            extra_data=extra_data,
        )


# Event type constants for consistency
class ObligationEventType:
    """Constants for obligation event types."""

    CREATED = "created"
    UPDATED = "updated"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELED = "canceled"
    STATUS_CHANGED = "status_changed"
    PRIORITY_CHANGED = "priority_changed"
    DUE_DATE_CHANGED = "due_date_changed"
    RECEIPT_UPLOADED = "receipt_uploaded"
    COMMENT_ADDED = "comment_added"
    ASSIGNED = "assigned"
    REMINDER_SENT = "reminder_sent"
