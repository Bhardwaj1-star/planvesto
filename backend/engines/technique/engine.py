from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from models.defined_goal import DefinedGoal


@dataclass(frozen=True)
class TechniqueEngineResult:
    """Deterministic output of one executable financial-planning technique."""

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
            "projected_value": max(0.0, float(item.projected_value)),
        }
        for item in goal.mapped_assets
        if float(item.allocated_amount) > 0
    ]


def _future_value_monthly(monthly: float, annual_return: float, years: float) -> float:
    months = max(0, round(years * 12))
    if months == 0 or monthly <= 0:
        return 0.0
    rate = annual_return / 12.0
    if abs(rate) < 1e-12:
        return monthly * months
    return monthly * (((1 + rate) ** months - 1) / rate)


def _future_value_step_up(
    starting_monthly: float,
    annual_step_up: float,
    annual_return: float,
    years: float,
) -> float:
    whole_years = max(0, round(years))
    if whole_years == 0 or starting_monthly <= 0:
        return 0.0
    total = 0.0
    for year in range(whole_years):
        monthly = starting_monthly * ((1 + annual_step_up) ** year)
        annual_stream = _future_value_monthly(monthly, annual_return, 1.0)
        total += annual_stream * ((1 + annual_return) ** (whole_years - year - 1))
    return total


def _execute_bucketing(goal: DefinedGoal, p: dict[str, Any]) -> TechniqueEngineResult:
    years = max(0.0, float(goal.duration_years))
    target = max(0.0, float(goal.future_target))
    resources = _asset_resources(goal)
    corpus = sum(x["amount"] for x in resources)
    count = max(1, min(5, int(p.get("bucket_count", 3 if years > 3 else 2))))
    step = years / count if years else 0.0
    weights = [1.0 / (i + 1) for i in range(count)]
    total_weight = sum(weights)
    targets = [target * w / total_weight for w in weights]
    remaining = corpus
    buckets = []
    for i, required in enumerate(targets):
        start = i * step
        end = years if i == count - 1 else (i + 1) * step
        allocated = min(remaining, required)
        remaining -= allocated
        buckets.append({
            "bucket": i + 1,
            "horizon_start_year": _pct(start),
            "horizon_end_year": _pct(end),
            "target_amount": _money(required),
            "mapped_resource_amount": _money(allocated),
            "funding_gap": _money(max(0.0, required - allocated)),
            "role": "near_term" if i == 0 else ("long_term_growth" if i == count - 1 else "intermediate"),
        })
    return TechniqueEngineResult(
        "tech-bucketing", "calculated",
        {"goal_id": goal.goal_id, "duration_years": years, "future_target": _money(target), "mapped_resources": resources},
        {"bucket_count": count},
        {"buckets": buckets, "mapped_resource_total": _money(corpus), "goal_target": _money(target),
         "unallocated_resources": _money(remaining), "overall_funding_gap": _money(max(0.0, target - corpus))},
        ["Mapped resources do not fully fund the target; bucket gaps remain."] if target > corpus else [],
    )


def _execute_glide_path(goal: DefinedGoal, p: dict[str, Any]) -> TechniqueEngineResult:
    years = max(0.0, float(goal.duration_years))
    start = max(0.0, min(100.0, float(p.get("starting_growth_pct", 80.0))))
    end = max(0.0, min(100.0, float(p.get("ending_growth_pct", 20.0))))
    transition = max(0.0, min(years, float(p.get("transition_years", min(5.0, years)))))
    points = max(1, int(round(transition)))
    schedule = []
    for elapsed in range(points + 1):
        progress = 1.0 if transition == 0 else min(1.0, elapsed / transition)
        growth = start + (end - start) * progress
        schedule.append({
            "years_to_goal": _pct(max(0.0, years - elapsed)),
            "growth_allocation_pct": _pct(growth),
            "safety_allocation_pct": _pct(100.0 - growth),
        })
    return TechniqueEngineResult(
        "tech-glide-path", "calculated",
        {"goal_id": goal.goal_id, "duration_years": years, "funding_status": goal.funding_status},
        {"starting_growth_pct": _pct(start), "ending_growth_pct": _pct(end), "transition_years": _pct(transition)},
        {"schedule": schedule, "initial_growth_allocation_pct": _pct(start),
         "terminal_growth_allocation_pct": _pct(end), "de_risking_range_pct": _pct(start - end)},
        ["Goal is already at or beyond its target date."] if years <= 0 else [],
    )


