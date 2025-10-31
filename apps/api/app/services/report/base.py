"""Base Report Service - Abstract base class for all report services."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.transaction import TransactionRepository


class BaseReportService(ABC):
    """Abstract base class for report services."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.transaction_repo = TransactionRepository(db)

    @abstractmethod
    async def generate_data(self, filters: dict[str, Any]) -> dict[str, Any]:
        """
        Generate report data based on filters.

        Args:
            filters: Dictionary with filter parameters

        Returns:
            Dictionary with report data
        """
        raise NotImplementedError

    async def preview(self, filters: dict[str, Any]) -> dict[str, Any]:
        """
        Generate preview data for the report with chart configurations.

        Args:
            filters: Dictionary with filter parameters

        Returns:
            Dictionary with preview data and chart configs
        """
        data = await self.generate_data(filters)

        return {
            "data": data,
            "charts_config": self._get_charts_config(),
            "summary": self._get_summary(filters, data),
            "record_count": self._count_records(data),
        }

    def validate_filters(self, filters: dict[str, Any]) -> bool:
        """
        Validate report filters.

        Args:
            filters: Dictionary with filter parameters

        Returns:
            True if valid, False otherwise
        """
        # Basic validation
        if "period_start" not in filters or "period_end" not in filters:
            return False

        period_start = filters["period_start"]
        period_end = filters["period_end"]

        if period_start > period_end:
            return False

        return True

    def _get_charts_config(self) -> Optional[list[dict[str, Any]]]:
        """
        Get default chart configurations for this report type.

        Returns:
            List of chart configurations or None
        """
        return None

    def _get_summary(
        self, filters: dict[str, Any], data: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """
        Generate summary information for the report.

        Args:
            filters: Report filters
            data: Report data

        Returns:
            Dictionary with summary or None
        """
        return None

    def _count_records(self, data: dict[str, Any]) -> int:
        """
        Count total records in the report data.

        Args:
            data: Report data

        Returns:
            Number of records
        """
        return 0

