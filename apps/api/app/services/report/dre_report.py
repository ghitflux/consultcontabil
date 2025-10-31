"""DRE Report Service - Demonstrativo de Resultados."""

from decimal import Decimal

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.finance import FinancialTransaction, PaymentStatus, TransactionType
from app.services.report.base import BaseReportService


class DREReportService(BaseReportService):
    """Service for generating DRE (Demonstrativo de Resultados) reports."""

    async def generate_data(self, filters: dict) -> dict:
        """
        Generate DRE report data.

        Filters:
            period_start: Start date
            period_end: End date
            client_ids: Optional list of client IDs to filter

        Returns:
            Dictionary with DRE data structure
        """
        period_start = filters["period_start"]
        period_end = filters["period_end"]
        client_ids = filters.get("client_ids")

        # Build conditions
        conditions = [
            FinancialTransaction.payment_status == PaymentStatus.PAGO,
            FinancialTransaction.deleted_at.is_(None),
            FinancialTransaction.reference_month >= period_start.replace(day=1),
            FinancialTransaction.reference_month <= period_end.replace(day=1),
        ]

        if client_ids:
            conditions.append(FinancialTransaction.client_id.in_(client_ids))

        # Calculate total revenue
        revenue_stmt = (
            select(func.sum(FinancialTransaction.amount))
            .where(
                and_(
                    *conditions,
                    FinancialTransaction.transaction_type == TransactionType.RECEITA,
                )
            )
        )
        total_receita = await self.db.scalar(revenue_stmt) or Decimal("0.00")

        # Group revenue by description/category
        revenue_group_stmt = (
            select(
                FinancialTransaction.description,
                func.sum(FinancialTransaction.amount).label("total"),
            )
            .where(
                and_(
                    *conditions,
                    FinancialTransaction.transaction_type == TransactionType.RECEITA,
                )
            )
            .group_by(FinancialTransaction.description)
            .order_by(func.sum(FinancialTransaction.amount).desc())
        )
        revenue_result = await self.db.execute(revenue_group_stmt)
        revenue_items = revenue_result.all()

        # Calculate total expenses (for future use when expenses are tracked)
        expense_stmt = (
            select(func.sum(FinancialTransaction.amount))
            .where(
                and_(
                    *conditions,
                    FinancialTransaction.transaction_type == TransactionType.DESPESA,
                )
            )
        )
        total_despesa = await self.db.scalar(expense_stmt) or Decimal("0.00")

        # Group expenses by description/category
        expense_group_stmt = (
            select(
                FinancialTransaction.description,
                func.sum(FinancialTransaction.amount).label("total"),
            )
            .where(
                and_(
                    *conditions,
                    FinancialTransaction.transaction_type == TransactionType.DESPESA,
                )
            )
            .group_by(FinancialTransaction.description)
            .order_by(func.sum(FinancialTransaction.amount).desc())
        )
        expense_result = await self.db.execute(expense_group_stmt)
        expense_items = expense_result.all()

        # Format revenue items
        receitas = []
        for item in revenue_items:
            percentual = (
                float(item.total / total_receita * 100) if total_receita > 0 else 0.0
            )
            receitas.append(
                {
                    "categoria": item.description or "Sem descrição",
                    "valor": float(item.total),
                    "percentual": round(percentual, 2),
                }
            )

        # Format expense items
        despesas = []
        for item in expense_items:
            percentual = (
                float(item.total / total_despesa * 100) if total_despesa > 0 else 0.0
            )
            despesas.append(
                {
                    "categoria": item.description or "Sem descrição",
                    "valor": float(item.total),
                    "percentual": round(percentual, 2),
                }
            )

        # Calculate results
        resultado_liquido = total_receita - total_despesa
        margem_lucro = float(resultado_liquido / total_receita * 100) if total_receita > 0 else 0.0

        return {
            "receitas": receitas,
            "despesas": despesas,
            "receita_total": float(total_receita),
            "despesa_total": float(total_despesa),
            "resultado_liquido": float(resultado_liquido),
            "margem_lucro": round(margem_lucro, 2),
        }

    def _get_charts_config(self) -> list[dict]:
        """Get chart configurations for DRE report."""
        return [
            {
                "type": "bar",
                "title": "Receitas vs Despesas",
                "data_key": "valor",
                "x_axis_key": "categoria",
                "y_axis_key": "valor",
                "color_scheme": ["#00bcd4", "#f44336"],
            }
        ]

    def _get_summary(self, filters: dict, data: dict) -> dict:
        """Generate summary for DRE report."""
        return {
            "period_start": filters["period_start"].isoformat(),
            "period_end": filters["period_end"].isoformat(),
            "total_revenue": data["receita_total"],
            "total_expenses": data["despesa_total"],
            "net_result": data["resultado_liquido"],
            "profit_margin": data["margem_lucro"],
        }

    def _count_records(self, data: dict) -> int:
        """Count total records in DRE report."""
        return len(data.get("receitas", [])) + len(data.get("despesas", []))

