from datetime import date
from typing import Any

from engines.calculation.engine import round_money
from engines.goal.asset_projection import calculate_asset_projection, get_default_expected_return
from engines.goal.funding_gap import (
    calculate_funding_gap,
    calculate_funding_return_assumption,
    calculate_required_monthly_contribution,
)
from engines.goal.target_calculator import DEFAULT_INFLATION_RATE, calculate_duration, calculate_future_target, calculate_retirement_corpus
from rules.goals import canonical_goal_name, canonical_goal_type
from models.defined_goal import DefinedGoal, DefinedGoalAssetMapping
from schemas.goals import GoalInput


class GoalEngine:
    """Generic target-date goal engine shared by every goal type."""

    def calculate_defined_goal(
        self,
        goal_input: GoalInput,
        assets_lookup: dict[str, dict[str, Any]],
        version: int = 1,
        is_latest: bool = True,
        reference_date: date | None = None,
    ) -> DefinedGoal:
        canonical_type = canonical_goal_type(goal_input.goal_type)
        canonical_name = canonical_goal_name(canonical_type, goal_input.goal_name)

        inflation_rate = (
            goal_input.inflation_rate
            if goal_input.inflation_rate is not None
            else DEFAULT_INFLATION_RATE
        )
        inflation_source = "custom" if goal_input.inflation_rate is not None else "default"

        duration_years = calculate_duration(
            target_month=goal_input.target_month,
            target_year=goal_input.target_year,
            reference_date=reference_date,
        )
        today_cost = float(goal_input.today_cost)

        mapped_assets: list[DefinedGoalAssetMapping] = []
        total_projected_assets = 0.0

        for mapping_in in goal_input.asset_mappings:
            asset_info = assets_lookup.get(mapping_in.asset_id)
            if not asset_info:
                raise ValueError(f"Asset {mapping_in.asset_id} is not available in the planning unit")
            asset_name = asset_info.get("asset_name")
            if not asset_name:
                raise ValueError(f"Asset {mapping_in.asset_id} has no asset name")

            current_value = float(asset_info.get("current_value", 0.0))
            expected_ret = (
                mapping_in.expected_return
                if mapping_in.expected_return is not None
                else get_default_expected_return(asset_name)
            )
            return_freq = mapping_in.return_frequency or "annual"

            allocated_amt, allocated_pct, projected_val = calculate_asset_projection(
                current_asset_value=current_value,
                allocation_type=mapping_in.allocation_type,
                allocation_value=mapping_in.allocation_value,
                expected_return=expected_ret,
                return_frequency=return_freq,
                duration_years=duration_years,
            )
            total_projected_assets += projected_val

            mapped_assets.append(
                DefinedGoalAssetMapping(
                    asset_id=mapping_in.asset_id,
                    asset_name=asset_name,
                    allocation_type=mapping_in.allocation_type,
                    allocation_value=mapping_in.allocation_value,
                    allocated_amount=allocated_amt,
                    allocated_percentage=allocated_pct,
                    expected_return=expected_ret,
                    return_frequency=return_freq,
                    projected_value=projected_val,
                )
            )

        total_projected_assets = round_money(total_projected_assets)
        funding_return = calculate_funding_return_assumption(
            [m.model_dump() for m in mapped_assets]
        )

        dynamic_details = goal_input.dynamic_details or {}
        if canonical_type == "retirement":
            current_age_raw = dynamic_details.get("currentAge", dynamic_details.get("current_age"))
            life_expectancy_raw = dynamic_details.get("lifeExpectancy", dynamic_details.get("life_expectancy"))
            if current_age_raw is None or life_expectancy_raw is None:
                raise ValueError(
                    "Retirement planning requires currentAge and lifeExpectancy in dynamic_details"
                )
            current_age = float(current_age_raw)
            life_expectancy = float(life_expectancy_raw)
            retirement_return = 0.08
            retirement_age, retirement_years, future_target = calculate_retirement_corpus(
                current_monthly_expense=today_cost / 12.0,
                inflation_rate=inflation_rate,
                years_to_retirement=duration_years,
                current_age=current_age,
                life_expectancy=life_expectancy,
                retirement_return=retirement_return,
            )
            funding_return = retirement_return
        else:
            future_target = calculate_future_target(
                today_cost=today_cost,
                inflation_rate=inflation_rate,
                duration_years=duration_years,
            )

        funding_gap, funding_status = calculate_funding_gap(
            future_target=future_target,
            projected_mapped_asset_value=total_projected_assets,
        )
        required_monthly = calculate_required_monthly_contribution(
            funding_gap=funding_gap,
            annual_return=funding_return,
            duration_years=duration_years,
        )

        metadata = {
            "asset_count": len(mapped_assets),
            "calculation_source": "GoalEngine",
            "funding_model": "retirement_corpus" if canonical_goal_type(goal_input.goal_type) == "retirement" else "target_gap_plus_monthly_contribution",
            "funding_return_assumption": funding_return,
            "required_monthly_contribution": required_monthly,
            "dynamic_details": dynamic_details,
        }
        if canonical_type == "retirement":
            metadata["retirement_age"] = retirement_age
            metadata["retirement_years"] = retirement_years

        return DefinedGoal(
            goal_id=goal_input.goal_id or "",
            planning_unit_id=goal_input.planning_unit_id,
            investor_id=goal_input.investor_id,
            version=version,
            is_latest=is_latest,
            goal_type=canonical_type,
            goal_name=canonical_name,
            today_cost=today_cost,
            inflation_rate=inflation_rate,
            inflation_source=inflation_source,
            target_month=goal_input.target_month,
            target_year=goal_input.target_year,
            duration_years=duration_years,
            future_target=future_target,
            priority=goal_input.priority,
            flexibility=goal_input.flexibility,
            status=goal_input.status,
            mapped_assets=mapped_assets,
            projected_mapped_asset_value=total_projected_assets,
            funding_gap=funding_gap,
            funding_status=funding_status,
            required_monthly_contribution=required_monthly,
            funding_return_assumption=funding_return,
            version_metadata=metadata,
        )
