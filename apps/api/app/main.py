"""
FastAPI application entry point.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import db_manager

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan events.
    Startup and shutdown logic.
    """
    # Startup
    logger.info("Starting application...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

    # Test database connection
    try:
        async for _ in db_manager.get_session():
            logger.info("✓ Database connection successful")
            break
    except Exception as e:
        logger.error(f"✗ Database connection failed: {e}")

    yield

    # Shutdown
    logger.info("Shutting down application...")
    await db_manager.close()
    logger.info("✓ Database connections closed")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="API para sistema de gestão contábil",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


# Root endpoint
@app.get("/", include_in_schema=False)
async def root() -> JSONResponse:
    """Root endpoint."""
    return JSONResponse(
        {
            "message": "SaaS Contábil API",
            "version": "0.1.0",
            "docs": "/docs",
            "health": f"{settings.API_V1_STR}/health",
        }
    )


# Exception handlers can be added here
# @app.exception_handler(CustomException)
# async def custom_exception_handler(request, exc):
#     return JSONResponse(status_code=400, content={"message": str(exc)})
