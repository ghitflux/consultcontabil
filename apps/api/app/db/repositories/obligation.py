"""Obligation Repository - Data access layer for obligations."""

from datetime import datetime
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.obligation import Obligation, ObligationStatus
from app.db.models.obligation_event import ObligationEvent
from app.db.repositories.base import BaseRepository


class ObligationRepository(BaseRepository[Obligation]):
    """Repository for Obligation operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(Obligation, db)

    async def get_by_id_with_relations(self, obligation_id: UUID) -> Optional[Obligation]:
        """Get obligation with all relationships loaded."""
        stmt = (
            select(Obligation)
            .where(Obligation.id == obligation_id)
            .options(
                selectinload(Obligation.obligation_type),
                selectinload(Obligation.client),
                selectinload(Obligation.events),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_client(
        self,
        client_id: UUID,
        status: Optional[ObligationStatus] = None,
        year: Optional[int] = None,
        month: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[Obligation], int]:
        """List obligations for a specific client with filters."""
        conditions = [Obligation.client_id == client_id]

        if status:
            conditions.append(Obligation.status == status)

        if year:
            conditions.append(func.extract("year", Obligation.due_date) == year)

        if month:
            conditions.append(func.extract("month", Obligation.due_date) == month)

        stmt = select(Obligation).where(and_(*conditions)).options(selectinload(Obligation.obligation_type))

        # Count total
        count_stmt = select(func.count()).select_from(Obligation).where(and_(*conditions))
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar_one()

        # Get paginated results
        stmt = stmt.offset(skip).limit(limit).order_by(Obligation.due_date.asc())
        result = await self.db.execute(stmt)
        items = result.scalars().all()

        return items, total

    async def list_pending_by_due_date(self, until_date: datetime) -> Sequence[Obligation]:
        """List all pending obligations with due date until specified date."""
        stmt = (
            select(Obligation)
            .where(
                and_(
                    Obligation.status == ObligationStatus.PENDING,
                    Obligation.due_date <= until_date,
                )
            )
            .options(
                selectinload(Obligation.obligation_type),
                selectinload(Obligation.client),
            )
            .order_by(Obligation.due_date.asc())
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def list_overdue(self, reference_date: Optional[datetime] = None) -> Sequence[Obligation]:
        """List all overdue obligations."""
        if reference_date is None:
            reference_date = datetime.utcnow()

        stmt = (
            select(Obligation)
            .where(
                and_(
                    Obligation.status == ObligationStatus.PENDING,
                    Obligation.due_date < reference_date,
                )
            )
            .options(
                selectinload(Obligation.obligation_type),
                selectinload(Obligation.client),
            )
            .order_by(Obligation.due_date.asc())
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_client_and_type_and_period(
        self,
        client_id: UUID,
        obligation_type_id: UUID,
        year: int,
        month: int,
    ) -> Optional[Obligation]:
        """Get obligation by client, type and period (year/month)."""
        stmt = select(Obligation).where(
            and_(
                Obligation.client_id == client_id,
                Obligation.obligation_type_id == obligation_type_id,
                func.extract("year", Obligation.due_date) == year,
                func.extract("month", Obligation.due_date) == month,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_status(
        self,
        obligation_id: UUID,
        status: ObligationStatus,
        completed_at: Optional[datetime] = None,
        receipt_url: Optional[str] = None,
        processed_by_id: Optional[UUID] = None,
    ) -> Optional[Obligation]:
        """Update obligation status and related fields."""
        obligation = await self.get(obligation_id)
        if not obligation:
            return None

        obligation.status = status

        if completed_at:
            obligation.completed_at = completed_at

        if receipt_url:
            obligation.receipt_url = receipt_url

        if processed_by_id:
            obligation.processed_by_id = processed_by_id

        await self.db.flush()
        await self.db.refresh(obligation)

        return obligation

    async def bulk_create(self, obligations: list[Obligation]) -> list[Obligation]:
        """Create multiple obligations at once."""
        self.db.add_all(obligations)
        await self.db.flush()

        # Refresh all to get IDs
        for obligation in obligations:
            await self.db.refresh(obligation)

        return obligations
