"""Central risk-profiler policy vocabulary and comparison rules."""


def assess_risk_capacity(*, required: float | None, capacity: float | None) -> tuple[str, str]:
    """Compare an investor's risk capacity with a strategy requirement."""
    if required is None or capacity is None:
        return "CONDITIONAL", "Risk-capacity evidence is incomplete"
    if required <= capacity:
        return "PASS", "Strategy risk requirement is within investor risk capacity"
    return "FAIL", "Strategy risk requirement exceeds investor risk capacity"


def strategy_required_risk_capacity(strategy: object) -> float | None:
    """Read the risk-capacity requirement declared by a strategy definition."""
    value = getattr(strategy, "required_risk_capacity", None)
    if value is None:
        value = getattr(strategy, "risk_capacity_required", None)
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None
