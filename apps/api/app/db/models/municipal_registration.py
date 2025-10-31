"""
Municipal Registration model for storing client municipal registrations (ISS).
"""

from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.models.base import Base
from app.schemas.municipal_registration import MunicipalRegistrationStatus, StateCode


class MunicipalRegistration(Base):
    """
    Municipal Registration model.
    Represents a municipal registration (Inscrição Municipal / CCM) for a client.
    Used primarily for ISS (Imposto Sobre Serviços) purposes.
    """

    __tablename__ = "municipal_registrations"

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

    # Location details
    city = Column(
        String(100),
        nullable=False,
        index=True,
        comment="Cidade",
    )
    state = Column(
        Enum(StateCode),
        nullable=False,
        index=True,
        comment="Estado (UF)",
    )

    # Registration details
    registration_number = Column(
        String(50),
        nullable=False,
        index=True,
        comment="Número da inscrição municipal (CCM)",
    )
    issue_date = Column(
        Date,
        nullable=False,
        comment="Data de emissão",
    )
    status = Column(
        Enum(MunicipalRegistrationStatus),
        default=MunicipalRegistrationStatus.PENDENTE,
        nullable=False,
        index=True,
        comment="Status da inscrição",
    )
    notes = Column(
        Text,
        nullable=True,
        comment="Notas adicionais",
    )

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    # Relationships
    client = relationship("Client", back_populates="municipal_registrations")

    # Constraints and indexes
    __table_args__ = (
        # Registration number should be unique per city/state
        UniqueConstraint(
            "city",
            "state",
            "registration_number",
            name="uq_city_state_registration",
        ),

        # Composite indexes for common queries
        Index("ix_mun_reg_client_status", "client_id", "status"),
        Index("ix_mun_reg_state_city", "state", "city"),
    )

    def __repr__(self) -> str:
        return (
            f"<MunicipalRegistration(id={self.id}, "
            f"city={self.city}, "
            f"state={self.state}, "
            f"number={self.registration_number}, "
            f"status={self.status})>"
        )
