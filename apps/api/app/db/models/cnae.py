"""
CNAE model for storing client CNAEs (economic activities).
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, String, Boolean, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.models.base import Base
from app.schemas.cnae import CnaeType


class Cnae(Base):
    """
    CNAE model.
    Represents a CNAE (Classificação Nacional de Atividades Econômicas) for a client.
    Each client can have one primary CNAE and multiple secondary CNAEs.
    """

    __tablename__ = "cnaes"

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

    # CNAE details
    cnae_code = Column(
        String(10),
        nullable=False,
        index=True,
        comment="Código CNAE (formato: 0000-0/00)",
    )
    description = Column(
        String(500),
        nullable=False,
        comment="Descrição da atividade",
    )
    cnae_type = Column(
        Enum(CnaeType),
        default=CnaeType.SECUNDARIO,
        nullable=False,
        index=True,
        comment="Tipo: principal ou secundário",
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
        comment="Se o CNAE está ativo",
    )

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    client = relationship("Client", back_populates="cnaes")

    # Constraints and indexes
    __table_args__ = (
        # Each CNAE code must be unique per client
        UniqueConstraint("client_id", "cnae_code", name="uq_client_cnae"),

        # Composite index for queries
        Index("ix_cnaes_client_type", "client_id", "cnae_type"),
        Index("ix_cnaes_client_active", "client_id", "is_active"),

        # Note: The constraint for "only one primary CNAE per client" is enforced
        # at the application/repository level, not database level, to allow more
        # flexible error handling
    )

    def __repr__(self) -> str:
        return (
            f"<Cnae(id={self.id}, "
            f"code={self.cnae_code}, "
            f"type={self.cnae_type}, "
            f"active={self.is_active})>"
        )
