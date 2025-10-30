"""
Base strategy for obligation rules.
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import List

from app.db.models.client import Client
from app.db.models.obligation_type import ObligationType
from app.schemas.obligation import ObligationPriority


class ObligationRule(ABC):
    """
    Base class for obligation generation rules.

    Each concrete implementation defines rules for a specific
    type of company (commerce, service, industry, MEI).
    """

    @abstractmethod
    def get_applicable_type_codes(self, client: Client) -> List[str]:
        """
        Returns obligation type codes applicable to this client.

        Args:
            client: Client model instance

        Returns:
            List of obligation type codes (e.g., ["DAS_MENSAL", "DEFIS_ANUAL"])
        """
        pass

    def calculate_due_date(
        self,
        obligation_type: ObligationType,
        reference_month: date
    ) -> date:
        """
        Calculate due date for given type and month.

        Default implementation uses the day_of_month from obligation_type.
        Can be overridden for custom logic.

        Args:
            obligation_type: ObligationType instance
            reference_month: Reference month (first day)

        Returns:
            Calculated due date
        """
        day = obligation_type.day_of_month or 20  # Default to 20th

        # Due date is in the next month
        if reference_month.month == 12:
            year = reference_month.year + 1
            month = 1
        else:
            year = reference_month.year
            month = reference_month.month + 1

        # Ensure day is valid for the month
        if month == 2:
            max_day = 28  # February
        elif month in [4, 6, 9, 11]:
            max_day = 30  # 30-day months
        else:
            max_day = 31  # 31-day months

        day = min(day, max_day)

        return date(year, month, day)

    def get_priority(
        self,
        obligation_type: ObligationType,
        due_date: date
    ) -> ObligationPriority:
        """
        Calculate priority based on type and due date.

        Default implementation based on days until due.
        Can be overridden for custom logic.

        Args:
            obligation_type: ObligationType instance
            due_date: Due date

        Returns:
            Calculated priority
        """
        today = date.today()
        days_until_due = (due_date - today).days

        if days_until_due < 0:
            return ObligationPriority.URGENTE
        elif days_until_due <= 3:
            return ObligationPriority.ALTA
        elif days_until_due <= 7:
            return ObligationPriority.MEDIA
        else:
            return ObligationPriority.BAIXA

    def should_generate_for_client(self, client: Client) -> bool:
        """
        Check if obligations should be generated for this client.

        Default checks: client is active and not deleted.
        Can be overridden for additional checks.

        Args:
            client: Client instance

        Returns:
            True if should generate, False otherwise
        """
        from app.db.models.client import ClientStatus

        return (
            client.status == ClientStatus.ATIVO and
            client.deleted_at is None
        )
