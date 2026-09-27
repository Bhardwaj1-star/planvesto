"""Deterministic goal fixtures for validating the generic Strategy Engine.

These fixtures intentionally avoid real investor data. They validate architecture
behavior across representative goal types using the same engine contract.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class GoalCase:
    name: str
    goal_type: str
    duration_years: int
    flexibility: str
    priority: str
    funding_status: str = "Shortfall"


GOAL_CASES = (
    GoalCase("retirement", "Retirement / Financial Freedom", 15, "Flexible", "High"),
    GoalCase("education", "Education", 8, "Fixed", "High"),
    GoalCase("home", "Dream Home", 6, "Fixed", "Medium"),
)


def expected_goal_aliases() -> dict[str, str]:
    return {
        "retirement": "retirement",
        "education": "child education",
        "home": "home purchase",
    }
