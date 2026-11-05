from __future__ import annotations

from models.goal_basket import GoalBasket, GoalBasketSummary


class GoalBasketEngine:
    """Validates and summarizes a client-defined grouping of existing goals."""

    def build_summary(self, basket: GoalBasket, goals: list[dict]) -> GoalBasketSummary:
        if not basket.goal_ids:
            raise ValueError("A goal basket must contain at least one goal.")

        requested = set(basket.goal_ids)
        found = {str(g.get("goal_id")): g for g in goals if str(g.get("goal_id")) in requested}
        missing = requested - set(found)
        if missing:
            raise ValueError(f"Goals not found in planning unit: {', '.join(sorted(missing))}")

        ordered = [found[goal_id] for goal_id in basket.goal_ids]
        priorities = list(dict.fromkeys(str(g.get("priority")) for g in ordered if g.get("priority")))
        names = [str(g.get("goal_name") or g.get("goal_id")) for g in ordered]

        # Goals currently expose target_amount at the base-goal level. Funding
        # figures are read when available and otherwise safely default to zero.
        required = round(sum(float(g.get("required_monthly_contribution") or 0.0) for g in ordered), 2)
        gap = round(sum(float(g.get("funding_gap") or 0.0) for g in ordered), 2)

        return GoalBasketSummary(
            basket_id=basket.basket_id,
            planning_unit_id=basket.planning_unit_id,
            name=basket.name,
            goal_count=len(ordered),
            goal_ids=list(basket.goal_ids),
            total_required_monthly_contribution=required,
            total_funding_gap=gap,
            priorities=priorities,
            goal_names=names,
        )
