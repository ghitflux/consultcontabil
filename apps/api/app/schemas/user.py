"""
User schemas for authentication and user management.
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import EmailStr, Field, field_validator

from .base import BaseSchema, TimestampSchema


class UserRole(str, Enum):
    """User role enumeration."""

    ADMIN = "admin"
    FUNC = "func"
    CLIENTE = "cliente"


class UserBase(BaseSchema):
    """Base user schema with common fields."""

    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(..., min_length=8, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in v):
            raise ValueError("Password must contain at least one letter")
        return v


class UserUpdate(BaseSchema):
    """Schema for updating a user."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserUpdatePassword(BaseSchema):
    """Schema for updating user password."""

    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in v):
            raise ValueError("Password must contain at least one letter")
        return v


class UserResponse(UserBase, TimestampSchema):
    """Schema for user response."""

    id: UUID
    is_active: bool
    is_verified: bool
    last_login_at: Optional[datetime] = None


class UserInDB(UserResponse):
    """Schema for user in database (includes sensitive data)."""

    password_hash: str


class UserListItem(TimestampSchema):
    """Schema for user list item (simplified)."""

    id: UUID
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    is_verified: bool
    last_login_at: Optional[datetime] = None


class UserResetPasswordRequest(BaseSchema):
    """Schema for admin reset password request."""

    generate_temporary: bool = Field(
        default=True,
        description="If true, generates a temporary password. If false, you must provide new_password."
    )
    new_password: Optional[str] = Field(None, min_length=8, max_length=100)

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        """Validate password strength if provided."""
        if v is not None:
            if not any(char.isdigit() for char in v):
                raise ValueError("Password must contain at least one digit")
            if not any(char.isalpha() for char in v):
                raise ValueError("Password must contain at least one letter")
        return v


class UserResetPasswordResponse(BaseSchema):
    """Schema for reset password response."""

    success: bool
    temporary_password: Optional[str] = None
    message: str
