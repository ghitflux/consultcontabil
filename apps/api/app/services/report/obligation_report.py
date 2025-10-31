"""Obligation Report Service."""

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.obligation import Obligation
from app.services.report.base import BaseReportService


class ObligationReportService(BaseReportService):
    """Service for generating Obligation reports."""

    async def generate_data(self, filters: dict) -> dict:
        """
        Generate Obligation report data.

        Filters:
            period_start: Start date
            period_end: End date
            client_ids: Optional list of client IDs to filter

        Returns:
            Dictionary with obligation statistics
        """
        client_ids = filters.get("client_ids")

        # Build conditions
        conditions = []

        if client_ids:
            conditions.append(Obligation.client_id.in_(client_ids))

        # Get counts by status
        count_stmt = select(
            func.count().label("total"),
            func.count().filter(Obligation.status == "pendente").label("pending"),
            func.count().filter(Obligation.status == "concluida").label("completed"),
            func.count().filter(Obligation.status == "atrasada").label("overdue"),
            func.count().filter(Obligation.status == "cancelada").label("cancelled"),
        )

        if conditions:
            count_stmt = count_stmt.where(and_(*conditions))

        result = await self.db.execute(count_stmt)
        row = result.one()

        # Calculate compliance rate
        total = row.total or 0
        completed = row.completed or 0
        compliance_rate = (completed / total * 100) if total > 0 else 0.0

        return {
            "compliance_rate": round(compliance_rate, 2),
            "total_obligations": total,
            "pending": row.pending or 0,
            "completed": completed,
            "overdue": row.overdue or 0,
            "cancelled": row.cancelled or 0,
        }

    def _get_charts_config(self) -> list[dict]:
        """Get chart configurations for Obligation report."""
        return [
            {
                "type": "pie",
                "title": "Obrigações por Status",
                "data_key": "count",
                "label_key": "status",
            },
            {
                "type": "bar",
                "title": "Taxa de Compliance",
                "data_key": "compliance_rate",
            },
        ]

    def _get_summary(self, filters: dict, data: dict) -> dict:
        """Generate summary for Obligation report."""
        return {
            "compliance_rate": data["compliance_rate"],
            "total": data["total_obligations"],
            "success_rate": round(
                (data["completed"] / data["total_obligations"] * 100)
                if data["total_obligations"] > 0
                else 0,
                2,
            ),
        }

    def _count_records(self, data: dict) -> int:
        """Count total records in Obligation report."""
        return data.get("total_obligations", 0)