def _execute_laddering(goal: DefinedGoal, p: dict[str, Any]) -> TechniqueEngineResult:
    years = max(0.0, float(goal.duration_years))
    target = max(0.0, float(goal.future_target))
    rungs = max(1, min(15, int(p.get("rung_count", max(1, round(years))))))
    amount = target / rungs if rungs else target
    schedule = [
        {"rung": i + 1, "years_to_goal": _pct(years * (i + 1) / rungs), "target_amount": _money(amount)}
        for i in range(rungs)
    ]
    return TechniqueEngineResult(
        "tech-laddering", "calculated",
        {"goal_id": goal.goal_id, "duration_years": years, "future_target": _money(target)},
        {"rung_count": rungs},
        {"rungs": schedule, "total_target_amount": _money(sum(x["target_amount"] for x in schedule)),
         "average_rung_amount": _money(amount)},
        ["Rung sizing is a planning schedule; no specific financial product is selected by this engine."],
    )


def _execute_cashflow_matching(goal: DefinedGoal, p: dict[str, Any]) -> TechniqueEngineResult:
    years = max(1.0, float(goal.duration_years))
    target = max(0.0, float(goal.future_target))
    annual_need = target / years
    monthly_need = annual_need / 12.0
    resources = _asset_resources(goal)
    resource_total = sum(x["amount"] for x in resources)
    coverage_years = resource_total / annual_need if annual_need > 0 else 0.0
    return TechniqueEngineResult(
        "tech-cashflow-matching", "calculated",
        {"goal_id": goal.goal_id, "duration_years": goal.duration_years, "future_target": _money(target),
         "mapped_resource_total": _money(resource_total)},
        {"cashflow_frequency": p.get("cashflow_frequency", "annual")},
        {"annual_target_cashflow": _money(annual_need), "monthly_target_cashflow": _money(monthly_need),
         "mapped_resource_coverage_years": _pct(coverage_years),
         "terminal_funding_gap": _money(max(0.0, target - resource_total))},
        ["This is a deterministic planning proxy because the goal model does not contain a dated cash-flow stream."],
    )


def _execute_asset_earmarking(goal: DefinedGoal, p: dict[str, Any]) -> TechniqueEngineResult:
    target = max(0.0, float(goal.future_target))
    resources = _asset_resources(goal)
    total = sum(x["amount"] for x in resources)
    earmarked = [
        {"asset_id": x["asset_id"], "asset_name": x["asset_name"], "earmarked_amount": _money(x["amount"]),
         "earmarked_pct_of_mapped": _pct((x["amount"] / total * 100) if total else 0)}
        for x in resources
    ]
    return TechniqueEngineResult(
        "tech-asset-earmarking", "calculated",
        {"goal_id": goal.goal_id, "future_target": _money(target), "mapped_resources": resources},
        {"allow_unallocated": bool(p.get("allow_unallocated", True))},
        {"earmarked_assets": earmarked, "earmarked_total": _money(total),
         "target_coverage_pct": _pct((total / target * 100) if target else 100),
         "unfunded_target": _money(max(0.0, target - total))},
        [],
    )


