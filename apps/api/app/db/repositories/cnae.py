"""
CNAE repository for database operations.
"""

from typing import Optional
from uuid import UUID
import re

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.cnae import Cnae
from app.db.repositories.base import BaseRepository
from app.schemas.cnae import CnaeType


class CnaeRepository(BaseRepository[Cnae]):
    """Repository for CNAE model operations."""

    def __init__(self, session: AsyncSession):
        """
        Initialize CNAE repository.

        Args:
            session: Database session
        """
        super().__init__(Cnae, session)

    async def get_by_client(self, client_id: UUID, active_only: bool = False) -> list[Cnae]:
        """
        Get all CNAEs for a client.

        Args:
            client_id: Client ID
            active_only: If True, return only active CNAEs

        Returns:
            List of CNAEs
        """
        filters = [Cnae.client_id == client_id]
        if active_only:
            filters.append(Cnae.is_active == True)

        result = await self.session.execute(
            select(Cnae)
            .where(and_(*filters))
            .order_by(
                Cnae.cnae_type.desc(),  # Primary first
                Cnae.created_at.asc()
            )
        )
        return list(result.scalars().all())

    async def get_primary(self, client_id: UUID) -> Optional[Cnae]:
        """
        Get the primary CNAE for a client.

        Args:
            client_id: Client ID

        Returns:
            Primary CNAE or None if not found
        """
        result = await self.session.execute(
            select(Cnae)
            .where(
                and_(
                    Cnae.client_id == client_id,
                    Cnae.cnae_type == CnaeType.PRINCIPAL,
                    Cnae.is_active == True,
                )
            )
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def set_as_primary(self, cnae_id: UUID, client_id: UUID) -> Cnae:
        """
        Set a CNAE as primary for a client.
        This will unset any existing primary CNAE for the client.

        Args:
            cnae_id: CNAE ID to set as primary
            client_id: Client ID (for validation)

        Returns:
            Updated CNAE

        Raises:
            ValueError: If CNAE not found or doesn't belong to client
        """
        # Get the CNAE to set as primary
        cnae = await self.get_by_id(cnae_id)
        if not cnae:
            raise ValueError(f"CNAE {cnae_id} not found")
        if cnae.client_id != client_id:
            raise ValueError(f"CNAE {cnae_id} does not belong to client {client_id}")

        # Unset all other primary CNAEs for this client
        result = await self.session.execute(
            select(Cnae)
            .where(
                and_(
                    Cnae.client_id == client_id,
                    Cnae.cnae_type == CnaeType.PRINCIPAL,
                    Cnae.id != cnae_id,
                )
            )
        )
        other_primaries = list(result.scalars().all())
        for other in other_primaries:
            other.cnae_type = CnaeType.SECUNDARIO

        # Set this CNAE as primary
        cnae.cnae_type = CnaeType.PRINCIPAL
        await self.session.flush()
        await self.session.refresh(cnae)

        return cnae

    def validate_cnae_format(self, cnae_code: str) -> bool:
        """
        Validate CNAE code format (0000-0/00).

        Args:
            cnae_code: CNAE code to validate

        Returns:
            True if format is valid, False otherwise
        """
        # Remove any whitespace
        cnae_code = cnae_code.strip()

        # Check format with regex
        pattern = r'^\d{4}-\d{1}/\d{2}$'
        return bool(re.match(pattern, cnae_code))

    async def cnae_exists_for_client(self, client_id: UUID, cnae_code: str, exclude_id: Optional[UUID] = None) -> bool:
        """
        Check if a CNAE code already exists for a client.

        Args:
            client_id: Client ID
            cnae_code: CNAE code to check
            exclude_id: Optional CNAE ID to exclude (for updates)

        Returns:
            True if CNAE exists, False otherwise
        """
        filters = [
            Cnae.client_id == client_id,
            Cnae.cnae_code == cnae_code,
        ]
        if exclude_id:
            filters.append(Cnae.id != exclude_id)

        result = await self.session.execute(
            select(Cnae).where(and_(*filters))
        )
        return result.scalar_one_or_none() is not None

    async def get_by_code(self, client_id: UUID, cnae_code: str) -> Optional[Cnae]:
        """
        Get a CNAE by code for a specific client.

        Args:
            client_id: Client ID
            cnae_code: CNAE code

        Returns:
            CNAE or None if not found
        """
        result = await self.session.execute(
            select(Cnae)
            .where(
                and_(
                    Cnae.client_id == client_id,
                    Cnae.cnae_code == cnae_code,
                )
            )
            .limit(1)
        )
        return result.scalar_one_or_none()

