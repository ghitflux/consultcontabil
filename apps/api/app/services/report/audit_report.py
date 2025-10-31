"""Audit Report Service."""

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.audit import AuditLog
from app.services.report.base import BaseReportService


class AuditReportService(BaseReportService):
    """Service for generating Audit reports."""

    async def generate_data(self, filters: dict) -> dict:
        """
        Generate Audit report data.

        Filters:
            period_start: Start date
            period_end: End date
            client_ids: Optional list of client IDs to filter (ignored for audit)

        Returns:
            Dictionary with audit statistics
        """
        # Build conditions for date range
        conditions = []

        # Get all actions in period
        total_stmt = select(func.count()).where(and_(*conditions))

        # Group by user
        user_stmt = (
            select(AuditLog.user_id, func.count().label("count"))
            .where(and_(*conditions))
            .group_by(AuditLog.user_id)
        )

        # Group by module/entity
        module_stmt = (
            select(AuditLog.entity, func.count().label("count"))
            .where(and_(*conditions))
            .group_by(AuditLog.entity)
        )

        # Group by action type
        action_stmt = (
            select(AuditLog.action, func.count().label("count"))
            .where(and_(*conditions))
            .group_by(AuditLog.action)
        )

        total = await self.db.scalar(total_stmt) or 0
        user_result = await self.db.execute(user_stmt)
        module_result = await self.db.execute(module_stmt)
        action_result = await self.db.execute(action_stmt)

        # Format results
        actions_by_user = {
            str(row.user_id): row.count for row in user_result.all()
        }
        actions_by_module = {row.entity: row.count for row in module_result.all()}
        actions_by_type = {row.action: row.count for row in action_result.all()}

        return {
            "total_actions": total,
            "actions_by_user": actions_by_user,
            "actions_by_module": actions_by_module,
            "actions_by_type": actions_by_type,
        }

    def _get_charts_config(self) -> list[dict]:
        """Get chart configurations for Audit report."""
        return [
            {
                "type": "bar",
                "title": "Atividades por Usuário",
                "data_key": "actions_by_user",
            },
            {
                "type": "bar",
                "title": "Atividades por Módulo",
                "data_key": "actions_by_module",
            },
        ]

    def _get_summary(self, filters: dict, data: dict) -> dict:
        """Generate summary for Audit report."""
        return {
            "total_actions": data["total_actions"],
            "unique_users": len(data["actions_by_user"]),
            "modules_touched": len(data["actions_by_module"]),
        }

    def _count_records(self, data: dict) -> int:
        """Count total records in Audit report."""
        return data.get("total_actions", 0)

