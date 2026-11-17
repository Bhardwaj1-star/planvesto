"""
domain/features/strategy_builder/comparison.py
Chapter 11 — Step 7: Strategy Comparison Matrix (§11.7).

Presents a side-by-side comparison of Self Money vs Self Money + Financing
under identical goal requirements, dates, and return assumptions.
Highlights trade-offs without auto-selecting a path; the investor retains full authority.
"""

from dataclasses import dataclass
from typing import List
from app.domain.shared.value_objects import Money
from app.domain.features.strategy_builder.funding_paths import (
    SelfMoneyPathResult,
    FinancingPathResult,
)


@dataclass(frozen=True)
class StrategyComparisonMatrix:
    """Side-by-side comparison matrix of both funding paths (§11.7)."""
    goal_id: str
    self_money_path: SelfMoneyPathResult
    financing_path: FinancingPathResult

    # Comparative trade-offs (§11.7)
    own_money_outflow_difference: Money  # Self Money total outflow vs Financing total outflow
    financing_cost_drag: Money           # Extra borrowing cost incurred under financing path
    remaining_corpus_difference: Money   # Difference in wealth left over after goal completion
    trade_off_summary: str
    investor_decision_prompt: str


def compare_funding_paths(
    self_money_path: SelfMoneyPathResult,
    financing_path: FinancingPathResult,
) -> StrategyComparisonMatrix:
    """
    Step 7 & §11.7: Compare Self Money vs Self Money + Financing on identical goal terms.
    Presents trade-offs and decision consequences without auto-selecting.
    """
    # 1. Own Money Outflow Difference:
    # Under financing: down payment + all repayments (principal + interest).
    # Under self money: initial assets + ongoing SIP contributions.
    outflow_diff = self_money_path.total_own_money_contributed - financing_path.total_own_money_outflow

    # 2. Financing Cost Drag
    cost_drag = financing_path.total_interest_cost

    # 3. Remaining Corpus Difference after goal completion
    remaining_corpus_diff = self_money_path.remaining_corpus_after_goal - financing_path.remaining_corpus_after_goal

    trade_off_parts: List[str] = [
        f"• Own Capital Outflow: Self Money requires {self_money_path.total_own_money_contributed.amount} in accumulated savings, "
        f"whereas Financing requires {financing_path.total_own_money_outflow.amount} total cash outflow (including {financing_path.total_interest_cost.amount} loan interest).",
        f"• Compounding & Residual Wealth: Self Money path leaves {self_money_path.remaining_corpus_after_goal.amount} in remaining investment corpus, "
        f"whereas Financing leaves {financing_path.remaining_corpus_after_goal.amount} residual balance.",
        f"• Debt Obligation: Financing commits {financing_path.monthly_emi.amount}/month in debt service for {financing_path.loan_tenure_months} months.",
    ]

    trade_off_summary = "\n".join(trade_off_parts)

    investor_prompt = (
        "Trade-off Decision: Does preserving near-term liquidity with a loan justify paying "
        f"{financing_path.total_interest_cost.amount} in financing cost and committing {financing_path.monthly_emi.amount}/month in EMI? "
        "The investor retains full authority to select the preferred route."
    )

    return StrategyComparisonMatrix(
        goal_id=self_money_path.goal_id,
        self_money_path=self_money_path,
        financing_path=financing_path,
        own_money_outflow_difference=outflow_diff,
        financing_cost_drag=cost_drag,
        remaining_corpus_difference=remaining_corpus_diff,
        trade_off_summary=trade_off_summary,
        investor_decision_prompt=investor_prompt,
    )
