"""Canonical planning assumption definitions."""

# Explicit planning baseline used only when a goal has no mapped assets carrying
# an expected return. This is not a universal market-return promise.
DEFAULT_FUNDING_RETURN_ASSUMPTION = 0.08


def normalize_annual_return(value: float | int | None) -> float:
    """Return a validated nominal annual assumption as a decimal."""
    if value is None:
        return DEFAULT_FUNDING_RETURN_ASSUMPTION
    result = float(value)
    if result <= -1.0:
        raise ValueError("Annual return assumption must be greater than -100%")
    return result
