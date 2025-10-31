"""Obligation Event Repository - Data access layer for obligation events."""

from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.obligation_event import ObligationEvent
from app.db.repositories.base import BaseRepository


class ObligationEventRepository(BaseRepository[ObligationEvent]):
    """Repository for ObligationEvent operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(ObligationEvent, db)

    async def list_by_obligation(
        self,
        obligation_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ObligationEvent]:
        """List all events for a specific obligation."""
        stmt = (
            select(ObligationEvent)
            .where(ObligationEvent.obligation_id == obligation_id)
            .order_by(ObligationEvent.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
