"""Database models."""

# Import all models here to ensure they are registered with Base.metadata
from app.db.models.audit import AuditLog  # noqa: F401
from app.db.models.base import Base  # noqa: F401
from app.db.models.client import Client, ClientStatus, RegimeTributario, TipoEmpresa  # noqa: F401
from app.db.models.user import User, UserRole  # noqa: F401

__all__ = ["Base", "User", "UserRole", "AuditLog", "Client", "ClientStatus", "RegimeTributario", "TipoEmpresa"]
