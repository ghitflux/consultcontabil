"""
Health check endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Basic health check without database."""
    return {"status": "ok", "message": "API is running"}


@router.get("/health/db")
async def health_check_db(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Health check with database connection test."""
    try:
        # Test database connection
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        return {"status": "ok", "message": "API and database are running"}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}
