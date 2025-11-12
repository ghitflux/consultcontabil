"""
User service with business logic.
"""

import secrets
import string
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client_user import ClientUser, ClientAccessLevel
from app.db.models.user import User, UserRole
from app.db.repositories.user import UserRepository
from app.schemas.user import (
    UserCreate,
    UserListItem,
    UserResetPasswordRequest,
    UserResetPasswordResponse,
    UserResponse,
    UserUpdate,
)


class UserService:
    """Service for user operations."""

    def __init__(self, session: AsyncSession):
        """
        Initialize user service.

        Args:
            session: Database session
        """
        self.session = session
        self.repo = UserRepository(session)

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

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """
        Create a new user.

        Args:
            user_data: User creation data

        Returns:
            Created user

        Raises:
            HTTPException: If email already exists
        """
        # Check if email already exists
        if await self.repo.email_exists(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Create user
        user = User(
            name=user_data.name,
            email=user_data.email,
            role=user_data.role,
            is_active=True,
            is_verified=False
        )
        user.set_password(user_data.password)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return UserResponse.model_validate(user)

    async def get_user(self, user_id: UUID) -> UserResponse:
        """
        Get user by ID.

        Args:
            user_id: User UUID

        Returns:
            User data

        Raises:
            HTTPException: If user not found
        """
        user = await self.repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserResponse.model_validate(user)

    async def update_user(
        self,
        user_id: UUID,
        user_data: UserUpdate,
    ) -> UserResponse:
        """
        Update user.

        Args:
            user_id: User UUID
            user_data: User update data

        Returns:
            Updated user

        Raises:
            HTTPException: If user not found or email already exists
        """
        # Get user
        user = await self.repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if email is being changed and already exists
        if user_data.email and user_data.email != user.email:
            if await self.repo.email_exists(user_data.email, exclude_id=user_id):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered"
                )

        # Update fields
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        await self.session.commit()
        await self.session.refresh(user)

        return UserResponse.model_validate(user)

    async def deactivate_user(self, user_id: UUID) -> None:
        """
        Deactivate user.

        Args:
            user_id: User UUID

        Raises:
            HTTPException: If user not found
        """
        user = await self.repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        await self.repo.deactivate(user)
        await self.session.commit()

    async def activate_user(self, user_id: UUID) -> None:
        """
        Activate user.

        Args:
            user_id: User UUID

        Raises:
            HTTPException: If user not found
        """
        user = await self.repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        await self.repo.activate(user)
        await self.session.commit()

    async def list_users(
        self,
        query: Optional[str] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        page: int = 1,
        size: int = 10,
    ) -> dict:
        """
        List users with filters and pagination.

        Args:
            query: Search term
            role: Filter by role
            is_active: Filter by active status
            page: Page number (1-indexed)
            size: Page size

        Returns:
            Paginated user list
        """
        skip = (page - 1) * size

        # Convert role string to enum
        role_enum = None
        if role:
            try:
                role_enum = UserRole(role)
            except ValueError:
                pass

        users, total = await self.repo.list_with_filters(
            query=query,
            role=role_enum,
            is_active=is_active,
            skip=skip,
            limit=size,
        )

        # Convert to list items
        items = [UserListItem.model_validate(u) for u in users]

        # Calculate pages
        pages = (total + size - 1) // size if size > 0 else 0

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages,
        }

    async def reset_password(
        self,
        user_id: UUID,
        reset_data: UserResetPasswordRequest
    ) -> UserResetPasswordResponse:
        """
        Reset user password (admin only).

        Args:
            user_id: User UUID
            reset_data: Reset password data

        Returns:
            Reset password response with temporary password if generated

        Raises:
            HTTPException: If user not found or invalid data
        """
        user = await self.repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        temporary_password = None

        if reset_data.generate_temporary:
            # Generate temporary password
            temporary_password = self._generate_temporary_password()
            user.set_password(temporary_password)
        elif reset_data.new_password:
            # Use provided password
            user.set_password(reset_data.new_password)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Must either generate_temporary=True or provide new_password"
            )

        await self.session.commit()

        return UserResetPasswordResponse(
            success=True,
            temporary_password=temporary_password,
            message="Password reset successfully"
        )

    async def link_user_to_client(
        self,
        client_id: UUID,
        user_id: UUID,
        access_level: ClientAccessLevel = ClientAccessLevel.VIEWER
    ) -> None:
        """
        Link user to client.

        Args:
            client_id: Client UUID
            user_id: User UUID
            access_level: Access level for the user

        Raises:
            HTTPException: If user not found or link already exists
        """
        user = await self.repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if link already exists
        from sqlalchemy import select
        existing = await self.session.execute(
            select(ClientUser).where(
                ClientUser.client_id == client_id,
                ClientUser.user_id == user_id
            )
        )

        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already linked to this client"
            )

        # Create link
        client_user = ClientUser(
            client_id=client_id,
            user_id=user_id,
            access_level=access_level
        )
        self.session.add(client_user)
        await self.session.commit()
