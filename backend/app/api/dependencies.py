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
    In development/testing or with dummy/test credentials, falls back to dev user ID.
    """
    is_test_env = (
        settings.ENVIRONMENT in ("development", "testing")
        or not settings.SUPABASE_URL
        or "example.supabase.co" in settings.SUPABASE_URL
    )
    if not authorization:
        if is_test_env:
            return "dev-investor-001"
        raise HTTPException(status_code=401, detail="Authorization token required")
    try:
        return authenticate_request(authorization)
    except HTTPException:
        if is_test_env:
            return "dev-investor-001"
        raise
