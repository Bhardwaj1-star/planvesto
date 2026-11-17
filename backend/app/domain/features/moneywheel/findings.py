"""
domain/features/moneywheel/findings.py
Chapter 09 §2 Structured Assessment Output.

Structured diagnostic finding model:
- Finding: specific strength, vulnerability or exposure
- Evidence: supporting facts and calculated metrics
- Impact: consequence for ability to meet obligations or absorb disruption
- Uncertainty: missing or assumption-dependent info
- Investor consideration: practical question or trade-off
"""

from dataclasses import dataclass
from enum import Enum


class ResilienceDimension(str, Enum):
    """Chapter 09 §3 Resilience Dimensions."""
    ACCESS_TO_MONEY = "access_to_money"
    CASH_FLOW_CONTINUITY = "cash_flow_continuity"
    DEBT_PRESSURE = "debt_pressure"
    PROTECTION_GAPS = "protection_gaps"
    CONCENTRATION_DEPENDENCY = "concentration_dependency"


@dataclass(frozen=True)
class AssessmentFinding:
    """Chapter 09 §2 Structured Diagnostic Finding."""
    dimension: ResilienceDimension
    finding: str
    evidence: str
    impact: str
    uncertainty: str
    investor_consideration: str
