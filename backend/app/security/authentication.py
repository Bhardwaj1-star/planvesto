"""Backend validation of the authenticated identity presented for a request."""

from typing import Optional
from fastapi import Header, HTTPException
from app.infrastructure.providers.supabase.identity import verify_supabase_token
from app.core.exceptions import AuthenticationError


def authenticate_request(authorization: Optional[str]) -> str:
    """Validate Authorization header and return verified server-side user ID."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token required")
    try:
        return verify_supabase_token(authorization)
    except AuthenticationError as exc:
        raise HTTPException(status_code=401, detail=exc.message) from exc
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid authorization token") from exc


def get_authenticated_user_id(authorization: Optional[str] = Header(None)) -> str:
    """FastAPI dependency to extract verified current user ID from Authorization header."""
    return authenticate_request(authorization)
