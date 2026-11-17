"""
domain/features/goal_planner/requirement.py
Chapter 10 — Goal Requirement Planning (§10.1, §10.2)

Inputs:
- Canonical goal (Chapter 03 CanonicalGoalId)
- Today's cost
- Target date / timeline
- Applicable inflation rate (goal-specific, no universal 6%)
- Assets mapped to the goal, if any
- Existing SIP linked to the goal, if any

Outputs:
- Future Goal Target
- Funding Gap
- Required Return (only when assets are mapped to the goal)
"""

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List, Optional

from app.domain.canonical.goal_taxonomy import CanonicalGoalId
from app.domain.shared.value_objects import Money, Rate
from app.domain.shared.constraints import (
    ConstraintEvaluationResult,
    evaluate_asset_availability_gate,
)
from app.domain.shared.calculations.goal_funding import (
    calculate_future_goal_target,
    calculate_projected_asset_value,
    calculate_goal_funding_gap,
    calculate_risk_required_return,
)
from app.domain.features.investor_profile.financial_state.models import AssetRecord


@dataclass
class GoalInstance:
    """Canonical goal instance carrying investor requirements (§10.2)."""
    id: str
    investor_id: str
    canonical_id: CanonicalGoalId
    name: str  # Custom label or display name
    target_date: date
    current_cost: Money
    applicable_inflation_rate: Rate  # Goal-specific inflation (no universal 6%)
    expected_annual_return: Rate     # Investment-mix specific return
    created_at: date
    priority: int = 1  # Investor preference ranking (1 = highest)
    mapped_assets: List[AssetRecord] = field(default_factory=list)
    existing_goal_sip: Money = field(default_factory=Money.zero)
    notes: Optional[str] = None


@dataclass(frozen=True)
class GoalRequirementOutput:
    """Outputs produced by Goal Requirement Planning (§10.2)."""
    goal_id: str
    goal_canonical_id: CanonicalGoalId
    future_goal_target: Money
    projected_existing_funding: Money
    funding_gap: Money
    required_return: Optional[Rate]  # Only when assets are mapped
    duration_years: Decimal
    months_horizon: int
    asset_constraint_evaluations: List[ConstraintEvaluationResult]


GoalRequirement = GoalRequirementOutput


def plan_goal_requirement(
    goal: GoalInstance,
    evaluation_date: date,
) -> GoalRequirementOutput:
    """
    Computes Chapter 10 §10.2 Goal Requirement:
    Target date horizon, Future Target, Mapped asset availability (CTR-LIQ-001),
    Funding Gap, and Required Return (when assets mapped).
    """
    days = (goal.target_date - evaluation_date).days
    if days <= 0:
        months_horizon = 0
        duration_years = Decimal("0.0")
    else:
        duration_years = Decimal(str(days)) / Decimal("365.25")
        months_horizon = max(1, int(days / 30.4375))

    future_target = calculate_future_goal_target(
        current_cost=goal.current_cost,
        annual_inflation_rate=goal.applicable_inflation_rate,
        duration_years=duration_years,
    )

    constraint_evaluations: List[ConstraintEvaluationResult] = []
    eligible_projected_assets = Money.zero(currency=goal.current_cost.currency)
    total_current_mapped_assets = Money.zero(currency=goal.current_cost.currency)

    for asset in goal.mapped_assets:
        liq_gate = evaluate_asset_availability_gate(
            asset_id=asset.id,
            asset_name=asset.name,
            asset_value=asset.effective_value,
            is_accessible=asset.is_accessible,
            access_restrictions=asset.access_restrictions,
            is_already_committed=asset.is_committed,
            committed_goal_id=asset.committed_goal_id,
        )
        constraint_evaluations.append(liq_gate)

        if liq_gate.is_satisfied:
            total_current_mapped_assets = total_current_mapped_assets + asset.effective_value
            proj_val = calculate_projected_asset_value(
                current_allocated=asset.effective_value,
                periodic_return=goal.expected_annual_return,
                periods=duration_years,
            )
            eligible_projected_assets = eligible_projected_assets + proj_val

    funding_gap = calculate_goal_funding_gap(future_target, eligible_projected_assets)

    required_return: Optional[Rate] = None
    if total_current_mapped_assets.is_positive and duration_years > Decimal(0):
        required_return = calculate_risk_required_return(
            future_goal_target=future_target,
            current_goal_funding=total_current_mapped_assets,
            duration_years=duration_years,
        )

    return GoalRequirementOutput(
        goal_id=goal.id,
        goal_canonical_id=goal.canonical_id,
        future_goal_target=future_target,
        projected_existing_funding=eligible_projected_assets,
        funding_gap=funding_gap,
        required_return=required_return,
        duration_years=duration_years,
        months_horizon=months_horizon,
        asset_constraint_evaluations=constraint_evaluations,
    )
