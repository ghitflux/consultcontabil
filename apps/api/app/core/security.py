"""
Security utilities for password hashing, JWT tokens, and field encryption.
"""

import base64
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from jose import JWTError, jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def create_access_token(data: dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Data to encode in the token (should include 'sub' for user ID)
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT refresh token.

    Args:
        data: Data to encode in the token (should include 'sub' for user ID)
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc), "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token to decode

    Returns:
        Decoded token payload

    Raises:
        JWTError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise JWTError(f"Invalid token: {str(e)}") from e


def create_tokens(user_id: str, role: str) -> dict[str, Any]:
    """
    Create both access and refresh tokens for a user.

    Args:
        user_id: User ID to encode in tokens
        role: User role to encode in tokens

    Returns:
        Dictionary with access_token, refresh_token, and expires_in
    """
    token_data = {"sub": user_id, "role": role}

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # seconds
    }


# ========== Field Encryption for Sensitive Data ==========

def _get_fernet_key() -> bytes:
    """
    Derive a Fernet encryption key from the SECRET_KEY.
    Uses PBKDF2 with a fixed salt for deterministic key derivation.

    Returns:
        32-byte Fernet-compatible encryption key
    """
    # Use a fixed salt derived from the secret key itself for deterministic encryption
    salt = settings.SECRET_KEY[:16].encode('utf-8').ljust(16, b'0')

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(settings.SECRET_KEY.encode('utf-8')))
    return key


def encrypt_field(value: str | None) -> str | None:
    """
    Encrypt a sensitive field value (e.g., passwords for external systems).

    Args:
        value: Plain text value to encrypt

    Returns:
        Encrypted value as base64 string, or None if input is None
    """
    if value is None or value == "":
        return None

    fernet = Fernet(_get_fernet_key())
    encrypted = fernet.encrypt(value.encode('utf-8'))
    return encrypted.decode('utf-8')


def decrypt_field(encrypted_value: str | None) -> str | None:
    """
    Decrypt a sensitive field value.

    Args:
        encrypted_value: Encrypted value as base64 string

    Returns:
        Decrypted plain text value, or None if input is None

    Raises:
        cryptography.fernet.InvalidToken: If decryption fails (corrupted data or wrong key)
    """
    if encrypted_value is None or encrypted_value == "":
        return None

    fernet = Fernet(_get_fernet_key())
    decrypted = fernet.decrypt(encrypted_value.encode('utf-8'))
    return decrypted.decode('utf-8')
