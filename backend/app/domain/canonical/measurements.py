"""
Chapter 05 — Canonical Measurements, Formulas & Assumptions
Canonical Measurement Metadata (§2)

Non-negotiable invariants:
1. Chapter 05 is the canonical owner of measurement definitions, formulas, units, assumptions and methods.
2. Shared rules/calculations have one canonical implementation; do not duplicate formulas per feature.
3. This file contains metadata definitions only; formula implementations live in domain/shared/calculations/.
4. Missing, stale, conflicting, invalid or insufficient evidence remains visible; never invent defaults.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class CanonicalMeasurementId(str, Enum):
    # Group A: Basic Financial Position
    NET_WORTH = "metric_net_worth"

    # Group B: Monthly Cash Flow
    MONTHLY_SURPLUS = "metric_monthly_surplus"
    SAVINGS_RATE = "metric_savings_rate"
    MONTHLY_VARIANCE = "metric_monthly_variance"

    # Group C: Financial Health, Assets & Debt
    DEBT_TO_INCOME_RATIO = "metric_debt_to_income_ratio"
    LEVERAGE_RATIO = "metric_leverage_ratio"
    LIQUID_ASSET_RATIO = "metric_liquid_asset_ratio"
    FINANCIAL_ASSET_RATIO = "metric_financial_asset_ratio"
    PORTFOLIO_CONCENTRATION = "metric_portfolio_concentration"
    WEIGHTED_DEBT_RATE = "metric_weighted_debt_rate"
    INVESTMENT_DEBT_SPREAD = "metric_investment_debt_spread"

    # Group D: Goal Funding & Feasibility
    FUTURE_GOAL_TARGET = "metric_future_goal_target"
    PROJECTED_ASSET_VALUE = "metric_projected_asset_value"
    GOAL_FUNDING_GAP = "metric_goal_funding_gap"
    GOAL_FUNDING_RATIO = "metric_goal_funding_ratio"
    FUTURE_FUNDING_RATIO = "metric_future_funding_ratio"
    REQUIRED_MONTHLY_CONTRIBUTION = "metric_required_monthly_contribution"
    MONTHLY_SIP_SURPLUS_GAP = "metric_monthly_sip_surplus_gap"
    REQUIRED_SURPLUS_INCREASE = "metric_required_surplus_increase"
    RISK_REQUIRED_RETURN = "metric_risk_required_return"


class MeasurementUnit(str, Enum):
    CURRENCY = "INR"
    CURRENCY_PER_MONTH = "INR/month"
    PERCENTAGE = "%"
    PERCENTAGE_PER_YEAR = "%/year"
    PERCENTAGE_POINTS = "percentage_points"
    YEARS = "years"


@dataclass(frozen=True)
class MeasurementMetadata:
    id: CanonicalMeasurementId
    canonical_name: str
    definition: str
    inputs_required: List[str]
    unit: MeasurementUnit
    assumptions_limits: str


MEASUREMENT_CATALOGUE: Dict[CanonicalMeasurementId, MeasurementMetadata] = {
    CanonicalMeasurementId.NET_WORTH: MeasurementMetadata(
        id=CanonicalMeasurementId.NET_WORTH,
        canonical_name="Net Worth",
        definition="Net financial position at the stated valuation date.",
        inputs_required=["Total Assets", "Total Liabilities"],
        unit=MeasurementUnit.CURRENCY,
        assumptions_limits="Requires consistent valuation basis and valid asset/liability inputs.",
    ),
    CanonicalMeasurementId.MONTHLY_SURPLUS: MeasurementMetadata(
        id=CanonicalMeasurementId.MONTHLY_SURPLUS,
        canonical_name="Available Monthly Surplus",
        definition="Amount remaining from actual net monthly income after deducting actual monthly expenses and actual monthly savings/investments for the same calendar month.",
        inputs_required=["Actual Net Monthly Income", "Actual Monthly Expenses", "Actual Monthly Savings and Investments"],
        unit=MeasurementUnit.CURRENCY_PER_MONTH,
        assumptions_limits="Formula: Net Income − Expenses − Savings. Uses same calendar month. Full EMI counted once under Expenses. Transfers excluded.",
    ),
    CanonicalMeasurementId.SAVINGS_RATE: MeasurementMetadata(
        id=CanonicalMeasurementId.SAVINGS_RATE,
        canonical_name="Savings Ratio",
        definition="Actual monthly savings and investments as a percentage of actual net monthly income for the same calendar month.",
        inputs_required=["Actual Monthly Savings and Investments", "Actual Net Monthly Income"],
        unit=MeasurementUnit.PERCENTAGE,
        assumptions_limits="Calculate only when net monthly income is positive. Transfers excluded.",
    ),
    CanonicalMeasurementId.MONTHLY_VARIANCE: MeasurementMetadata(
        id=CanonicalMeasurementId.MONTHLY_VARIANCE,
        canonical_name="Monthly Spending Variance",
        definition="Difference between actual and budgeted spending for the same category and calendar month.",
        inputs_required=["Actual monthly spending by category", "Budgeted monthly spending limit for category"],
        unit=MeasurementUnit.CURRENCY_PER_MONTH,
        assumptions_limits="Actual − Budget. Positive = over budget; negative = under budget. Zero budget is valid.",
    ),
    CanonicalMeasurementId.DEBT_TO_INCOME_RATIO: MeasurementMetadata(
        id=CanonicalMeasurementId.DEBT_TO_INCOME_RATIO,
        canonical_name="Debt-to-Income Ratio",
        definition="Share of gross monthly income committed to monthly debt payments.",
        inputs_required=["Monthly Debt Payments", "Gross Monthly Income"],
        unit=MeasurementUnit.PERCENTAGE,
        assumptions_limits="Monthly Debt Payments ÷ Gross Monthly Income × 100. Requires positive gross income.",
    ),
    CanonicalMeasurementId.LEVERAGE_RATIO: MeasurementMetadata(
        id=CanonicalMeasurementId.LEVERAGE_RATIO,
        canonical_name="Leverage Ratio",
        definition="Liabilities relative to total assets, expressed as a percentage.",
        inputs_required=["Total Liabilities", "Total Assets"],
        unit=MeasurementUnit.PERCENTAGE,
        assumptions_limits="Total Liabilities ÷ Total Assets × 100. Requires valid total asset value > 0.",
    ),
    CanonicalMeasurementId.LIQUID_ASSET_RATIO: MeasurementMetadata(
        id=CanonicalMeasurementId.LIQUID_ASSET_RATIO,
        canonical_name="Liquid Asset Ratio",
        definition="Share of total assets classified as liquid under the approved eligibility mapping.",
        inputs_required=["Liquid Assets", "Total Assets"],
        unit=MeasurementUnit.PERCENTAGE,
        assumptions_limits="Liquid Assets ÷ Total Assets × 100. Requires explicit liquidity classification.",
    ),
    CanonicalMeasurementId.FINANCIAL_ASSET_RATIO: MeasurementMetadata(
        id=CanonicalMeasurementId.FINANCIAL_ASSET_RATIO,
        canonical_name="Financial Asset Ratio",
        definition="Share of total assets classified as financial assets under approved category mapping.",
        inputs_required=["Financial Assets", "Total Assets"],
        unit=MeasurementUnit.PERCENTAGE,
        assumptions_limits="Financial Assets ÷ Total Assets × 100. Physical assets excluded.",
    ),
    CanonicalMeasurementId.PORTFOLIO_CONCENTRATION: MeasurementMetadata(
        id=CanonicalMeasurementId.PORTFOLIO_CONCENTRATION,
        canonical_name="Portfolio Concentration",
        definition="Share of total assets represented by the largest single asset.",
        inputs_required=["Largest Single Asset Value", "Total Asset Value"],
        unit=MeasurementUnit.PERCENTAGE,
        assumptions_limits="Largest Asset ÷ Total Assets × 100.",
    ),
    CanonicalMeasurementId.WEIGHTED_DEBT_RATE: MeasurementMetadata(
        id=CanonicalMeasurementId.WEIGHTED_DEBT_RATE,
        canonical_name="Weighted Debt Rate",
        definition="Outstanding-principal-weighted annual interest rate across all included active debt accounts.",
        inputs_required=["Current Outstanding Principal per debt", "Annual Interest Rate per debt"],
        unit=MeasurementUnit.PERCENTAGE_PER_YEAR,
        assumptions_limits="Σ(Principalᵢ × Rateᵢ) ÷ Σ(Principalᵢ). Never use original sanctioned amount. Contractual 0% included; missing rate cannot be treated as 0%.",
    ),
    CanonicalMeasurementId.INVESTMENT_DEBT_SPREAD: MeasurementMetadata(
        id=CanonicalMeasurementId.INVESTMENT_DEBT_SPREAD,
        canonical_name="Investment–Debt Spread",
        definition="Difference, in percentage points, between annualised portfolio return and weighted debt rate.",
        inputs_required=["Annualised Portfolio Return", "Weighted Debt Rate"],
        unit=MeasurementUnit.PERCENTAGE_POINTS,
        assumptions_limits="Portfolio Return − Weighted Debt Rate.",
    ),
    CanonicalMeasurementId.FUTURE_GOAL_TARGET: MeasurementMetadata(
        id=CanonicalMeasurementId.FUTURE_GOAL_TARGET,
        canonical_name="Future Goal Target",
        definition="Estimated goal cost at the future goal date, using applicable inflation assumption.",
        inputs_required=["Today's Goal Cost", "Applicable Inflation Rate", "Duration in Years"],
        unit=MeasurementUnit.CURRENCY,
        assumptions_limits="Cost × (1 + inflation)^years. Requires goal-specific approved inflation.",
    ),
    CanonicalMeasurementId.PROJECTED_ASSET_VALUE: MeasurementMetadata(
        id=CanonicalMeasurementId.PROJECTED_ASSET_VALUE,
        canonical_name="Projected Asset Value",
        definition="Estimated future value of an allocated asset under stated return and period assumptions.",
        inputs_required=["Current Allocated Amount", "Periodic Return", "Number of Periods"],
        unit=MeasurementUnit.CURRENCY,
        assumptions_limits="Allocated Amount × (1 + periodic_return)^periods.",
    ),
    CanonicalMeasurementId.GOAL_FUNDING_GAP: MeasurementMetadata(
        id=CanonicalMeasurementId.GOAL_FUNDING_GAP,
        canonical_name="Goal Funding Gap",
        definition="Amount by which the future goal target exceeds the projected value of eligible funding assigned to that goal.",
        inputs_required=["Future Goal Target", "Projected Value of Mapped Assets"],
        unit=MeasurementUnit.CURRENCY,
        assumptions_limits="Future Goal Target − Projected Value of Mapped Assets.",
    ),
    CanonicalMeasurementId.GOAL_FUNDING_RATIO: MeasurementMetadata(
        id=CanonicalMeasurementId.GOAL_FUNDING_RATIO,
        canonical_name="Goal Funding Ratio",
        definition="Current eligible funding allocated to a goal relative to the goal's current cost.",
        inputs_required=["Current Eligible Funding", "Current Goal Cost"],
        unit=MeasurementUnit.PERCENTAGE,
        assumptions_limits="Current Funding ÷ Current Cost × 100. Today's cost basis.",
    ),
    CanonicalMeasurementId.FUTURE_FUNDING_RATIO: MeasurementMetadata(
        id=CanonicalMeasurementId.FUTURE_FUNDING_RATIO,
        canonical_name="Future Funding Ratio",
        definition="Projected goal funding relative to the goal's target value at future goal date.",
        inputs_required=["Projected Goal Funding", "Future Goal Target"],
        unit=MeasurementUnit.PERCENTAGE,
        assumptions_limits="Projected Funding ÷ Future Target × 100.",
    ),
    CanonicalMeasurementId.REQUIRED_MONTHLY_CONTRIBUTION: MeasurementMetadata(
        id=CanonicalMeasurementId.REQUIRED_MONTHLY_CONTRIBUTION,
        canonical_name="Required Monthly Contribution",
        definition="Monthly contribution needed to cover remaining future-value gap by goal date under approved return and timing assumptions.",
        inputs_required=["Remaining Future Funding Gap", "Monthly Periods Remaining", "Effective Annual Return"],
        unit=MeasurementUnit.CURRENCY_PER_MONTH,
        assumptions_limits="Ordinary annuity (month-end): G × r_m ÷ ((1 + r_m)^n − 1), where r_m = (1 + r_a)^(1/12) − 1. If r_m = 0: G ÷ n.",
    ),
    CanonicalMeasurementId.MONTHLY_SIP_SURPLUS_GAP: MeasurementMetadata(
        id=CanonicalMeasurementId.MONTHLY_SIP_SURPLUS_GAP,
        canonical_name="Monthly SIP / Surplus Gap",
        definition="Additional monthly contribution amount by which Required SIP exceeds Available Monthly Surplus.",
        inputs_required=["Additional Required SIP", "Available Monthly Surplus"],
        unit=MeasurementUnit.CURRENCY_PER_MONTH,
        assumptions_limits="Required SIP − Available Monthly Surplus. Non-positive gap means no shortfall.",
    ),
    CanonicalMeasurementId.REQUIRED_SURPLUS_INCREASE: MeasurementMetadata(
        id=CanonicalMeasurementId.REQUIRED_SURPLUS_INCREASE,
        canonical_name="Required Surplus Increase",
        definition="Percentage increase over current positive Available Monthly Surplus required to close Monthly SIP / Surplus Gap.",
        inputs_required=["Monthly SIP / Surplus Gap", "Available Monthly Surplus"],
        unit=MeasurementUnit.PERCENTAGE,
        assumptions_limits="(Gap ÷ Surplus) × 100. Only valid when Surplus > 0.",
    ),
    CanonicalMeasurementId.RISK_REQUIRED_RETURN: MeasurementMetadata(
        id=CanonicalMeasurementId.RISK_REQUIRED_RETURN,
        canonical_name="Risk Required Return — individual-goal measure",
        definition="Annualised return implied by current eligible goal funding, future goal target and time remaining.",
        inputs_required=["Future Goal Target", "Current Goal Funding", "Duration in Years"],
        unit=MeasurementUnit.PERCENTAGE_PER_YEAR,
        assumptions_limits="((Future Target ÷ Current Funding) ^ (1 ÷ Years) − 1) × 100. Single-goal metric only.",
    ),
}


def get_measurement_metadata(measurement_id: CanonicalMeasurementId | str) -> Optional[MeasurementMetadata]:
    """Retrieve metadata for canonical measurement."""
    if isinstance(measurement_id, str):
        try:
            measurement_id = CanonicalMeasurementId(measurement_id)
        except ValueError:
            return None
    return MEASUREMENT_CATALOGUE.get(measurement_id)
