"""Supabase identity provider adapter for verifying user tokens."""

from typing import Optional
from app.infrastructure.providers.supabase.client import get_supabase_client
from app.core.exceptions import AuthenticationError
from app.core.logging import get_logger

logger = get_logger(__name__)


def verify_supabase_token(token: str) -> str:
    """Verify bearer token against Supabase auth API and return authenticated user ID."""
    if not token or not token.strip():
        raise AuthenticationError("Authorization token required")

    clean_token = token.removeprefix("Bearer ").strip()
    if not clean_token:
        raise AuthenticationError("Authorization token required")

    try:
        supabase = get_supabase_client()
        result = supabase.auth.get_user(clean_token)
    except Exception as exc:
        logger.warning("Token verification rejected by Supabase auth provider.")
        raise AuthenticationError("Invalid authorization token") from exc

    user = getattr(result, "user", None)
    if not user or not getattr(user, "id", None):
        raise AuthenticationError("Invalid authorization token")

    return str(user.id)
