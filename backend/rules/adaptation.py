"""Authoritative strategy adaptation rules and conditional requirement generators."""
from __future__ import annotations

from typing import Any


def format_cashflow_adaptation(shortfall: float) -> str:
    """Format required change for cash-flow shortfall condition."""
    return f"Increase monthly available surplus by ₹{shortfall:,.2f}"


def format_liquidity_adaptation(liquidity_gap: float) -> str:
    """Format required change for emergency/liquidity gap condition."""
    return f"Maintain additional liquidity of ₹{liquidity_gap:,.2f}"


def format_resource_adaptation(resource_gap: float) -> str:
    """Format required change for asset/resource gap condition."""
    return f"Create/reallocate ₹{resource_gap:,.2f} of required resources"


def format_risk_adaptation() -> str:
    """Format required change for risk-capacity de-risking condition."""
    return "Use the defined de-risked implementation"


def format_multi_goal_adaptation() -> str:
    """Format required change for multi-goal resource reallocation condition."""
    return "Adjust allocation without materially compromising higher-priority goals"


def format_implementation_adaptation() -> str:
    """Format required change for implementation requirement condition."""
    return "Complete the defined implementation changes"
