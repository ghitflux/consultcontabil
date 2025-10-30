"""
Client routes.
"""

from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_active_user, get_db, require_admin, require_admin_or_func
from app.db.models.user import User
from app.schemas.base import ResponseSchema
from app.schemas.client import ClientCreate, ClientListItem, ClientResponse, ClientUpdate
from app.services.client import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=dict, status_code=status.HTTP_200_OK)
async def list_clients(
    db: Annotated[AsyncSession, Depends(get_db)],
    _: User = Depends(require_admin_or_func()),
    query: Optional[str] = Query(None, description="Search by razao social or CNPJ"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    starts_with: Optional[str] = Query(None, description="Filter by first letter (A-Z)", max_length=1),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
) -> dict:
    """
    List all clients with filters and pagination (admin or func only).

    Args:
        db: Database session
        _: Current user (must be admin or func)
        query: Optional search term
        status_filter: Optional status filter
        starts_with: Optional first letter filter
        page: Page number (1-indexed)
        size: Page size

    Returns:
        Paginated list of clients
    """
    service = ClientService(db)
    return await service.list_clients(
        query=query,
        status=status_filter,
        starts_with=starts_with,
        page=page,
        size=size,
    )


@router.get("/search", response_model=dict, status_code=status.HTTP_200_OK)
async def search_clients(
    db: Annotated[AsyncSession, Depends(get_db)],
    _: User = Depends(require_admin_or_func()),
    q: str = Query(..., min_length=1, description="Search term"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results"),
) -> dict:
    """
    Quick search for autocomplete (admin or func only).

    Args:
        db: Database session
        _: Current user (must be admin or func)
        q: Search term
        limit: Maximum results

    Returns:
        List of matching clients
    """
    service = ClientService(db)
    results = await service.search_clients(q, limit)
    return {"items": results}


@router.get("/{client_id}", response_model=ClientResponse, status_code=status.HTTP_200_OK)
async def get_client(
    client_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_active_user),
) -> ClientResponse:
    """
    Get client by ID.

    Admin and func can see any client.
    Cliente users can only see their own data.

    Args:
        client_id: Client UUID
        db: Database session
        current_user: Current authenticated user

    Returns:
        Client data

    Raises:
        HTTPException: 403 if not authorized, 404 if not found
    """
    from app.db.models.user import UserRole

    service = ClientService(db)
    client = await service.get_client(client_id)

    # Check authorization for cliente users
    if current_user.role == UserRole.CLIENTE:
        # TODO: Add relationship between user and client
        # For now, allow if client email matches user email
        if client.email != current_user.email:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this client"
            )

    return client


@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(
    client_data: ClientCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: User = Depends(require_admin_or_func()),
) -> ClientResponse:
    """
    Create a new client (admin or func only).

    Args:
        client_data: Client creation data
        db: Database session
        _: Current user (must be admin or func)

    Returns:
        Created client

    Raises:
        HTTPException: 409 if CNPJ already exists
    """
    service = ClientService(db)
    return await service.create_client(client_data)


@router.put("/{client_id}", response_model=ClientResponse, status_code=status.HTTP_200_OK)
async def update_client(
    client_id: UUID,
    client_data: ClientUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: User = Depends(require_admin_or_func()),
) -> ClientResponse:
    """
    Update client (admin or func only).

    Args:
        client_id: Client UUID
        client_data: Client update data
        db: Database session
        _: Current user (must be admin or func)

    Returns:
        Updated client

    Raises:
        HTTPException: 404 if not found, 409 if CNPJ conflict
    """
    service = ClientService(db)
    return await service.update_client(client_id, client_data)


@router.delete("/{client_id}", response_model=ResponseSchema, status_code=status.HTTP_200_OK)
async def delete_client(
    client_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: User = Depends(require_admin()),
) -> ResponseSchema:
    """
    Delete client (soft delete, admin only).

    Args:
        client_id: Client UUID
        db: Database session
        _: Current user (must be admin)

    Returns:
        Success message

    Raises:
        HTTPException: 404 if not found
    """
    service = ClientService(db)
    await service.delete_client(client_id)

    return ResponseSchema(
        success=True,
        message="Client deleted successfully"
    )
