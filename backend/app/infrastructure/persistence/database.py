"""Database connection and session access helpers."""

from typing import Any, Dict
from app.infrastructure.providers.supabase.client import get_supabase_client
from app.core.exceptions import DatabaseConnectionError
from app.core.logging import get_logger

logger = get_logger(__name__)


def get_db_client():
    """Return persistence client (Supabase / Postgres client)."""
    return get_supabase_client()


def check_database_health() -> Dict[str, Any]:
    """Test connectivity to persistence backend and report status."""
    try:
        client = get_db_client()
        # Ping table with a lightweight query or auth check
        res = client.table("planning_units").select("planning_unit_id").limit(1).execute()
        return {"connected": True, "provider": "supabase_postgresql"}
    except Exception as exc:
        logger.warning(f"Database connectivity check encountered issue: {exc}")
        return {"connected": False, "provider": "supabase_postgresql", "error": str(exc)}
