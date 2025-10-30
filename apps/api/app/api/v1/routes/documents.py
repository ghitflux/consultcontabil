"""
Document upload routes.
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_active_user, get_db, require_admin_or_func
from app.core.config import settings
from app.db.models.user import User

router = APIRouter(prefix="/documents", tags=["documents"])

# Ensure upload directory exists
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    client_id: UUID = None,
    db: Annotated[AsyncSession, Depends(get_db)] = None,
    current_user: User = Depends(require_admin_or_func()),
) -> dict:
    """
    Upload a document for a client.

    Args:
        file: File to upload
        client_id: Optional client ID to associate document with
        db: Database session
        current_user: Current authenticated user

    Returns:
        Document metadata

    Raises:
        HTTPException: If file is too large or invalid
    """
    # Validate file size
    if file.size and file.size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE} bytes"
        )

    # Validate file type (basic validation)
    allowed_extensions = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.jpg', '.jpeg', '.png'}
    file_ext = Path(file.filename).suffix.lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed: {', '.join(allowed_extensions)}"
        )

    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid4())[:8]
    safe_filename = f"{timestamp}_{unique_id}_{file.filename}"

    # Create client directory if client_id provided
    if client_id:
        upload_path = UPLOAD_DIR / str(client_id)
        upload_path.mkdir(parents=True, exist_ok=True)
    else:
        upload_path = UPLOAD_DIR / "general"
        upload_path.mkdir(parents=True, exist_ok=True)

    file_path = upload_path / safe_filename

    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )

    return {
        "success": True,
        "filename": safe_filename,
        "original_filename": file.filename,
        "size": os.path.getsize(file_path),
        "path": str(file_path.relative_to(UPLOAD_DIR)),
        "uploaded_by": current_user.id,
        "uploaded_at": datetime.now().isoformat(),
    }


@router.get("/client/{client_id}", status_code=status.HTTP_200_OK)
async def list_client_documents(
    client_id: UUID,
    current_user: User = Depends(require_admin_or_func()),
) -> dict:
    """
    List all documents for a client.

    Args:
        client_id: Client UUID
        current_user: Current authenticated user

    Returns:
        List of documents
    """
    client_dir = UPLOAD_DIR / str(client_id)

    if not client_dir.exists():
        return {"documents": []}

    documents = []
    for file_path in client_dir.iterdir():
        if file_path.is_file():
            documents.append({
                "filename": file_path.name,
                "size": file_path.stat().st_size,
                "modified_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            })

    return {"documents": documents}
