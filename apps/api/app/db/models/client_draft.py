"""
Client Draft model for temporary form data storage.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base, TimestampMixin, UUIDMixin


class ClientDraft(Base, UUIDMixin, TimestampMixin):
    """Client draft model for auto-save functionality."""

    __tablename__ = "client_drafts"

    # User who owns this draft (one draft per user)
    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # One draft per user
        index=True,
    )

    # Draft data stored as JSONB
    draft_data: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Optional notes
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationship
    user = relationship("User", back_populates="client_draft")

    def __repr__(self) -> str:
        return f"<ClientDraft user_id={self.user_id} updated={self.updated_at}>"
