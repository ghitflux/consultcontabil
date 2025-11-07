"""
Obligation Template model for auto-suggesting obligations based on client configuration.
"""

from enum import Enum
from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import ENUM, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base, TimestampMixin, UUIDMixin
from app.db.models.client import RegimeTributario


class ObligationPeriodicidade(str, Enum):
    """Obligation periodicity enum."""

    MENSAL = "mensal"
    ANUAL = "anual"


class ServicoContratado(str, Enum):
    """Contracted service type enum."""

    FISCAL = "fiscal"
    CONTABIL = "contabil"
    PESSOAL = "pessoal"


class ObligationTemplate(Base, UUIDMixin, TimestampMixin):
    """Obligation template model for auto-suggestion."""

    __tablename__ = "obligations_templates"

    # Template info
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Filters for auto-suggestion
    regime_tributario: Mapped[RegimeTributario] = mapped_column(
        ENUM(RegimeTributario, name="regime_tributario", create_type=False),
        nullable=False,
        index=True,
    )
    servico_contratado: Mapped[ServicoContratado] = mapped_column(
        ENUM(ServicoContratado, name="servico_contratado", create_type=False),
        nullable=False,
        index=True,
    )
    periodicidade: Mapped[ObligationPeriodicidade] = mapped_column(
        ENUM(ObligationPeriodicidade, name="obligation_periodicidade", create_type=False),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<ObligationTemplate {self.nome} ({self.regime_tributario}/{self.servico_contratado})>"
