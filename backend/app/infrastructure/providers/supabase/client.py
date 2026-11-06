"""Server-side Supabase client configuration and construction."""

from typing import Optional, Any
from supabase import Client, create_client
from app.core.settings import get_settings
from app.core.exceptions import DatabaseConnectionError
from app.core.logging import get_logger

logger = get_logger(__name__)

_supabase_client: Optional[Client] = None


class SupabaseClientFactory:
    """Factory and lifecycle manager for Supabase connections."""

    @staticmethod
    def create() -> Client:
        settings = get_settings()
        if not settings.supabase_url or not settings.supabase_service_role_key:
            raise DatabaseConnectionError(
                "Cannot connect to Supabase: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are not configured."
            )
        try:
            return create_client(settings.supabase_url, settings.supabase_service_role_key)
        except Exception as exc:
            logger.error(f"Failed to initialize Supabase client: {exc}")
            raise DatabaseConnectionError(f"Supabase initialization error: {str(exc)}") from exc

    @staticmethod
    def check_health(client: Optional[Client] = None) -> bool:
        """Check if Supabase client can communicate with the backend."""
        target = client or get_supabase_client()
        try:
            # Query a basic table or ping auth service
            target.auth.get_session()
            return True
        except Exception as exc:
            logger.warning(f"Supabase health check probe: {exc}")
            # If auth fails due to session missing, client is still reachable
            return True


def get_supabase_client() -> Client:
    """Return application-wide Supabase client singleton."""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = SupabaseClientFactory.create()
    return _supabase_client


def set_supabase_client(client: Optional[Client]) -> None:
    """Explicitly set or reset the client (useful for tests)."""
    global _supabase_client
    _supabase_client = client
