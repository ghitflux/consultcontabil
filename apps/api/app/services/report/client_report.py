"""Client Report Service."""

from decimal import Decimal

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client import Client
from app.db.models.finance import FinancialTransaction, PaymentStatus
from app.services.report.base import BaseReportService


class ClientReportService(BaseReportService):
    """Service for generating Client reports."""

    async def generate_data(self, filters: dict) -> dict:
        """
        Generate Client report data.

        Filters:
            period_start: Start date (optional)
            period_end: End date (optional)
            client_ids: Optional list of client IDs to filter

        Returns:
            Dictionary with client data structure
        """
        client_ids = filters.get("client_ids")

        # Build base conditions
        conditions = [Client.deleted_at.is_(None)]

        if client_ids:
            conditions.append(Client.id.in_(client_ids))

        # Get all clients with their financial summary
        stmt = select(Client).where(and_(*conditions)).order_by(Client.razao_social)

        result = await self.db.execute(stmt)
        clients_list = result.scalars().all()

        # For each client, calculate financial summaries
        clients_data = []
        total_honorarios = Decimal("0.00")

        for client in clients_list:
            # Get pending transactions
            pending_stmt = (
                select(func.sum(FinancialTransaction.amount))
                .where(
                    and_(
                        FinancialTransaction.client_id == client.id,
                        FinancialTransaction.payment_status == PaymentStatus.PENDENTE,
                        FinancialTransaction.deleted_at.is_(None),
                    )
                )
            )
            total_pendente = await self.db.scalar(pending_stmt) or Decimal("0.00")

            # Get overdue transactions
            overdue_stmt = (
                select(func.sum(FinancialTransaction.amount))
                .where(
                    and_(
                        FinancialTransaction.client_id == client.id,
                        FinancialTransaction.payment_status == PaymentStatus.ATRASADO,
                        FinancialTransaction.deleted_at.is_(None),
                    )
                )
            )
            total_atrasado = await self.db.scalar(overdue_stmt) or Decimal("0.00")

            clients_data.append({
                "id": str(client.id),
                "razao_social": client.razao_social,
                "cnpj": client.cnpj,
                "email": client.email,
                "status": client.status,
                "honorarios": float(client.honorarios_mensais),
                "total_pendente": float(total_pendente),
                "total_atrasado": float(total_atrasado),
            })

            total_honorarios += Decimal(str(client.honorarios_mensais))

        return {
            "clients": clients_data,
            "total_clientes": len(clients_data),
            "total_honorarios": float(total_honorarios),
        }

    def _get_charts_config(self) -> list[dict]:
        """Get chart configurations for Client report."""
        return [
            {
                "type": "table",
                "title": "Lista de Clientes",
                "columns": ["razao_social", "status", "honorarios", "total_pendente"],
            }
        ]

    def _get_summary(self, filters: dict, data: dict) -> dict:
        """Generate summary for Client report."""
        return {
            "total_clients": data["total_clientes"],
            "total_monthly_fees": data["total_honorarios"],
        }

    def _count_records(self, data: dict) -> int:
        """Count total records in Client report."""
        return len(data.get("clients", []))

