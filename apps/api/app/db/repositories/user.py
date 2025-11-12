"""
User repository for database operations.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User, UserRole
from app.db.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model operations."""

    def __init__(self, session: AsyncSession):
        """
        Initialize user repository.

        Args:
            session: Database session
        """
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> User | None:
        """
        Get user by email.

        Args:
            email: User email

        Returns:
            User or None if not found
        """
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def email_exists(self, email: str, exclude_id: Optional[UUID] = None) -> bool:
        """
        Check if email already exists.

        Args:
            email: Email to check
            exclude_id: Optional user ID to exclude from check

        Returns:
            True if email exists, False otherwise
        """
        query = select(User).where(User.email == email)

        if exclude_id:
            query = query.where(User.id != exclude_id)

        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def get_active_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """
        Get all active users.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active users
        """
        result = await self.session.execute(
            select(User).where(User.is_active == True).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def list_with_filters(
        self,
        query: Optional[str] = None,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> tuple[list[User], int]:
        """
        List users with filters and pagination.

        Args:
            query: Search term (name or email)
            role: Filter by role
            is_active: Filter by active status
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (users list, total count)
        """
        # Build base query
        stmt = select(User)

        # Apply filters
        if query:
            search = f"%{query}%"
            stmt = stmt.where(
                (User.name.ilike(search)) | (User.email.ilike(search))
            )

        if role is not None:
            stmt = stmt.where(User.role == role)

        if is_active is not None:
            stmt = stmt.where(User.is_active == is_active)

        # Get total count
        from sqlalchemy import func
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar() or 0

        # Apply pagination and ordering
        stmt = stmt.order_by(User.created_at.desc()).offset(skip).limit(limit)

        # Execute query
        result = await self.session.execute(stmt)
        users = list(result.scalars().all())

        return users, total

    async def get_users_by_client(self, client_id: UUID) -> list[User]:
        """
        Get all users associated with a client.

        Args:
            client_id: Client UUID

        Returns:
            List of users
        """
        from app.db.models.client_user import ClientUser

        stmt = (
            select(User)
            .join(ClientUser, ClientUser.user_id == User.id)
            .where(ClientUser.client_id == client_id)
            .order_by(User.created_at.desc())
        )

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def deactivate(self, user: User) -> User:
        """
        Deactivate a user.

        Args:
            user: User to deactivate

        Returns:
            Updated user
        """
        user.is_active = False
        await self.session.flush()
        return user

    async def activate(self, user: User) -> User:
        """
        Activate a user.

        Args:
            user: User to activate

        Returns:
            Updated user
        """
        user.is_active = True
        await self.session.flush()
        return user
