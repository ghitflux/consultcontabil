"""
Obligation model for storing fiscal obligations.
"""

from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.models.base import Base
from app.schemas.obligation import ObligationPriority, ObligationStatus


class Obligation(Base):
    """
    Obligation model.
    Represents a fiscal obligation for a client.
    """

    __tablename__ = "obligations"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Foreign keys
    client_id = Column(
        UUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Cliente associado",
    )
    obligation_type_id = Column(
        UUID(as_uuid=True),
        ForeignKey("obligation_types.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment="Tipo de obrigação",
    )

    # Obligation details
    due_date = Column(Date, nullable=False, index=True, comment="Data de vencimento")
    status = Column(
        SQLEnum(
            ObligationStatus,
            name="obligationstatus",
            create_type=False,
            native_enum=False,
            values_callable=lambda x: [e.value for e in ObligationStatus]
        ),
        default=ObligationStatus.PENDENTE,
        nullable=False,
        index=True,
        comment="Status da obrigação",
    )
    priority = Column(
        SQLEnum(
            ObligationPriority,
            name="obligationpriority",
            create_type=False,
            native_enum=False,
            values_callable=lambda x: [e.value for e in ObligationPriority]
        ),
        default=ObligationPriority.MEDIA,
        nullable=False,
        comment="Prioridade",
    )

    description = Column(Text, nullable=True, comment="Descrição adicional")

    # Completion info
    receipt_url = Column(
        String(500), nullable=True, comment="URL do comprovante"
    )
    completed_at = Column(
        DateTime(timezone=True), nullable=True, comment="Data/hora de conclusão"
    )
    completed_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="Usuário que concluiu",
    )

    # Timestamps
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(
        DateTime(timezone=True), nullable=True, comment="Soft delete"
    )

    # Relationships
    client = relationship("Client", back_populates="obligations")
    obligation_type = relationship("ObligationType")
    completed_by_user = relationship("User", foreign_keys=[completed_by])
    events = relationship(
        "ObligationEvent",
        back_populates="obligation",
        cascade="all, delete-orphan",
        order_by="ObligationEvent.created_at.desc()",
    )

    # Table arguments (indexes)
    __table_args__ = (
        Index("idx_obligations_client_due", "client_id", "due_date"),
        Index("idx_obligations_status_due", "status", "due_date"),
        Index("idx_obligations_type_status", "obligation_type_id", "status"),
    )

    def __repr__(self):
        return f"<Obligation {self.id}: {self.status} - {self.due_date}>"

    @property
    def is_overdue(self) -> bool:
        """Check if obligation is overdue."""
        if self.status in [ObligationStatus.CONCLUIDA, ObligationStatus.CANCELADA]:
            return False

        today = date.today()
        return self.due_date < today

    @property
    def days_until_due(self) -> int:
        """Calculate days until due date (negative if overdue)."""
        today = date.today()
        delta = self.due_date - today
        return delta.days

    def can_be_completed(self) -> bool:
        """Check if obligation can be marked as completed."""
        return self.status not in [
            ObligationStatus.CONCLUIDA,
            ObligationStatus.CANCELADA,
        ]

    def mark_as_completed(self, user_id: UUID, receipt_url: str) -> None:
        """
        Mark obligation as completed.

        Args:
            user_id: User who completed the obligation
            receipt_url: URL of the uploaded receipt
        """
        if not self.can_be_completed():
            raise ValueError(f"Cannot complete obligation in status: {self.status}")

        self.status = ObligationStatus.CONCLUIDA
        self.completed_at = datetime.utcnow()
        self.completed_by = user_id
        self.receipt_url = receipt_url

    def cancel(self) -> None:
        """Cancel the obligation."""
        if self.status == ObligationStatus.CONCLUIDA:
            raise ValueError("Cannot cancel completed obligation")

        self.status = ObligationStatus.CANCELADA

    def update_status_by_due_date(self) -> bool:
        """
        Update status to ATRASADA if overdue.

        Returns:
            bool: True if status was changed, False otherwise
        """
        if self.is_overdue and self.status == ObligationStatus.PENDENTE:
            self.status = ObligationStatus.ATRASADA
            return True

        return False

    def calculate_priority(self) -> ObligationPriority:
        """
        Calculate priority based on days until due.

        Returns:
            ObligationPriority: Calculated priority
        """
        days = self.days_until_due

        if days < 0:
            return ObligationPriority.URGENTE
        elif days <= 3:
            return ObligationPriority.ALTA
        elif days <= 7:
            return ObligationPriority.MEDIA
        else:
            return ObligationPriority.BAIXA
