"""
CNAE validator service.
"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.cnae import CnaeRepository


class CnaeValidator:
    """Service for CNAE validation operations."""

    def __init__(self, session: AsyncSession):
        """
        Initialize CNAE validator.

        Args:
            session: Database session
        """
        self.session = session
        self.repo = CnaeRepository(session)

    def validate_format(self, cnae_code: str) -> tuple[bool, str]:
        """
        Validate CNAE code format (0000-0/00).

        Args:
            cnae_code: CNAE code to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.repo.validate_cnae_format(cnae_code):
            return False, "CNAE deve estar no formato 0000-0/00 (ex: 1234-5/67)"

        return True, ""

    async def validate_primary_constraint(
        self,
        client_id: UUID,
        cnae_id: UUID | None = None,
    ) -> tuple[bool, str]:
        """
        Validate that a client has at most one primary CNAE.

        Args:
            client_id: Client ID
            cnae_id: Optional CNAE ID to exclude (for updates)

        Returns:
            Tuple of (is_valid, error_message)
        """
        primary = await self.repo.get_primary(client_id)

        if primary and (not cnae_id or primary.id != cnae_id):
            return False, "Cliente já possui um CNAE principal. Remova o principal atual antes de definir outro."

        return True, ""

    async def validate_unique_cnae(
        self,
        client_id: UUID,
        cnae_code: str,
        exclude_id: UUID | None = None,
    ) -> tuple[bool, str]:
        """
        Validate that CNAE code is unique for the client.

        Args:
            client_id: Client ID
            cnae_code: CNAE code to check
            exclude_id: Optional CNAE ID to exclude (for updates)

        Returns:
            Tuple of (is_valid, error_message)
        """
        exists = await self.repo.cnae_exists_for_client(client_id, cnae_code, exclude_id)

        if exists:
            return False, f"CNAE {cnae_code} já existe para este cliente"

        return True, ""

