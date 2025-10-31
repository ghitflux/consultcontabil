"""Cash Flow Report Service - Fluxo de Caixa."""

from datetime import date
from decimal import Decimal

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.finance import FinancialTransaction, PaymentStatus, TransactionType
from app.services.report.base import BaseReportService


class CashFlowReportService(BaseReportService):
    """Service for generating Cash Flow reports."""

    async def generate_data(self, filters: dict) -> dict:
        """
        Generate Cash Flow report data.

        Filters:
            period_start: Start date
            period_end: End date
            client_ids: Optional list of client IDs to filter

        Returns:
            Dictionary with cash flow data structure
        """
        period_start = filters["period_start"].replace(day=1)
        period_end = filters["period_end"].replace(day=1)
        client_ids = filters.get("client_ids")

        # Build conditions
        conditions = [
            FinancialTransaction.deleted_at.is_(None),
        ]

        if client_ids:
            conditions.append(FinancialTransaction.client_id.in_(client_ids))

        # Get all transactions in period grouped by month
        stmt = (
            select(
                FinancialTransaction.reference_month,
                FinancialTransaction.transaction_type,
                func.sum(FinancialTransaction.amount).label("total"),
            )
            .where(
                and_(
                    *conditions,
                    FinancialTransaction.reference_month >= period_start,
                    FinancialTransaction.reference_month <= period_end,
                    FinancialTransaction.payment_status.in_([
                        PaymentStatus.PAGO,
                    ]),
                )
            )
            .group_by(FinancialTransaction.reference_month, FinancialTransaction.transaction_type)
            .order_by(FinancialTransaction.reference_month)
        )

        result = await self.db.execute(stmt)
        rows = result.all()

        # Organize data by period
        period_data = {}
        for row in rows:
            month = row.reference_month.strftime("%Y-%m")
            if month not in period_data:
                period_data[month] = {
                    "entradas": Decimal("0.00"),
                    "saidas": Decimal("0.00"),
                }

            if row.transaction_type == TransactionType.RECEITA:
                period_data[month]["entradas"] += row.total
            elif row.transaction_type == TransactionType.DESPESA:
                period_data[month]["saidas"] += row.total

        # Build periods list with accumulated balance
        periods = []
        current_month = period_start
        saldo_anterior = Decimal("0.00")
        total_entradas = Decimal("0.00")
        total_saidas = Decimal("0.00")

        while current_month <= period_end:
            month_str = current_month.strftime("%Y-%m")
            data = period_data.get(month_str, {"entradas": Decimal("0.00"), "saidas": Decimal("0.00")})

            entradas = data["entradas"]
            saidas = data["saidas"]
            saldo_inicial = saldo_anterior
            saldo_final = saldo_inicial + entradas - saidas

            periods.append({
                "periodo": month_str,
                "entradas": float(entradas),
                "saidas": float(saidas),
                "saldo_inicial": float(saldo_inicial),
                "saldo_final": float(saldo_final),
            })

            saldo_anterior = saldo_final
            total_entradas += entradas
            total_saidas += saidas

            # Move to next month
            if current_month.month == 12:
                current_month = date(current_month.year + 1, 1, 1)
            else:
                current_month = date(current_month.year, current_month.month + 1, 1)

        return {
            "periods": periods,
            "total_entradas": float(total_entradas),
            "total_saidas": float(total_saidas),
            "saldo_final_periodo": float(saldo_anterior),
        }

    def _get_charts_config(self) -> list[dict]:
        """Get chart configurations for Cash Flow report."""
        return [
            {
                "type": "line",
                "title": "Fluxo de Caixa",
                "data_key": "periodo",
                "series": [
                    {"key": "entradas", "label": "Entradas", "color": "#00bcd4"},
                    {"key": "saidas", "label": "Saídas", "color": "#f44336"},
                    {"key": "saldo_final", "label": "Saldo", "color": "#4caf50"},
                ],
            }
        ]

    def _get_summary(self, filters: dict, data: dict) -> dict:
        """Generate summary for Cash Flow report."""
        return {
            "period": f"{filters['period_start'].isoformat()} a {filters['period_end'].isoformat()}",
            "total_inflows": data["total_entradas"],
            "total_outflows": data["total_saidas"],
            "net_flow": data["total_entradas"] - data["total_saidas"],
        }

    def _count_records(self, data: dict) -> int:
        """Count total records in Cash Flow report."""
        return len(data.get("periods", []))

