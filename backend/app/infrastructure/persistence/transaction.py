"""Unit of work and transaction mechanics."""

from contextlib import contextmanager
from typing import Generator
from app.core.logging import get_logger

logger = get_logger(__name__)


@contextmanager
def transaction() -> Generator[None, None, None]:
    """Provide a transaction block for atomic operations.
    
    When using Supabase REST API, individual calls are atomic; this context manager
    provides a consistent port contract for future direct Postgres/SQLAlchemy connections.
    """
    try:
        yield
    except Exception as exc:
        logger.error(f"Transaction rolled back due to error: {exc}")
        raise
