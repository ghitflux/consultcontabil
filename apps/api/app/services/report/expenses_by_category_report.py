"""Expenses by Category Report Service."""

from decimal import Decimal

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.finance import FinancialTransaction, PaymentStatus, TransactionType
from app.services.report.base import BaseReportService


class ExpensesByCategoryReportService(BaseReportService):
    """Service for generating Expenses by Category reports."""

    async def generate_data(self, filters: dict) -> dict:
        """
        Generate Expenses by Category report data.

        Filters:
            period_start: Start date
            period_end: End date
            client_ids: Optional list of client IDs to filter

        Returns:
            Dictionary with expenses grouped by category
        """
        period_start = filters["period_start"].replace(day=1)
        period_end = filters["period_end"].replace(day=1)
        client_ids = filters.get("client_ids")

        # Build conditions
        conditions = [
            FinancialTransaction.transaction_type == TransactionType.DESPESA,
            FinancialTransaction.payment_status == PaymentStatus.PAGO,
            FinancialTransaction.deleted_at.is_(None),
            FinancialTransaction.reference_month >= period_start,
            FinancialTransaction.reference_month <= period_end,
        ]

        if client_ids:
            conditions.append(FinancialTransaction.client_id.in_(client_ids))

        # Get expenses grouped by description/category
        stmt = (
            select(
                FinancialTransaction.description,
                func.sum(FinancialTransaction.amount).label("total"),
            )
            .where(and_(*conditions))
            .group_by(FinancialTransaction.description)
            .order_by(func.sum(FinancialTransaction.amount).desc())
        )

        result = await self.db.execute(stmt)
        rows = result.all()

        # Calculate total expenses
        total_despesas = sum(row.total for row in rows) or Decimal("0.00")

        # Format category expenses
        categories = []
        for row in rows:
            percentual = (
                float(row.total / total_despesas * 100) if total_despesas > 0 else 0.0
            )
            categories.append({
                "categoria": row.description or "Sem descrição",
                "total": float(row.total),
                "percentual_total": round(percentual, 2),
            })

        return {
            "categories": categories,
            "total_despesas": float(total_despesas),
        }

    def _get_charts_config(self) -> list[dict]:
        """Get chart configurations for Expenses by Category report."""
        return [
            {
                "type": "pie",
                "title": "Despesas por Categoria",
                "data_key": "percentual_total",
                "label_key": "categoria",
            },
            {
                "type": "bar",
                "title": "Top Despesas",
                "data_key": "total",
                "x_axis_key": "categoria",
                "orientation": "horizontal",
            },
        ]

    def _get_summary(self, filters: dict, data: dict) -> dict:
        """Generate summary for Expenses by Category report."""
        return {
            "period": f"{filters['period_start'].isoformat()} a {filters['period_end'].isoformat()}",
            "total_categories": len(data["categories"]),
            "total_expenses": data["total_despesas"],
        }

    def _count_records(self, data: dict) -> int:
        """Count total records in Expenses by Category report."""
        return len(data.get("categories", []))

