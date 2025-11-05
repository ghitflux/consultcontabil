"""Obligations API routes."""

from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_active_user, get_db
from app.db.models.user import User, UserRole
from app.db.models.obligation import ObligationStatus
from app.db.repositories.obligation import ObligationRepository
from app.db.repositories.obligation_event import ObligationEventRepository
from app.db.repositories.client import ClientRepository
from app.schemas.obligation import (
    ObligationCreate,
    ObligationResponse,
    ObligationListResponse,
    ObligationEventResponse,
    ObligationGenerateRequest,
    ObligationGenerateResponse,
    ObligationReceiptRequest,
    ObligationUpdateDueDateRequest,
    ObligationCancelRequest,
)
from app.services.obligation.processor import ObligationProcessor
from app.services.obligation.generator import ObligationGenerator
from app.websockets.manager import manager as websocket_manager

router = APIRouter()


def _obligation_to_response(obligation) -> ObligationResponse:
    """Convert Obligation model to ObligationResponse schema."""
    ob_dict = {
        "id": obligation.id,
        "client_id": obligation.client_id,
        "client_name": obligation.client.razao_social if obligation.client else "",
        "client_cnpj": obligation.client.cnpj if obligation.client else "",
        "obligation_type_id": obligation.obligation_type_id,
        "obligation_type_name": obligation.obligation_type.name if obligation.obligation_type else "",
        "obligation_type_code": obligation.obligation_type.code if obligation.obligation_type else "",
        "due_date": obligation.due_date,
        "status": obligation.status,
        "priority": obligation.priority,
        "description": obligation.description,
        "receipt_url": obligation.receipt_url,
        "completed_at": obligation.completed_at,
        "completed_by_name": None,
        "created_at": obligation.created_at,
        "updated_at": obligation.updated_at,
    }
    return ObligationResponse.model_validate(ob_dict)


@router.get("", response_model=ObligationListResponse)
async def list_obligations(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    client_id: Optional[UUID] = Query(None),
    status: Optional[ObligationStatus] = Query(None),
    year: Optional[int] = Query(None),
    month: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
):
    """
    List obligations with filters.

    - Admin/Func: Can see all obligations (client_id optional)
    - Client: Can only see their own obligations
    """
    repo = ObligationRepository(db)

    # If user is client, override client_id filter
    if current_user.role == UserRole.CLIENTE:
        # Get client associated with this user
        client_repo = ClientRepository(db)
        client = await client_repo.get_by_user_id(current_user.id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client profile not found",
            )
        client_id = client.id
    # Admin/Func can see all obligations if client_id is not provided

    obligations, total = await repo.list_by_client(
        client_id=client_id,
        status=status,
        year=year,
        month=month,
        skip=skip,
        limit=limit,
    )

    # Convert to response format with client info
    items = [_obligation_to_response(ob) for ob in obligations]

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/{obligation_id}", response_model=ObligationResponse)
async def get_obligation(
    obligation_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Get obligation by ID."""
    repo = ObligationRepository(db)
    obligation = await repo.get_by_id_with_relations(obligation_id)

    if not obligation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Obligation not found",
        )

    # Check access: clients can only see their own
    if current_user.role == UserRole.CLIENTE:
        client_repo = ClientRepository(db)
        client = await client_repo.get_by_user_id(current_user.id)
        if not client or obligation.client_id != client.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this obligation",
            )

    return _obligation_to_response(obligation)


@router.post("/generate", response_model=ObligationGenerateResponse)
async def generate_obligations(
    request: ObligationGenerateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Generate obligations for a specific month.

    Admin/Func only.
    Can generate for one client or all clients.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.FUNC]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin/func can generate obligations",
        )

    generator = ObligationGenerator(db)

    if request.client_id:
        # Generate for specific client
        client_repo = ClientRepository(db)
        client = await client_repo.get(request.client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found",
            )

        obligations = await generator.generate_for_client(
            client=client,
            year=request.year,
            month=request.month,
            generated_by_id=current_user.id,
        )

        return {
            "success": True,
            "total_obligations": len(obligations),
            "obligations": obligations,
        }
    else:
        # Generate for all clients
        stats = await generator.generate_for_all_clients(
            year=request.year,
            month=request.month,
            generated_by_id=current_user.id,
        )

        return {
            "success": True,
            "total_clients": stats["total_clients"],
            "total_obligations": stats["total_obligations"],
            "errors": stats["errors"],
        }


@router.post("/{obligation_id}/receipt", response_model=ObligationResponse)
async def upload_receipt(
    obligation_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    file: Annotated[UploadFile, File()],
    notes: Annotated[Optional[str], Form()] = None,
):
    """
    Upload receipt for an obligation and mark as completed.

    Admin/Func only.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.FUNC]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin/func can upload receipts",
        )

    # Validate file type
    allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: PDF, JPEG, PNG",
        )

    # Validate file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    contents = await file.read()
    if len(contents) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 10MB limit",
        )

    # Save file (simplified - in production use proper storage service)
    import os
    from pathlib import Path

    upload_dir = Path("/var/uploads/receipts")
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{obligation_id}_{timestamp}_{file.filename}"
    file_path = upload_dir / filename

    with open(file_path, "wb") as f:
        f.write(contents)

    receipt_url = f"/uploads/receipts/{filename}"

    # Process receipt
    processor = ObligationProcessor(db, websocket_manager)
    obligation = await processor.process_receipt(
        obligation_id=obligation_id,
        receipt_url=receipt_url,
        processed_by_id=current_user.id,
        notes=notes,
    )

    # Reload with relations
    repo = ObligationRepository(db)
    obligation = await repo.get_by_id_with_relations(obligation_id)
    return _obligation_to_response(obligation)