def _execute_contribution_escalation(goal: DefinedGoal, p: dict[str, Any]) -> TechniqueEngineResult:
    starting = max(0.0, float(p.get("starting_monthly_contribution", goal.required_monthly_contribution or 0.0)))
    step_up = max(0.0, min(1.0, float(p.get("annual_step_up", 0.10))))
    annual_return = float(p.get("annual_return", goal.funding_return_assumption))
    years = max(0.0, float(goal.duration_years))
    schedule = [
        {"year": y + 1, "monthly_contribution": _money(starting * ((1 + step_up) ** y))}
        for y in range(max(0, round(years)))
    ]
    fv = _future_value_step_up(starting, step_up, annual_return, years)
    return TechniqueEngineResult(
        "tech-contribution-escalation", "calculated",
        {"goal_id": goal.goal_id, "duration_years": years, "future_target": _money(goal.future_target)},
        {"starting_monthly_contribution": _money(starting), "annual_step_up": _pct(step_up),
         "annual_return": _pct(annual_return)},
        {"schedule": schedule, "projected_future_value": _money(fv),
         "projected_gap_reduction": _money(min(fv, max(0.0, goal.future_target)))},
        [],
    )


def _execute_barbell(goal: DefinedGoal, p: dict[str, Any]) -> TechniqueEngineResult:
    total = sum(x["amount"] for x in _asset_resources(goal))
    safety = max(0.0, min(100.0, float(p.get("safety_allocation_pct", 50.0))))
    growth = 100.0 - safety
    return TechniqueEngineResult(
        "tech-barbell", "calculated",
        {"goal_id": goal.goal_id, "mapped_resource_total": _money(total)},
        {"safety_allocation_pct": _pct(safety), "growth_allocation_pct": _pct(growth)},
        {"safety_amount": _money(total * safety / 100), "growth_amount": _money(total * growth / 100),
         "total_allocated": _money(total)},
        ["Allocation sleeves are strategic buckets; no individual products are selected."],
    )


def _execute_goal_segmentation(goal: DefinedGoal, p: dict[str, Any]) -> TechniqueEngineResult:
    """Segment one goal's funding requirement when multi-goal context is absent.

    If parameters['goals'] is supplied, each goal is segmented independently
    and the aggregate target is returned. This keeps the technique executable
    without changing the persistence model.
    """
    supplied = p.get("goals")
    goals = supplied if isinstance(supplied, list) and supplied else [{
        "goal_id": goal.goal_id, "goal_name": goal.goal_name, "priority": goal.priority,
        "target": float(goal.future_target), "funding_gap": float(goal.funding_gap),
    }]
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    segments = sorted(
        [{
            "goal_id": str(g.get("goal_id", "")),
            "goal_name": str(g.get("goal_name", "")),
            "priority": str(g.get("priority", "medium")),
            "target": _money(max(0.0, float(g.get("target", g.get("future_target", 0.0))))),
            "funding_gap": _money(max(0.0, float(g.get("funding_gap", 0.0)))),
        } for g in goals],
        key=lambda x: priority_order.get(x["priority"].lower(), 9),
    )
    return TechniqueEngineResult(
        "tech-goal-segmentation", "calculated",
        {"goal_id": goal.goal_id, "goal_count": len(segments)},
        {"segmentation_basis": p.get("segmentation_basis", "priority")},
        {"segments": segments, "aggregate_target": _money(sum(x["target"] for x in segments)),
         "aggregate_funding_gap": _money(sum(x["funding_gap"] for x in segments))},
        ["Only supplied goal context is segmented; the engine does not invent missing goals or priorities."],
    )


