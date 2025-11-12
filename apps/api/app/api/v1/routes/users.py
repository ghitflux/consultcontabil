"""
User routes.
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import (
    get_current_active_user,
    get_db,
    require_admin,
    require_admin_or_func,
)
from app.db.models.user import User
from app.db.repositories.user import UserRepository
from app.schemas.base import ResponseSchema
from app.schemas.user import (
    UserCreate,
    UserListItem,
    UserResetPasswordRequest,
    UserResetPasswordResponse,
    UserResponse,
    UserUpdate,
    UserUpdatePassword,
)
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserResponse:
    """
    Get current user information.

    Args:
        current_user: Current authenticated user

    Returns:
        UserResponse: Current user data
    """
    return UserResponse.model_validate(current_user)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: User = Depends(require_admin()),
) -> UserResponse:
    """
    Create a new user (admin only).

    Args:
        user_data: User creation data
        db: Database session
        _: Current user (must be admin)

    Returns:
        UserResponse: Created user data

    Raises:
        HTTPException: 409 if email already exists
    """
    user_repo = UserRepository(db)

    # Check if email already exists
    if await user_repo.email_exists(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new user
    user = User(
        name=user_data.name,
        email=user_data.email,
        role=user_data.role,
        is_active=True,
        is_verified=False,
    )
    user.set_password(user_data.password)

    user = await user_repo.create(user)
    await db.commit()
    await db.refresh(user)

    return UserResponse.model_validate(user)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(require_admin_or_func()),
) -> UserResponse:
    """
    Get user by ID (admin or func only).

    Args:
        user_id: User UUID
        db: Database session
        current_user: Current authenticated user

    Returns:
        UserResponse: User data

    Raises:
        HTTPException: 404 if user not found
    """
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_active_user),
) -> UserResponse:
    """
    Update user (admin or self only).

    Args:
        user_id: User UUID
        user_data: User update data
        db: Database session
        current_user: Current authenticated user

    Returns:
        UserResponse: Updated user data

    Raises:
        HTTPException: 403 if not authorized, 404 if user not found
    """
    user_repo = UserRepository(db)

    # Get user to update
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check authorization (admin or self)
    from app.db.models.user import UserRole
    is_admin = current_user.role == UserRole.ADMIN
    is_self = current_user.id == user_id

    if not (is_admin or is_self):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )

    # If not admin, can only update own name and email
    if not is_admin:
        if user_data.role is not None or user_data.is_active is not None or user_data.is_verified is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admin can update role, active status, or verified status"
            )

    # Update fields
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.email is not None:
        # Check if new email already exists
        if user_data.email != user.email and await user_repo.email_exists(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        user.email = user_data.email
    if user_data.role is not None and is_admin:
        user.role = user_data.role
    if user_data.is_active is not None and is_admin:
        user.is_active = user_data.is_active
    if user_data.is_verified is not None and is_admin:
        user.is_verified = user_data.is_verified

    user = await user_repo.update(user)
    await db.commit()
    await db.refresh(user)

    return UserResponse.model_validate(user)


@router.put("/me/password", response_model=ResponseSchema, status_code=status.HTTP_200_OK)
async def update_own_password(
    password_data: UserUpdatePassword,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_active_user),
) -> ResponseSchema:
    """
    Update own password.

    Args:
        password_data: Password update data
        db: Database session
        current_user: Current authenticated user

    Returns:
        ResponseSchema: Success message

    Raises:
        HTTPException: 401 if current password is incorrect
    """
    # Verify current password
    if not current_user.verify_password(password_data.current_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )

    # Set new password
    current_user.set_password(password_data.new_password)

    user_repo = UserRepository(db)
    await user_repo.update(current_user)
    await db.commit()

    return ResponseSchema(
        success=True,
        message="Password updated successfully"
    )


@router.delete("/{user_id}", response_model=ResponseSchema, status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: User = Depends(require_admin()),
) -> ResponseSchema:
    """
    Delete user (admin only).

    Note: This is a hard delete. Consider implementing soft delete in production.

    Args:
        user_id: User UUID
        db: Database session
        _: Current user (must be admin)

    Returns:
        ResponseSchema: Success message

    Raises:
        HTTPException: 404 if user not found
    """
    user_repo = UserRepository(db)

    deleted = await user_repo.delete(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await db.commit()

    return ResponseSchema(
        success=True,
        message="User deleted successfully"
    )


@router.get("", response_model=dict, status_code=status.HTTP_200_OK)
async def list_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    _: User = Depends(require_admin()),
    query: str | None = None,
    role: str | None = None,
    is_active: bool | None = None,
    page: int = 1,
    size: int = 10,
) -> dict:
    """
    List all users with filters and pagination (admin only).

    Args:
        db: Database session
        _: Current user (must be admin)
        query: Optional search term (name or email)
        role: Optional role filter
        is_active: Optional active status filter
        page: Page number (1-indexed)
        size: Page size

    Returns:
        Paginated list of users
    """
    service = UserService(db)
    return await service.list_users(
        query=query,
        role=role,
        is_active=is_active,
        page=page,
        size=size,
    )


@router.patch("/{user_id}/activate", response_model=ResponseSchema, status_code=status.HTTP_200_OK)
async def activate_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: User = Depends(require_admin()),
) -> ResponseSchema:
    """
    Activate user (admin only).

    Args:
        user_id: User UUID
        db: Database session
        _: Current user (must be admin)

    Returns:
        Success message

    Raises:
        HTTPException: 404 if user not found
    """
    service = UserService(db)
    await service.activate_user(user_id)

    return ResponseSchema(
        success=True,
        message="User activated successfully"
    )


@router.patch("/{user_id}/deactivate", response_model=ResponseSchema, status_code=status.HTTP_200_OK)
async def deactivate_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: User = Depends(require_admin()),
) -> ResponseSchema:
    """
    Deactivate user (admin only).

    Args:
        user_id: User UUID
        db: Database session
        _: Current user (must be admin)

    Returns:
        Success message

    Raises:
        HTTPException: 404 if user not found
    """
    service = UserService(db)
    await service.deactivate_user(user_id)

    return ResponseSchema(
        success=True,
        message="User deactivated successfully"
    )


@router.post("/{user_id}/reset-password", response_model=UserResetPasswordResponse, status_code=status.HTTP_200_OK)
async def reset_user_password(
    user_id: UUID,
    reset_data: UserResetPasswordRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: User = Depends(require_admin()),
) -> UserResetPasswordResponse:
    """
    Reset user password (admin only).

    Generates a temporary password or sets a new password.

    Args:
        user_id: User UUID
        reset_data: Reset password data
        db: Database session
        _: Current user (must be admin)

    Returns:
        Reset password response with temporary password if generated

    Raises:
        HTTPException: 404 if user not found, 400 if invalid data
    """
    service = UserService(db)
    return await service.reset_password(user_id, reset_data)
