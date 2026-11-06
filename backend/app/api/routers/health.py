"""Health check and root diagnostic router."""

from fastapi import APIRouter
from app.core.settings import get_settings
from app.infrastructure.persistence.database import check_database_health

router = APIRouter(tags=["Health"])


@router.get("/")
def root():
    """Root endpoint for status check."""
    settings = get_settings()
    return {
        "service": settings.app_title,
        "status": "running",
        "version": settings.api_version,
    }


@router.get("/health")
def health():
    """Standard health check endpoint reporting service and database connectivity."""
    settings = get_settings()
    db_status = check_database_health()
    status_text = "healthy" if db_status.get("connected", True) else "degraded"
    return {
        "status": status_text,
        "service": settings.app_title,
        "version": settings.api_version,
        "environment": settings.environment,
        "database": db_status.get("connected", False),
    }
