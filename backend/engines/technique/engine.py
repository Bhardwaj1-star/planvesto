from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from models.defined_goal import DefinedGoal


@dataclass(frozen=True)
class TechniqueEngineResult:
    """Deterministic output of one executable planning technique."""

    technique_id: str
    status: str
    inputs: dict[str, Any] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def model_dump(self) -> dict[str, Any]:
        return {
            "technique_id": self.technique_id,
            "status": self.status,
            "inputs": self.inputs,
            "parameters": self.parameters,
            "outputs": self.outputs,
            "warnings": self.warnings,
        }


def _money(value: float) -> float:
    return round(float(value), 2)


def _pct(value: float) -> float:
    return round(float(value), 4)


def _asset_resources(goal: DefinedGoal) -> list[dict[str, Any]]:
    return [
        {
            "asset_id": item.asset_id,
            "asset_name": item.asset_name,
            "amount": max(0.0, float(item.allocated_amount)),
            "expected_return": float(item.expected_return),
        }
        for item in goal.mapped_assets
        if float(item.allocated_amount) > 0
    ]


def _execute_bucketing(goal: DefinedGoal, parameters: dict[str, Any]) -> TechniqueEngineResult:
    """Allocate the currently mapped goal resources across time buckets.

    This is intentionally a planning allocation, not a product recommendation.
    Bucket sizing is driven by goal horizon and target, then constrained by the
    resources actually mapped to the goal.
    """
    years = max(0.0, float(goal.duration_years))
    target = max(0.0, float(goal.future_target))
    resources = _asset_resources(goal)
    corpus = sum(item["amount"] for item in resources)
    shortfall = max(0.0, target - corpus)

    requested_count = parameters.get("bucket_count")
    if requested_count is None:
        requested_count = 3 if years > 3 else 2
    bucket_count = max(1, min(5, int(requested_count)))

    # Equal horizon bands are deterministic and transparent. The final bucket
    # absorbs any rounding remainder so total horizon remains exact.
    horizons: list[tuple[float, float]] = []
    if years <= 0:
        horizons = [(0.0, 0.0)]
    else:
        step = years / bucket_count
        for index in range(bucket_count):
            start = index * step
            end = years if index == bucket_count - 1 else (index + 1) * step
            horizons.append((start, end))

    weights = [1.0 / (index + 1) for index in range(bucket_count)]
    weight_total = sum(weights)
    required = target if target > 0 else corpus
    bucket_targets = [required * weight / weight_total for weight in weights]

    remaining = corpus
    buckets: list[dict[str, Any]] = []
    for index, ((start, end), target_amount) in enumerate(zip(horizons, bucket_targets), start=1):
        allocation = min(remaining, target_amount)
        remaining -= allocation
        buckets.append({
            "bucket": index,
            "horizon_start_year": _pct(start),
            "horizon_end_year": _pct(end),
            "target_amount": _money(target_amount),
            "mapped_resource_amount": _money(allocation),
            "funding_gap": _money(max(0.0, target_amount - allocation)),
            "role": "near_term" if index == 1 else ("long_term_growth" if index == bucket_count else "intermediate"),
        })

    return TechniqueEngineResult(
        technique_id="tech-bucketing",
        status="calculated",
        inputs={
            "goal_id": goal.goal_id,
            "duration_years": years,
            "future_target": _money(target),
            "mapped_resources": resources,
        },
        parameters={"bucket_count": bucket_count},
        outputs={
            "buckets": buckets,
            "mapped_resource_total": _money(corpus),
            "goal_target": _money(target),
            "unallocated_resources": _money(remaining),
            "overall_funding_gap": _money(shortfall),
        },
        warnings=(
            ["Mapped resources do not fully fund the target; bucket gaps remain."]
            if shortfall > 0 else []
        ),
    )


def _execute_glide_path(goal: DefinedGoal, parameters: dict[str, Any]) -> TechniqueEngineResult:
    """Generate a deterministic de-risking schedule from time-to-goal."""
    years = max(0.0, float(goal.duration_years))
    start_growth = float(parameters.get("starting_growth_pct", 80.0))
    end_growth = float(parameters.get("ending_growth_pct", 20.0))
    transition_years = float(parameters.get("transition_years", min(5.0, years)))
    transition_years = max(0.0, min(years, transition_years))
    start_growth = max(0.0, min(100.0, start_growth))
    end_growth = max(0.0, min(100.0, end_growth))

    points = max(1, int(round(transition_years)))
    schedule: list[dict[str, Any]] = []
    for elapsed in range(points + 1):
        remaining_years = max(0.0, transition_years - elapsed)
        progress = 1.0 if transition_years == 0 else min(1.0, elapsed / transition_years)
        growth = start_growth + (end_growth - start_growth) * progress
        safety = 100.0 - growth
        schedule.append({
            "years_to_goal": _pct(max(0.0, years - elapsed)),
            "growth_allocation_pct": _pct(growth),
            "safety_allocation_pct": _pct(safety),
        })

    return TechniqueEngineResult(
        technique_id="tech-glide-path",
        status="calculated",
        inputs={
            "goal_id": goal.goal_id,
            "duration_years": years,
            "funding_status": goal.funding_status,
        },
        parameters={
            "starting_growth_pct": _pct(start_growth),
            "ending_growth_pct": _pct(end_growth),
            "transition_years": _pct(transition_years),
        },
        outputs={
            "schedule": schedule,
            "initial_growth_allocation_pct": _pct(start_growth),
            "terminal_growth_allocation_pct": _pct(end_growth),
            "de_risking_range_pct": _pct(start_growth - end_growth),
        },
        warnings=(
            ["Goal is already at or beyond its target date; glide-path schedule collapses to the terminal allocation."]
            if years <= 0 else []
        ),
    )


class TechniqueEngine:
    """Dispatcher for executable canonical financial-planning techniques."""

    SUPPORTED = {"tech-bucketing", "tech-glide-path"}

    def execute(
        self,
        technique_id: str,
        goal: DefinedGoal,
        parameters: dict[str, Any] | None = None,
    ) -> TechniqueEngineResult:
        params = dict(parameters or {})
        if technique_id == "tech-bucketing":
            return _execute_bucketing(goal, params)
        if technique_id == "tech-glide-path":
            return _execute_glide_path(goal, params)
        return TechniqueEngineResult(
            technique_id=technique_id,
            status="not_implemented",
            inputs={"goal_id": goal.goal_id},
            parameters=params,
            warnings=[f"Executable implementation is not yet registered for {technique_id}."],
        )

    def execute_many(
        self,
        technique_ids: list[str],
        goal: DefinedGoal,
        parameters: dict[str, Any] | None = None,
    ) -> list[TechniqueEngineResult]:
        return [self.execute(technique_id, goal, parameters) for technique_id in dict.fromkeys(technique_ids)]
