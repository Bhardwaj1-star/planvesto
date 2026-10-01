"""Risk profile adapter.

Delegates directly to the authoritative RiskProfilerEngine in engines.risk_profiler.
"""
from __future__ import annotations

from engines.risk_profiler.engine import RiskProfilerEngine, build_risk_profile

__all__ = ["RiskProfilerEngine", "build_risk_profile"]
