"""
Client service with business logic.
"""

import secrets
import string
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client import Client
from app.db.models.client_user import ClientUser, ClientAccessLevel
from app.db.models.user import User, UserRole
from app.db.repositories.client import ClientRepository
from app.schemas.client import ClientCreate, ClientCreateResponse, ClientDraftCreate, ClientListItem, ClientResponse, ClientUpdate


class ClientService:
    """Service for client operations."""

    def __init__(self, session: AsyncSession):
        """
        Initialize client service.

        Args:
            session: Database session
        """
        self.session = session
        self.repo = ClientRepository(session)

    def _generate_temporary_password(self, length: int = 12) -> str:
        """
        Generate a secure temporary password.

        Args:
            length: Password length

        Returns:
            Temporary password
        """
        alphabet = string.ascii_letters + string.digits + "!@#$%&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password

    async def create_client(self, client_data: ClientCreate) -> ClientCreateResponse:
        """
        Create a new client with optional user creation.

        Args:
            client_data: Client creation data

        Returns:
            Created client with user info if created

        Raises:
            HTTPException: If CNPJ already exists or user email already exists
        """
        # Check if CNPJ already exists
        if await self.repo.cnpj_exists(client_data.cnpj):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="CNPJ already registered"
            )

        # Extract user creation fields before creating client
        create_user = client_data.create_user
        user_email = client_data.user_email
        user_name = client_data.user_name

        # Create client (exclude user creation fields)
        client_dict = client_data.model_dump(exclude={"create_user", "user_email", "user_name"})
        client = Client(**client_dict)
        client = await self.repo.create(client)
        await self.session.flush()  # Flush to get client.id

        # Create user if requested
        user_created = False
        temporary_password = None
        final_user_email = None

        if create_user:
            # Determine user email
            final_user_email = user_email or client_data.responsavel_email or client_data.email

            if not final_user_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email do usuário é obrigatório quando create_user=True"
                )

            # Check if user email already exists
            from sqlalchemy import select
            existing_user = await self.session.execute(
                select(User).where(User.email == final_user_email)
            )
            if existing_user.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Email {final_user_email} já está em uso"
                )

            # Determine user name
            final_user_name = user_name or client_data.responsavel_nome or client_data.razao_social

            # Generate temporary password
            temporary_password = self._generate_temporary_password()

            # Create user
            new_user = User(
                name=final_user_name,
                email=final_user_email,
                role=UserRole.CLIENTE,
                is_active=True,
                is_verified=False,
                primary_client_id=client.id
            )
            new_user.set_password(temporary_password)
            self.session.add(new_user)
            await self.session.flush()

            # Create client-user relationship
            client_user = ClientUser(
                client_id=client.id,
                user_id=new_user.id,
                access_level=ClientAccessLevel.OWNER
            )
            self.session.add(client_user)

            user_created = True

        await self.session.commit()
        await self.session.refresh(client)

        return ClientCreateResponse(
            client=ClientResponse.model_validate(client),
            user_created=user_created,
            user_email=final_user_email if user_created else None,
            temporary_password=temporary_password if user_created else None
        )

    async def get_client(self, client_id: UUID) -> ClientResponse:
        """
        Get client by ID.

        Args:
            client_id: Client UUID

        Returns:
            Client data

        Raises:
            HTTPException: If client not found
        """
        client = await self.repo.get_by_id(client_id)

        if not client or client.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )

        return ClientResponse.model_validate(client)

    async def get_client_by_cnpj(self, cnpj: str) -> ClientResponse:
        """
        Get client by CNPJ.

        Args:
            cnpj: Client CNPJ

        Returns:
            Client data

        Raises:
            HTTPException: If client not found
        """
        client = await self.repo.get_by_cnpj(cnpj)

        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )

        return ClientResponse.model_validate(client)

    async def update_client(
        self,
        client_id: UUID,
        client_data: ClientUpdate,
    ) -> ClientResponse:
        """
        Update client.

        Args:
            client_id: Client UUID
            client_data: Client update data

        Returns:
            Updated client

        Raises:
            HTTPException: If client not found or CNPJ already exists
        """
        # Get client
        client = await self.repo.get_by_id(client_id)

        if not client or client.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )

        # Check if CNPJ is being changed and already exists
        if client_data.cnpj and client_data.cnpj != client.cnpj:
            if await self.repo.cnpj_exists(client_data.cnpj, exclude_id=client_id):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="CNPJ already registered"
                )

        # Update fields
        update_data = client_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(client, field, value)

        client = await self.repo.update(client)
        await self.session.commit()
        await self.session.refresh(client)

        return ClientResponse.model_validate(client)

    async def delete_client(self, client_id: UUID) -> None:
        """
        Delete client (soft delete).

        Args:
            client_id: Client UUID

        Raises:
            HTTPException: If client not found
        """
        client = await self.repo.get_by_id(client_id)

        if not client or client.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )

        client.soft_delete()
        await self.session.commit()

    async def list_clients(
        self,
        query: Optional[str] = None,
        status: Optional[str] = None,
        starts_with: Optional[str] = None,
        page: int = 1,
        size: int = 10,
    ) -> dict:
        """
        List clients with filters and pagination.

        Args:
            query: Search term
            status: Filter by status
            starts_with: Filter by first letter
            page: Page number (1-indexed)
            size: Page size

        Returns:
            Paginated client list
        """
        skip = (page - 1) * size

        # Convert status string to enum
        status_enum = None
        if status:
            from app.db.models.client import ClientStatus
            try:
                status_enum = ClientStatus(status)
            except ValueError:
                pass

        clients, total = await self.repo.list_with_filters(
            query=query,
            status=status_enum,
            starts_with=starts_with,
            skip=skip,
            limit=size,
        )

        # Convert to list items
        items = [ClientListItem.model_validate(c) for c in clients]

        # Calculate pages
        pages = (total + size - 1) // size if size > 0 else 0

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages,
        }

    async def search_clients(self, query: str, limit: int = 10) -> list[dict]:
        """
        Quick search for autocomplete.

        Args:
            query: Search term
            limit: Maximum results

        Returns:
            List of clients (simplified)
        """
        clients = await self.repo.search(query, limit)

        return [
            {
                "id": str(c.id),
                "razao_social": c.razao_social,
                "cnpj": c.cnpj,
            }
            for c in clients
        ]

    async def get_stats(self) -> dict:
        """
        Get client statistics.

        Returns:
            Dictionary with client statistics including:
            - total: Total number of clients
            - by_status: Breakdown by status
            - by_regime: Breakdown by tax regime
            - total_revenue: Total monthly revenue
        """
        from sqlalchemy import func, select
        from app.db.models.client import Client, ClientStatus

        # Total clients
        total_query = select(func.count(Client.id)).where(Client.is_deleted == False)
        total_result = await self.session.execute(total_query)
        total = total_result.scalar() or 0

        # By status
        status_query = (
            select(Client.status, func.count(Client.id))
            .where(Client.is_deleted == False)
            .group_by(Client.status)
        )
        status_result = await self.session.execute(status_query)
        by_status = {status: count for status, count in status_result.all()}

        # By regime
        regime_query = (
            select(Client.regime_tributario, func.count(Client.id))
            .where(Client.is_deleted == False)
            .group_by(Client.regime_tributario)
        )
        regime_result = await self.session.execute(regime_query)
        by_regime = {regime: count for regime, count in regime_result.all()}

        # Total revenue
        revenue_query = select(func.sum(Client.honorarios_mensais)).where(
            Client.is_deleted == False,
            Client.status == ClientStatus.ATIVO
        )
        revenue_result = await self.session.execute(revenue_query)
        total_revenue = revenue_result.scalar() or 0.0

        return {
            "total": total,
            "by_status": by_status,
            "by_regime": by_regime,
            "total_revenue": float(total_revenue),
        }

    async def save_draft(self, draft_data: ClientDraftCreate, user_id: UUID) -> UUID:
        """
        Save client form draft.

        Args:
            draft_data: Draft data
            user_id: User ID who created the draft

        Returns:
            Draft ID
        """
        from app.db.models.client_draft import ClientDraft
        import json

        # Convert draft data to JSON
        draft_json = draft_data.model_dump(exclude={"draft_name"})

        # Create draft
        draft = ClientDraft(
            name=draft_data.draft_name,
            data=draft_json,
            user_id=user_id
        )

        self.session.add(draft)
        await self.session.commit()
        await self.session.refresh(draft)

        return draft.id
