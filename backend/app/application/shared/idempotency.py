"""
application/shared/idempotency.py
Generic duplicate-operation protection contracts for mutating application commands.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class IdempotencyKey:
    key: str
    investor_id: str
    created_at: datetime
    operation: str


@dataclass
class IdempotencyRecord:
    key: IdempotencyKey
    status: str  # e.g. "PENDING", "COMPLETED", "FAILED"
    cached_response: Optional[dict] = None
