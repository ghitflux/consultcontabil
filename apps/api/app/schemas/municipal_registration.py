"""
Municipal Registration schemas for API requests and responses.
"""

from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class MunicipalRegistrationStatus(str, Enum):
    """Status of municipal registration"""
    ATIVA = "ativa"
    INATIVA = "inativa"
    SUSPENSA = "suspensa"
    PENDENTE = "pendente"
    CANCELADA = "cancelada"


class StateCode(str, Enum):
    """Brazilian state codes (UF)"""
    AC = "AC"
    AL = "AL"
    AP = "AP"
    AM = "AM"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MT = "MT"
    MS = "MS"
    MG = "MG"
    PA = "PA"
    PB = "PB"
    PR = "PR"
    PE = "PE"
    PI = "PI"
    RJ = "RJ"
    RN = "RN"
    RS = "RS"
    RO = "RO"
    RR = "RR"
    SC = "SC"
    SP = "SP"
    SE = "SE"
    TO = "TO"


# Municipal Registration Schemas
class MunicipalRegistrationBase(BaseModel):
    """Base schema for municipal registration"""
    client_id: UUID
    city: str = Field(..., min_length=1, max_length=100, description="City name")
    state: StateCode = Field(..., description="State code (UF)")
    registration_number: str = Field(..., min_length=1, max_length=50, description="Municipal registration number (CCM/Inscrição Municipal)")
    issue_date: date = Field(..., description="Issue date")
    notes: Optional[str] = Field(None, max_length=1000, description="Additional notes")


class MunicipalRegistrationCreate(MunicipalRegistrationBase):
    """Schema for creating a new municipal registration"""
    pass


class MunicipalRegistrationUpdate(BaseModel):
    """Schema for updating a municipal registration"""
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[StateCode] = None
    registration_number: Optional[str] = Field(None, min_length=1, max_length=50)
    issue_date: Optional[date] = None
    status: Optional[MunicipalRegistrationStatus] = None
    notes: Optional[str] = Field(None, max_length=1000)


class MunicipalRegistrationResponse(MunicipalRegistrationBase):
    """Schema for municipal registration response"""
    id: UUID
    status: MunicipalRegistrationStatus
    created_at: datetime
    updated_at: datetime

    # Related data
    client_name: Optional[str] = None

    class Config:
        from_attributes = True


class MunicipalRegistrationListResponse(BaseModel):
    """Schema for paginated municipal registration list"""
    items: list[MunicipalRegistrationResponse]
    total: int
    page: int
    size: int
    pages: int


# Statistics
class MunicipalRegistrationStatistics(BaseModel):
    """Municipal registration statistics"""
    total_registrations: int = 0
    active_registrations: int = 0
    inactive_registrations: int = 0
    by_state: dict[str, int] = Field(default_factory=dict)
    by_status: dict[str, int] = Field(default_factory=dict)