@router.put("/{obligation_id}/due-date", response_model=ObligationResponse)
async def update_due_date(
    obligation_id: UUID,
    request: ObligationUpdateDueDateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Update obligation due date.

    Admin/Func only.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.FUNC]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin/func can update due dates",
        )

    processor = ObligationProcessor(db, websocket_manager)
    obligation = await processor.update_due_date(
        obligation_id=obligation_id,
        new_due_date=request.new_due_date,
        reason=request.reason,
        performed_by_id=current_user.id,
    )

    # Reload with relations
    repo = ObligationRepository(db)
    obligation = await repo.get_by_id_with_relations(obligation_id)
    return _obligation_to_response(obligation)


@router.post("/{obligation_id}/cancel", response_model=ObligationResponse)
async def cancel_obligation(
    obligation_id: UUID,
    request: ObligationCancelRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Cancel an obligation.

    Admin/Func only.
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.FUNC]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin/func can cancel obligations",
        )

    processor = ObligationProcessor(db, websocket_manager)
    obligation = await processor.cancel_obligation(
        obligation_id=obligation_id,
        reason=request.reason,
        performed_by_id=current_user.id,
    )

    # Reload with relations
    repo = ObligationRepository(db)
    obligation = await repo.get_by_id_with_relations(obligation_id)
    return _obligation_to_response(obligation)


@router.post("/{obligation_id}/reopen", response_model=ObligationResponse)
async def reopen_obligation(
    obligation_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    notes: Optional[str] = None,
):
    """
    Reopen obligation (mark as pending again).

    Admin only.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can reopen obligations",
        )

    processor = ObligationProcessor(db, websocket_manager)
    obligation = await processor.mark_as_pending(
        obligation_id=obligation_id,
        performed_by_id=current_user.id,
        notes=notes,
    )

    # Reload with relations
    repo = ObligationRepository(db)
    obligation = await repo.get_by_id_with_relations(obligation_id)
    return _obligation_to_response(obligation)


@router.get("/{obligation_id}/events", response_model=list[ObligationEventResponse])
async def get_obligation_events(
    obligation_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
):
    """Get timeline of events for an obligation."""
    # Verify access to obligation
    repo = ObligationRepository(db)
    obligation = await repo.get(obligation_id)

    if not obligation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Obligation not found",
        )

    # Check access: clients can only see their own
    if current_user.role == UserRole.CLIENTE:
        client_repo = ClientRepository(db)
        client = await client_repo.get_by_user_id(current_user.id)
        if not client or obligation.client_id != client.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this obligation",
            )

    # Get events
    event_repo = ObligationEventRepository(db)
    events = await event_repo.list_by_obligation(
        obligation_id=obligation_id,
        skip=skip,
        limit=limit,
    )

    return events


@router.get("/upcoming/pending", response_model=list[ObligationResponse])
async def get_upcoming_obligations(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    days_ahead: int = Query(7, ge=1, le=90),
):
    """
    Get pending obligations due in the next X days.

    Admin/Func: See all
    Client: See only their own
    """
    generator = ObligationGenerator(db)
    obligations = await generator.check_pending_obligations(days_ahead=days_ahead)

    # Filter for clients
    if current_user.role == UserRole.CLIENTE:
        client_repo = ClientRepository(db)
        client = await client_repo.get_by_user_id(current_user.id)
        if client:
            obligations = [o for o in obligations if o.client_id == client.id]
        else:
            obligations = []

    # Load relations and convert to response
    repo = ObligationRepository(db)
    obligations_with_relations = []
    for ob in obligations:
        ob_with_relations = await repo.get_by_id_with_relations(ob.id)
        if ob_with_relations:
            obligations_with_relations.append(_obligation_to_response(ob_with_relations))

    return obligations_with_relations


@router.get("/overdue/list", response_model=list[ObligationResponse])
async def get_overdue_obligations(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Get all overdue obligations.

    Admin/Func: See all
    Client: See only their own
    """
    generator = ObligationGenerator(db)
    obligations = await generator.get_overdue_obligations()

    # Filter for clients
    if current_user.role == UserRole.CLIENTE:
        client_repo = ClientRepository(db)
        client = await client_repo.get_by_user_id(current_user.id)
        if client:
            obligations = [o for o in obligations if o.client_id == client.id]
        else:
            obligations = []

    # Load relations and convert to response
    repo = ObligationRepository(db)
    obligations_with_relations = []
    for ob in obligations:
        ob_with_relations = await repo.get_by_id_with_relations(ob.id)
        if ob_with_relations:
            obligations_with_relations.append(_obligation_to_response(ob_with_relations))

    return obligations_with_relations
