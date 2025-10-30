"""
Authentication schemas.
"""
from typing import Optional

from pydantic import EmailStr, Field

from .base import BaseSchema
from .user import UserResponse


class LoginRequest(BaseSchema):
    """Schema for login request."""

    email: EmailStr
    password: str = Field(..., min_length=1)


class TokenData(BaseSchema):
    """Schema for token payload data."""

    sub: str  # User ID
    role: str
    exp: Optional[int] = None


class TokenResponse(BaseSchema):
    """Schema for token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: UserResponse


class RefreshRequest(BaseSchema):
    """Schema for refresh token request."""

    refresh_token: str


class RefreshResponse(BaseSchema):
    """Schema for refresh token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class LogoutRequest(BaseSchema):
    """Schema for logout request (optional)."""

    refresh_token: Optional[str] = None


class PasswordResetRequest(BaseSchema):
    """Schema for password reset request."""

    email: EmailStr


class PasswordResetConfirm(BaseSchema):
    """Schema for password reset confirmation."""

    token: str
    new_password: str = Field(..., min_length=8, max_length=100)
