"""
api/dependencies.py
API layer request-scoped dependencies.
"""

from typing import Optional
from fastapi import Header, HTTPException
from app.security.authentication import authenticate_request
from app.core.config import settings


def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:
    """
    Validates Authorization token.
    In development/testing with no Supabase credentials, falls back to dev user ID.
    """
    if not authorization:
        if settings.ENVIRONMENT in ("development", "testing") and not settings.SUPABASE_URL:
            return "dev-investor-001"
        raise HTTPException(status_code=401, detail="Authorization token required")
    try:
        return authenticate_request(authorization)
    except HTTPException:
        if settings.ENVIRONMENT in ("development", "testing") and not settings.SUPABASE_URL:
            return "dev-investor-001"
        raise
