"""License Report Service."""

from datetime import date, timedelta

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.license import License
from app.services.report.base import BaseReportService


class LicenseReportService(BaseReportService):
    """Service for generating License reports."""

    async def generate_data(self, filters: dict) -> dict:
        """
        Generate License report data.

        Filters:
            period_start: Start date
            period_end: End date
            client_ids: Optional list of client IDs to filter

        Returns:
            Dictionary with license statistics
        """
        client_ids = filters.get("client_ids")
        today = date.today()

        # Build conditions
        conditions = []

        if client_ids:
            conditions.append(License.client_id.in_(client_ids))

        # Get total counts
        count_stmt = select(
            func.count().label("total"),
            func.count().filter(License.status == "ATIVA").label("active"),
            func.count().filter(License.status == "VENCIDA").label("expired"),
        )

        if conditions:
            count_stmt = count_stmt.where(and_(*conditions))

        result = await self.db.execute(count_stmt)
        row = result.one()

        # Count licenses expiring soon (within 30 days)
        expiring_soon_date = today + timedelta(days=30)
        expiring_stmt = (
            select(func.count())
            .where(
                and_(
                    *conditions,
                    License.expiration_date <= expiring_soon_date,
                    License.expiration_date > today,
                    License.status == "ATIVA",
                )
            )
        )
        expiring_count = await self.db.scalar(expiring_stmt) or 0

        # Count renewals in period
        renewals_stmt = (
            select(func.count())
            .where(
                and_(
                    *conditions,
                    License.issue_date >= filters["period_start"],
                    License.issue_date <= filters["period_end"],
                )
            )
        )
        renewals_count = await self.db.scalar(renewals_stmt) or 0

        return {
            "total_licenses": row.total or 0,
            "active": row.active or 0,
            "expiring_soon": expiring_count,
            "expired": row.expired or 0,
            "renewals_in_period": renewals_count,
        }

    def _get_charts_config(self) -> list[dict]:
        """Get chart configurations for License report."""
        return [
            {
                "type": "pie",
                "title": "Licenças por Status",
                "data_key": "count",
                "label_key": "status",
            },
            {
                "type": "bar",
                "title": "Licenças Vencendo em 30 dias",
                "data_key": "expiring_soon",
            },
        ]

    def _get_summary(self, filters: dict, data: dict) -> dict:
        """Generate summary for License report."""
        return {
            "total_licenses": data["total_licenses"],
            "active_rate": round(
                (data["active"] / data["total_licenses"] * 100)
                if data["total_licenses"] > 0
                else 0,
                2,
            ),
            "expiring_soon": data["expiring_soon"],
        }

    def _count_records(self, data: dict) -> int:
        """Count total records in License report."""
        return data.get("total_licenses", 0)