def _execute_tax_sequencing(goal: DefinedGoal, p: dict[str, Any]) -> TechniqueEngineResult:
    sources = p.get("funding_sources")
    if not isinstance(sources, list) or not sources:
        return TechniqueEngineResult(
            "tech-tax-efficient-sequencing", "insufficient_inputs",
            {"goal_id": goal.goal_id}, p, {},
            ["Funding-source tax treatment is not present in the goal model; provide funding_sources with tax_rate/tax_treatment."],
        )
    ordered = sorted(sources, key=lambda x: float(x.get("tax_rate", 1.0)))
    return TechniqueEngineResult(
        "tech-tax-efficient-sequencing", "calculated",
        {"goal_id": goal.goal_id, "source_count": len(ordered)}, p,
        {"sequence": [{"source_id": s.get("source_id"), "tax_rate": _pct(float(s.get("tax_rate", 0))),
                       "available_amount": _money(float(s.get("available_amount", 0)))} for s in ordered]},
        ["Ordering is based only on supplied tax rates; jurisdiction-specific tax law is not inferred."],
    )


def _execute_tax_loss_harvesting(goal: DefinedGoal, p: dict[str, Any]) -> TechniqueEngineResult:
    lots = p.get("tax_lots")
    if not isinstance(lots, list) or not lots:
        return TechniqueEngineResult(
            "tech-tax-loss-harvesting", "insufficient_inputs",
            {"goal_id": goal.goal_id}, p, {},
            ["Tax-lot cost basis and realised/unrealised gain data are required; the goal model does not contain them."],
        )
    candidates = []
    for lot in lots:
        cost = max(0.0, float(lot.get("cost_basis", 0)))
        value = max(0.0, float(lot.get("current_value", 0)))
        loss = max(0.0, cost - value)
        if loss > 0:
            candidates.append({
                "lot_id": lot.get("lot_id"),
                "unrealised_loss": _money(loss),
                "loss_pct_of_cost": _pct(loss / cost * 100 if cost else 0),
            })
    return TechniqueEngineResult(
        "tech-tax-loss-harvesting", "calculated",
        {"goal_id": goal.goal_id, "tax_lot_count": len(lots)}, p,
        {"harvest_candidates": candidates, "total_unrealised_loss": _money(sum(x["unrealised_loss"] for x in candidates))},
        ["Eligibility, wash-sale rules and tax offsets must be validated outside this generic calculation layer."],
    )


class TechniqueEngine:
    """Dispatcher for all canonical techniques.

    Execution means deterministic planning calculation. It does not select
    financial products and does not infer unavailable tax/legal inputs.
    """

    SUPPORTED = {
        "tech-bucketing", "tech-laddering", "tech-glide-path",
        "tech-cashflow-matching", "tech-barbell", "tech-asset-earmarking",
        "tech-goal-segmentation", "tech-contribution-escalation",
        "tech-tax-efficient-sequencing", "tech-tax-loss-harvesting",
    }

    HANDLERS = {
        "tech-bucketing": _execute_bucketing,
        "tech-laddering": _execute_laddering,
        "tech-glide-path": _execute_glide_path,
        "tech-cashflow-matching": _execute_cashflow_matching,
        "tech-barbell": _execute_barbell,
        "tech-asset-earmarking": _execute_asset_earmarking,
        "tech-goal-segmentation": _execute_goal_segmentation,
        "tech-contribution-escalation": _execute_contribution_escalation,
        "tech-tax-efficient-sequencing": _execute_tax_sequencing,
        "tech-tax-loss-harvesting": _execute_tax_loss_harvesting,
    }

    def execute(
        self,
        technique_id: str,
        goal: DefinedGoal,
        parameters: dict[str, Any] | None = None,
    ) -> TechniqueEngineResult:
        params = dict(parameters or {})
        handler = self.HANDLERS.get(technique_id)
        if handler is None:
            return TechniqueEngineResult(
                technique_id=technique_id,
                status="not_implemented",
                inputs={"goal_id": goal.goal_id},
                parameters=params,
                warnings=[f"Executable implementation is not registered for {technique_id}."],
            )
        return handler(goal, params)

    def execute_many(
        self,
        technique_ids: list[str],
        goal: DefinedGoal,
        parameters: dict[str, Any] | None = None,
    ) -> list[TechniqueEngineResult]:
        return [self.execute(tid, goal, parameters) for tid in dict.fromkeys(technique_ids)]
