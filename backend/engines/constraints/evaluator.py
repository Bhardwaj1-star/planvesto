from __future__ import annotations

from typing import Any
from engines.constraints.models import (
    ConstraintCheckResult,
    FinancialRatioResult,
    RatioConstraintAssessment,
)
from engines.orchestration.models import GoalEvaluationInput
from rules.constraints import (
    DEBT_TO_INCOME_CRITICAL_PERCENT,
    DEBT_TO_INCOME_HEALTHY_PERCENT,
    EMERGENCY_RESERVE_CRITICAL_MONTHS,
    EMERGENCY_RESERVE_HEALTHY_MONTHS,
    RULE_DEBT_BURDEN_EXCEEDED,
    RULE_EMERGENCY_RESERVE_CRITICAL,
    SAVINGS_RATIO_HEALTHY_PERCENT,
    WARN_DEBT_BURDEN_ATTENTION,
    WARN_EMERGENCY_RESERVE_ATTENTION,
    WARN_SAVINGS_RATE_DEFICIT,
)
from rules.financial_state import cash_flow_ratio, required_safety_reserve_months, savings_investment_rate
from rules.goals import DISCRETIONARY_GOAL_TYPES, ESSENTIAL_GOAL_TYPES, is_discretionary_goal, is_essential_goal
from rules.moneywheel import RULES, classify


