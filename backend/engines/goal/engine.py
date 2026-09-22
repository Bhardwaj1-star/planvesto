from datetime import date
from typing import Any
from engines.calculation.engine import round_money
from engines.goal.asset_projection import (
    calculate_asset_projection,
    get_default_expected_return,
)
from engines.goal.funding_gap import (
    calculate_funding_gap,
    calculate_funding_return_assumption,
    calculate_required_monthly_contribution,
)
from engines.goal.target_calculator import (
    DEFAULT_INFLATION_RATE,
    calculate_duration,
    calculate_future_target,
)
from models.defined_goal import DefinedGoal, DefinedGoalAssetMapping
from schemas.goals import GoalInput


class GoalEngine:
    def calculate_defined_goal(
        self,
        goal_input: GoalInput,
        assets_lookup: dict[str, dict[str, Any]],
        version: int = 1,
        is_latest: bool = True,
        reference_date: date | None = None,
    ) -> DefinedGoal:
        if goal_input.inflation_rate is not None:
            inflation_rate = goal_input.inflation_rate
            inflation_source = "custom"
        else:
            inflation_rate = DEFAULT_INFLATION_RATE
            inflation_source = "default"

        duration_years = calculate_duration(
            target_month=goal_input.target_month,
            target_year=goal_input.target_year,
            reference_date=reference_date,
        )

        today_cost = float(goal_input.today_cost)
        future_target = calculate_future_target(
            today_cost=today_cost,
            inflation_rate=inflation_rate,
            duration_years=duration_years,
        )

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
        funding_gap, funding_status = calculate_funding_gap(
            future_target=future_target,
            projected_mapped_asset_value=total_projected_assets,
        )

        funding_return = calculate_funding_return_assumption(
            [m.model_dump() for m in mapped_assets]
        )
        required_monthly = calculate_required_monthly_contribution(
            funding_gap=funding_gap,
            annual_return=funding_return,
            duration_years=duration_years,
        )

        metadata = {
            "asset_count": len(mapped_assets),
            "calculation_source": "GoalEngine",
            "funding_model": "target_gap_plus_monthly_contribution",
            "funding_return_assumption": funding_return,
            "required_monthly_contribution": required_monthly,
        }

        return DefinedGoal(
            goal_id=goal_input.goal_id or "",
            planning_unit_id=goal_input.planning_unit_id,
            investor_id=goal_input.investor_id,
            version=version,
            is_latest=is_latest,
            goal_type=goal_input.goal_type,
            goal_name=goal_input.goal_name,
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
