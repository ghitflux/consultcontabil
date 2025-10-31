"""Obligation services package."""

from app.services.obligation.processor import ObligationProcessor
from app.services.obligation.generator import ObligationGenerator

__all__ = ["ObligationProcessor", "ObligationGenerator"]
