"""
domain/features/history/__init__.py
History domain feature exports.
"""

from app.domain.features.history.history_records import (
    HistoricalRecordType,
    HistoryAuditRecord,
)

__all__ = [
    "HistoricalRecordType",
    "HistoryAuditRecord",
]
