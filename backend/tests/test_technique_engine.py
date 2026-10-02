from models.defined_goal import DefinedGoal
from engines.technique.engine import TechniqueEngine


def _goal() -> DefinedGoal:
    return DefinedGoal(
        defined_goal_id="dg-tech-001",
        goal_id="goal-tech-001",
        planning_unit_id="pu-tech-001",
        goal_type="Retirement",
        goal_name="Retirement",
        today_cost=10_000_000,
        inflation_rate=0.06,
        target_month=12,
        target_year=2036,
        duration_years=10,
        future_target=17_908_478,
        priority="High",
        flexibility="Low",
        mapped_assets=[
            {
                "asset_id":"asset-1",
                "asset_name":"Corpus",
                "allocation_type":"currency",
                "allocation_value":10_000_000,
                "allocated_amount":10_000_000,
                "allocated_percentage":100,
                "expected_return":0.08,
                "projected_value":21_589_250,
            }
        ],
        projected_mapped_asset_value=10_000_000,
        funding_gap=7_908_478,
        funding_status="Shortfall",
        required_monthly_contribution=30_000,
    )


def test_bucketing_is_executable_and_balances_resources():
    result = TechniqueEngine().execute("tech-bucketing", _goal(), {"bucket_count": 3})
    assert result.status == "calculated"
    buckets = result.outputs["buckets"]
    assert len(buckets) == 3
    assert sum(item["mapped_resource_amount"] for item in buckets) == 10_000_000
    assert result.outputs["overall_funding_gap"] == 7_908_478


def test_glide_path_is_executable_and_de_risks():
    result = TechniqueEngine().execute(
        "tech-glide-path",
        _goal(),
        {"starting_growth_pct": 80, "ending_growth_pct": 20, "transition_years": 5},
    )
    assert result.status == "calculated"
    schedule = result.outputs["schedule"]
    assert schedule[0]["growth_allocation_pct"] == 80
    assert schedule[-1]["growth_allocation_pct"] == 20
    assert schedule[0]["safety_allocation_pct"] == 20
    assert schedule[-1]["safety_allocation_pct"] == 80


def test_unknown_technique_is_explicitly_not_implemented():
    result = TechniqueEngine().execute("tech-unknown", _goal())
    assert result.status == "not_implemented"
    assert result.warnings


def test_remaining_allocation_techniques_are_executable():
    engine = TechniqueEngine()
    ids = [
        "tech-laddering",
        "tech-cashflow-matching",
        "tech-asset-earmarking",
        "tech-contribution-escalation",
        "tech-goal-segmentation",
        "tech-barbell",
    ]
    results = engine.execute_many(ids, _goal())
    assert all(r.status == "calculated" for r in results)
    assert {r.technique_id for r in results} == set(ids)


def test_tax_sequencing_requires_explicit_tax_inputs():
    result = TechniqueEngine().execute("tech-tax-efficient-sequencing", _goal())
    assert result.status == "insufficient_inputs"


def test_tax_loss_harvesting_requires_explicit_tax_lots():
    result = TechniqueEngine().execute("tech-tax-loss-harvesting", _goal())
    assert result.status == "insufficient_inputs"


def test_tax_loss_harvesting_calculates_candidates_when_lots_exist():
    result = TechniqueEngine().execute(
        "tech-tax-loss-harvesting",
        _goal(),
        {
            "tax_lots": [
                {"lot_id": "lot-1", "cost_basis": 100000, "current_value": 90000},
                {"lot_id": "lot-2", "cost_basis": 50000, "current_value": 55000},
            ]
        },
    )
    assert result.status == "calculated"
    assert result.outputs["total_unrealised_loss"] == 10000
    assert len(result.outputs["harvest_candidates"]) == 1
