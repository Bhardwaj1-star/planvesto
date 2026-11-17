"""
domain/features/history/history_records.py
Chapter 15 — History: Financial Record, Decision & Report Audit Trail.

Domain-level contract for identifying, relating and interpreting historical
investor-data records, saved planning runs, reports, and material decision changes.
Non-negotiable invariants:
- Preserves original context, assumptions, calculation versions and evidence.
- History NEVER reruns past calculations using current rules.
- Immutable once recorded.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class HistoricalRecordType(str, Enum):
    FINANCIAL_STATE_SNAPSHOT = "financial_state_snapshot"
    MONEYWHEEL_ASSESSMENT = "moneywheel_assessment"
    GOAL_PLANNER_RUN = "goal_planner_run"
    STRATEGY_BUILDER_ASSESSMENT = "strategy_builder_assessment"
    ACCEPTED_PLAN_EVENT = "accepted_plan_event"
    GENERATED_REPORT = "generated_report"


@dataclass(frozen=True)
class HistoryAuditRecord:
    """Historical record entry preserving original context and version reference."""
    record_id: str
    investor_id: str
    record_type: HistoricalRecordType
    created_at: datetime
    calculation_engine_version: str
    rules_version: str
    payload_snapshot: Dict[str, Any]
    source_provenance: str
    immutable: bool = True