class FinancialRatioConstraintEvaluator:
    """Evaluates financial ratios and checks goal priorities against approved business constraints."""

    DISCRETIONARY_GOAL_TYPES = DISCRETIONARY_GOAL_TYPES
    ESSENTIAL_GOAL_TYPES = ESSENTIAL_GOAL_TYPES

    @staticmethod
    def _extract_metric(state: dict[str, Any], key: str) -> float | None:
        val = state.get(key)
        if isinstance(val, dict):
            val = val.get("value")
        if hasattr(val, "value"):
            val = val.value
        if val is None:
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    def evaluate_ratios(self, financial_context: dict[str, Any]) -> list[FinancialRatioResult]:
        results: list[FinancialRatioResult] = []

        monthly_income = (
            self._extract_metric(financial_context, "monthly_income")
            or (self._extract_metric(financial_context, "annual_income") or 0.0) / 12.0
            or (self._extract_metric(financial_context, "income") or 0.0) / 12.0
        )
        monthly_expenses = (
            self._extract_metric(financial_context, "monthly_expenses")
            or (self._extract_metric(financial_context, "annual_expenses") or 0.0) / 12.0
            or (self._extract_metric(financial_context, "expenses") or 0.0) / 12.0
        )
        monthly_surplus = self._extract_metric(financial_context, "monthly_surplus")
        if monthly_surplus is None and monthly_income > 0:
            monthly_surplus = monthly_income - monthly_expenses

        total_assets = self._extract_metric(financial_context, "assets") or self._extract_metric(financial_context, "total_assets") or 0.0
        total_liabilities = self._extract_metric(financial_context, "liabilities") or self._extract_metric(financial_context, "total_liabilities") or 0.0
        monthly_emi = self._extract_metric(financial_context, "emi_burden_monthly") or self._extract_metric(financial_context, "monthly_debt_payments") or 0.0

        liquid_assets = self._extract_metric(financial_context, "liquid_assets")
        if liquid_assets is None:
            # Fallback to checking liquidity breakdown if present
            liq_breakdown = financial_context.get("liquidity_breakdown")
            if isinstance(liq_breakdown, dict):
                liquid_assets = float(liq_breakdown.get("liquid", 0.0))
            elif isinstance(liq_breakdown, list):
                liquid_assets = sum(float(item.get("amount", 0.0)) for item in liq_breakdown if str(item.get("category", "")).lower() == "liquid")
            else:
                # If unspecified, estimate conservative liquid pool from assets
                liquid_assets = 0.0

        # 1. Savings Ratio
        if monthly_income > 0 and monthly_surplus is not None:
            sav_val = round((monthly_surplus / monthly_income) * 100.0, 2)
            try:
                status = classify("savings_ratio", sav_val)
            except ValueError:
                status = "attention"
            results.append(FinancialRatioResult(
                ratio_key="savings_ratio",
                name="Savings Ratio",
                value=sav_val,
                unit="%",
                status=status,
                benchmark="Healthy >= 20.0%",
                evidence={"monthly_surplus": monthly_surplus, "monthly_income": monthly_income},
            ))

        # 2. Emergency Fund Coverage
        if monthly_expenses > 0:
            cov_val = round(liquid_assets / monthly_expenses, 2)
            try:
                status = classify("emergency_fund_coverage", cov_val)
            except ValueError:
                status = "critical"
            results.append(FinancialRatioResult(
                ratio_key="emergency_fund_coverage",
                name="Emergency Fund Coverage",
                value=cov_val,
                unit="months",
                status=status,
                benchmark="Healthy >= 6.0 months (Critical < 3.0 months)",
                evidence={"liquid_assets": liquid_assets, "monthly_expenses": monthly_expenses},
            ))

        # 3. Debt to Income Ratio
        if monthly_income > 0:
            dti_val = round((monthly_emi / monthly_income) * 100.0, 2)
            try:
                status = classify("debt_to_income_ratio", dti_val)
            except ValueError:
                status = "healthy"
            results.append(FinancialRatioResult(
                ratio_key="debt_to_income_ratio",
                name="Debt-to-Income Ratio",
                value=dti_val,
                unit="%",
                status=status,
                benchmark="Healthy <= 30.0% (Critical > 40.0%)",
                evidence={"monthly_emi": monthly_emi, "monthly_income": monthly_income},
            ))

        # 4. Leverage Ratio
        if total_assets > 0:
            lev_val = round((total_liabilities / total_assets) * 100.0, 2)
            try:
                status = classify("leverage_ratio", lev_val)
            except ValueError:
                status = "healthy"
            results.append(FinancialRatioResult(
                ratio_key="leverage_ratio",
                name="Leverage Ratio",
                value=lev_val,
                unit="%",
                status=status,
                benchmark="Healthy <= 30.0% (Critical > 50.0%)",
                evidence={"total_liabilities": total_liabilities, "total_assets": total_assets},
            ))

        return results

    def assess_constraints(
        self,
        goals: list[GoalEvaluationInput],
        financial_context: dict[str, Any],
    ) -> RatioConstraintAssessment:
        ratios = self.evaluate_ratios(financial_context)
        ratio_map = {r.ratio_key: r for r in ratios}

        constraints: list[ConstraintCheckResult] = []
        hard_constraints: list[ConstraintCheckResult] = []
        warnings: list[ConstraintCheckResult] = []
        suggested_overrides: dict[str, dict[str, Any]] = {}

        # 1. Emergency Fund Rule
        ef_ratio = ratio_map.get("emergency_fund_coverage")
        if ef_ratio:
            if ef_ratio.status == "critical":
                # Critical emergency reserve deficit: any discretionary goal prioritized above emergency is constrained
                has_emergency_goal = any(g.goal_type in ("emergency_fund", "emergency", "contingency") for g in goals)
                for g in goals:
                    is_discretionary = g.goal_type.lower() in self.DISCRETIONARY_GOAL_TYPES
                    if is_discretionary and g.client_priority in ("critical", "high"):
                        c = ConstraintCheckResult(
                            rule_id="RULE_EMERGENCY_RESERVE_CRITICAL",
                            goal_id=g.goal_id,
                            severity="hard",
                            passed=False,
                            message=(
                                f"Emergency fund coverage is critical ({ef_ratio.value} months < 3.0 threshold). "
                                f"Discretionary goal '{g.goal_name}' priority demoted to low until baseline reserve is established."
                            ),
                            suggested_override_priority="low",
                            override_reason=(
                                f"Discretionary allocation constrained because emergency fund coverage is in critical zone "
                                f"({ef_ratio.value} months vs minimum 3.0 required)."
                            ),
                            ratio_evidence=ef_ratio.evidence,
                        )
                        constraints.append(c)
                        hard_constraints.append(c)
                        suggested_overrides[g.goal_id] = {
                            "resolved_priority": "low",
                            "reason": c.override_reason,
                        }
            elif ef_ratio.status == "attention":
                warnings.append(ConstraintCheckResult(
                    rule_id="WARN_EMERGENCY_RESERVE_ATTENTION",
                    severity="warning",
                    passed=True,
                    message=f"Emergency fund coverage is below recommended buffer ({ef_ratio.value} months vs 6.0 recommended).",
                    ratio_evidence=ef_ratio.evidence,
                ))

        # 2. Debt Burden Rule
        dti_ratio = ratio_map.get("debt_to_income_ratio")
        if dti_ratio:
            if dti_ratio.status == "critical":
                for g in goals:
                    if g.goal_type.lower() in self.DISCRETIONARY_GOAL_TYPES and g.client_priority in ("critical", "high"):
                        c = ConstraintCheckResult(
                            rule_id="RULE_DEBT_BURDEN_EXCEEDED",
                            goal_id=g.goal_id,
                            severity="hard",
                            passed=False,
                            message=(
                                f"Debt-to-Income ratio ({dti_ratio.value}%) exceeds safe critical ceiling (40.0%). "
                                f"Discretionary goal '{g.goal_name}' priority reduced to preserve debt serviceability."
                            ),
                            suggested_override_priority="low",
                            override_reason=(
                                f"Debt-to-Income ratio exceeds critical threshold ({dti_ratio.value}% > 40.0%). "
                                f"System prioritized financial solvency over discretionary commitments."
                            ),
                            ratio_evidence=dti_ratio.evidence,
                        )
                        constraints.append(c)
                        hard_constraints.append(c)
                        suggested_overrides[g.goal_id] = {
                            "resolved_priority": "low",
                            "reason": c.override_reason,
                        }
            elif dti_ratio.status == "attention":
                warnings.append(ConstraintCheckResult(
                    rule_id="WARN_DEBT_BURDEN_ATTENTION",
                    severity="warning",
                    passed=True,
                    message=f"Debt-to-Income ratio ({dti_ratio.value}%) is in attention range (30-40%). Monitor leverage closely.",
                    ratio_evidence=dti_ratio.evidence,
                ))

        # 3. Savings Rate Rule
        sav_ratio = ratio_map.get("savings_ratio")
        if sav_ratio and sav_ratio.status in ("critical", "attention"):
            warnings.append(ConstraintCheckResult(
                rule_id="WARN_SAVINGS_RATE_DEFICIT",
                severity="warning",
                passed=True,
                message=f"Current savings rate ({sav_ratio.value}%) is constrained; may require expense reduction to meet multiple goals.",
                ratio_evidence=sav_ratio.evidence,
            ))

        return RatioConstraintAssessment(
            ratios=ratios,
            constraints=constraints,
            hard_constraints=hard_constraints,
            warnings=warnings,
            suggested_overrides=suggested_overrides,
        )
