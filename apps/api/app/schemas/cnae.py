"""
CNAE schemas for API requests and responses.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator
import re


class CnaeType(str, Enum):
    """Type of CNAE"""
    PRINCIPAL = "principal"
    SECUNDARIO = "secundario"


# CNAE Schemas
class CnaeBase(BaseModel):
    """Base schema for CNAE"""
    cnae_code: str = Field(..., min_length=9, max_length=10, description="CNAE code in format 0000-0/00")
    description: str = Field(..., min_length=1, max_length=500, description="CNAE description")
    cnae_type: CnaeType = Field(default=CnaeType.SECUNDARIO, description="Primary or secondary CNAE")

    @field_validator("cnae_code")
    @classmethod
    def validate_cnae_format(cls, v: str) -> str:
        """Validate CNAE code format (0000-0/00)"""
        # Remove any whitespace
        v = v.strip()

        # Check format with regex
        pattern = r'^\d{4}-\d{1}/\d{2}$'
        if not re.match(pattern, v):
            raise ValueError(
                "CNAE code must be in format 0000-0/00 (e.g., 6201-5/00)"
            )

        return v


class CnaeCreate(CnaeBase):
    """Schema for creating a new CNAE"""
    client_id: UUID


class CnaeUpdate(BaseModel):
    """Schema for updating a CNAE"""
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    cnae_type: Optional[CnaeType] = None
    is_active: Optional[bool] = None


class CnaeResponse(CnaeBase):
    """Schema for CNAE response"""
    id: UUID
    client_id: UUID
    is_active: bool
    created_at: datetime

    # Related data
    client_name: Optional[str] = None

    class Config:
        from_attributes = True


class CnaeListResponse(BaseModel):
    """Schema for CNAE list response"""
    items: list[CnaeResponse]
    total: int


class CnaeSetPrimary(BaseModel):
    """Schema for setting a CNAE as primary"""
    cnae_id: UUID = Field(..., description="CNAE ID to set as primary")


# CNAE Validation
class CnaeValidation(BaseModel):
    """Schema for CNAE validation response"""
    is_valid: bool
    cnae_code: str
    formatted_code: str
    error: Optional[str] = None
