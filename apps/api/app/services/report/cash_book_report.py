"""Cash Book Report Service - Livro Caixa."""

from decimal import Decimal

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.finance import FinancialTransaction, PaymentStatus, TransactionType
from app.services.report.base import BaseReportService


class CashBookReportService(BaseReportService):
    """Service for generating Cash Book reports."""

    async def generate_data(self, filters: dict) -> dict:
        """
        Generate Cash Book report data with chronological entries.

        Filters:
            period_start: Start date
            period_end: End date
            client_ids: Optional list of client IDs to filter

        Returns:
            Dictionary with cash book entries
        """
        period_start = filters["period_start"]
        period_end = filters["period_end"]
        client_ids = filters.get("client_ids")

        # Build conditions
        conditions = [
            FinancialTransaction.deleted_at.is_(None),
            FinancialTransaction.paid_date.isnot(None),  # Only paid transactions
        ]

        if client_ids:
            conditions.append(FinancialTransaction.client_id.in_(client_ids))

        # Get all transactions ordered by paid date
        stmt = (
            select(FinancialTransaction)
            .where(and_(*conditions))
            .filter(
                FinancialTransaction.paid_date >= period_start,
                FinancialTransaction.paid_date <= period_end,
            )
            .order_by(FinancialTransaction.paid_date, FinancialTransaction.created_at)
        )

        result = await self.db.execute(stmt)
        transactions = result.scalars().all()

        # Build entries with accumulated balance
        entries = []
        saldo_acumulado = Decimal("0.00")
        total_entradas = Decimal("0.00")
        total_saidas = Decimal("0.00")

        for transaction in transactions:
            tipo = "entrada" if transaction.transaction_type == TransactionType.RECEITA else "saida"
            valor = transaction.amount

            if tipo == "entrada":
                saldo_acumulado += valor
                total_entradas += valor
            else:
                saldo_acumulado -= valor
                total_saidas += valor

            entries.append({
                "data": transaction.paid_date.date(),
                "tipo": tipo,
                "descricao": transaction.description,
                "valor": float(valor),
                "saldo_acumulado": float(saldo_acumulado),
            })

        return {
            "entries": entries,
            "saldo_inicial": 0.0,  # Could be enhanced to get opening balance
            "saldo_final": float(saldo_acumulado),
            "total_entradas": float(total_entradas),
            "total_saidas": float(total_saidas),
        }

    def _get_charts_config(self) -> list[dict]:
        """Get chart configurations for Cash Book report."""
        return [
            {
                "type": "table",
                "title": "Livro Caixa",
                "columns": ["data", "tipo", "descricao", "valor", "saldo_acumulado"],
            }
        ]

    def _get_summary(self, filters: dict, data: dict) -> dict:
        """Generate summary for Cash Book report."""
        return {
            "period": f"{filters['period_start'].isoformat()} a {filters['period_end'].isoformat()}",
            "initial_balance": data["saldo_inicial"],
            "final_balance": data["saldo_final"],
            "total_entries": len(data["entries"]),
        }

    def _count_records(self, data: dict) -> int:
        """Count total records in Cash Book report."""
        return len(data.get("entries", []))

