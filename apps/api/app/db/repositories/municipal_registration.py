"""
Municipal Registration repository for database operations.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.municipal_registration import MunicipalRegistration
from app.db.repositories.base import BaseRepository
from app.schemas.municipal_registration import MunicipalRegistrationStatus, StateCode


class MunicipalRegistrationRepository(BaseRepository[MunicipalRegistration]):
    """Repository for MunicipalRegistration model operations."""

    def __init__(self, session: AsyncSession):
        """
        Initialize municipal registration repository.

        Args:
            session: Database session
        """
        super().__init__(MunicipalRegistration, session)

    async def get_by_client(self, client_id: UUID, active_only: bool = False) -> list[MunicipalRegistration]:
        """
        Get all municipal registrations for a client.

        Args:
            client_id: Client ID
            active_only: If True, return only active registrations

        Returns:
            List of municipal registrations
        """
        filters = [MunicipalRegistration.client_id == client_id]
        if active_only:
            filters.append(MunicipalRegistration.status == MunicipalRegistrationStatus.ATIVA)

        result = await self.session.execute(
            select(MunicipalRegistration)
            .where(and_(*filters))
            .order_by(
                MunicipalRegistration.state,
                MunicipalRegistration.city,
                MunicipalRegistration.created_at.desc()
            )
        )
        return list(result.scalars().all())

    async def get_by_city_state(
        self,
        city: str,
        state: StateCode,
        registration_number: Optional[str] = None,
    ) -> list[MunicipalRegistration]:
        """
        Get municipal registrations by city and state.

        Args:
            city: City name
            state: State code (UF)
            registration_number: Optional registration number to filter

        Returns:
            List of municipal registrations
        """
        filters = [
            MunicipalRegistration.city.ilike(f"%{city}%"),
            MunicipalRegistration.state == state,
        ]

        if registration_number:
            filters.append(MunicipalRegistration.registration_number == registration_number)

        result = await self.session.execute(
            select(MunicipalRegistration)
            .where(and_(*filters))
            .order_by(MunicipalRegistration.city, MunicipalRegistration.created_at.desc())
        )
        return list(result.scalars().all())

    async def registration_exists(
        self,
        city: str,
        state: StateCode,
        registration_number: str,
        exclude_id: Optional[UUID] = None,
    ) -> bool:
        """
        Check if a municipal registration already exists.

        Args:
            city: City name
            state: State code (UF)
            registration_number: Registration number
            exclude_id: Optional registration ID to exclude (for updates)

        Returns:
            True if registration exists, False otherwise
        """
        filters = [
            MunicipalRegistration.city == city,
            MunicipalRegistration.state == state,
            MunicipalRegistration.registration_number == registration_number,
        ]

        if exclude_id:
            filters.append(MunicipalRegistration.id != exclude_id)

        result = await self.session.execute(
            select(MunicipalRegistration).where(and_(*filters))
        )
        return result.scalar_one_or_none() is not None

    async def list_with_filters(
        self,
        client_id: Optional[UUID] = None,
        state: Optional[StateCode] = None,
        status: Optional[MunicipalRegistrationStatus] = None,
        city: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> tuple[list[MunicipalRegistration], int]:
        """
        List municipal registrations with filters and pagination.

        Args:
            client_id: Filter by client ID
            state: Filter by state (UF)
            status: Filter by status
            city: Filter by city name (ILIKE search)
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (registrations list, total count)
        """
        filters = []

        # Apply filters
        if client_id:
            filters.append(MunicipalRegistration.client_id == client_id)

        if state:
            filters.append(MunicipalRegistration.state == state)

        if status:
            filters.append(MunicipalRegistration.status == status)

        if city:
            filters.append(MunicipalRegistration.city.ilike(f"%{city}%"))

        # Count query
        count_query = select(func.count()).select_from(MunicipalRegistration)
        if filters:
            count_query = count_query.where(and_(*filters))
        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        # Data query with pagination
        data_query = select(MunicipalRegistration)
        if filters:
            data_query = data_query.where(and_(*filters))
        data_query = (
            data_query
            .order_by(
                MunicipalRegistration.state,
                MunicipalRegistration.city,
                MunicipalRegistration.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(data_query)
        registrations = list(result.scalars().all())

        return registrations, total

