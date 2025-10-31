"""Revenue by Client Report Service."""

from decimal import Decimal

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client import Client
from app.db.models.finance import FinancialTransaction, PaymentStatus, TransactionType
from app.services.report.base import BaseReportService


class RevenueByClientReportService(BaseReportService):
    """Service for generating Revenue by Client reports."""

    async def generate_data(self, filters: dict) -> dict:
        """
        Generate Revenue by Client report data.

        Filters:
            period_start: Start date
            period_end: End date
            client_ids: Optional list of client IDs to filter

        Returns:
            Dictionary with revenue grouped by client
        """
        period_start = filters["period_start"].replace(day=1)
        period_end = filters["period_end"].replace(day=1)
        client_ids = filters.get("client_ids")

        # Build conditions
        conditions = [
            FinancialTransaction.transaction_type == TransactionType.RECEITA,
            FinancialTransaction.payment_status == PaymentStatus.PAGO,
            FinancialTransaction.deleted_at.is_(None),
            FinancialTransaction.reference_month >= period_start,
            FinancialTransaction.reference_month <= period_end,
        ]

        if client_ids:
            conditions.append(FinancialTransaction.client_id.in_(client_ids))

        # Get revenue grouped by client
        stmt = (
            select(
                Client.id,
                Client.razao_social,
                Client.cnpj,
                func.sum(FinancialTransaction.amount).label("total_receita"),
            )
            .join(Client, FinancialTransaction.client_id == Client.id)
            .where(and_(*conditions))
            .group_by(Client.id, Client.razao_social, Client.cnpj)
            .order_by(func.sum(FinancialTransaction.amount).desc())
        )

        result = await self.db.execute(stmt)
        rows = result.all()

        # Calculate total revenue
        total_receita = sum(row.total_receita for row in rows) or Decimal("0.00")

        # Format client revenues
        clients = []
        for row in rows:
            percentual = (
                float(row.total_receita / total_receita * 100) if total_receita > 0 else 0.0
            )
            clients.append({
                "client_id": str(row.id),
                "client_name": row.razao_social,
                "client_cnpj": row.cnpj,
                "total_receita": float(row.total_receita),
                "percentual_total": round(percentual, 2),
            })

        return {
            "clients": clients,
            "total_receita": float(total_receita),
        }

    def _get_charts_config(self) -> list[dict]:
        """Get chart configurations for Revenue by Client report."""
        return [
            {
                "type": "bar",
                "title": "Receita por Cliente",
                "data_key": "total_receita",
                "x_axis_key": "client_name",
                "orientation": "horizontal",
            },
            {
                "type": "pie",
                "title": "Distribuição de Receitas",
                "data_key": "percentual_total",
                "label_key": "client_name",
            },
        ]

    def _get_summary(self, filters: dict, data: dict) -> dict:
        """Generate summary for Revenue by Client report."""
        return {
            "period": f"{filters['period_start'].isoformat()} a {filters['period_end'].isoformat()}",
            "total_clients": len(data["clients"]),
            "total_revenue": data["total_receita"],
            "average_per_client": round(
                data["total_receita"] / len(data["clients"]) if data["clients"] else 0, 2
            ),
        }

    def _count_records(self, data: dict) -> int:
        """Count total records in Revenue by Client report."""
        return len(data.get("clients", []))

