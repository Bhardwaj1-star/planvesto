"""Authoritative eligibility business rules for Strategy Builder."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Tuple
from models.strategy import StrategyDefinition
from models.defined_goal import DefinedGoal as GoalSnapshot
from rules.eligibility import ELIGIBILITY_FITS, EligibilityStatus
from rules.goals import GOAL_TYPE_ALIASES

# Re-exported for backwards compatibility with tests and callers
EligibilityStatus = EligibilityStatus
ELIGIBILITY_FITS = ELIGIBILITY_FITS

@dataclass(frozen=True)
class EligibilityFitResult:
    fit: str
    status: EligibilityStatus
    reason: str = ""
    required_changes: tuple[str, ...] = ()
    data: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class EligibilityAssessment:
    results: tuple[EligibilityFitResult, ...]
    @property
    def status(self):
        statuses = {r.status for r in self.results}
        return EligibilityStatus.FAIL if EligibilityStatus.FAIL in statuses else EligibilityStatus.CONDITIONAL if EligibilityStatus.CONDITIONAL in statuses else EligibilityStatus.PASS
    @property
    def failed_fits(self): return tuple(r for r in self.results if r.status == EligibilityStatus.FAIL)
    @property
    def conditional_fits(self): return tuple(r for r in self.results if r.status == EligibilityStatus.CONDITIONAL)
    @property
    def required_changes(self): return tuple(c for r in self.results for c in r.required_changes)
    @property
    def eligible_for_recommendation(self): return self.status != EligibilityStatus.FAIL

def _num(context: dict[str, Any], key: str, default=None):
    value = context.get(key, default)
    if isinstance(value, dict): value = value.get("value", default)
    try: return float(value) if value is not None else default
    except (TypeError, ValueError): return default

def _monthly(context: dict[str, Any], monthly_key: str, annual_key: str):
    value = _num(context, monthly_key)
    if value is not None: return value
    value = _num(context, annual_key)
    return value / 12 if value is not None else None

def _fit(status, fit, reason, changes=(), data=None):
    return EligibilityFitResult(fit, status, reason, tuple(changes), data or {})

def _goal_gate(strategy, goal, context):
    reasons=[]
    raw=(getattr(goal,"goal_type",getattr(goal,"type","")) or "").strip().lower()
    canonical=GOAL_TYPE_ALIASES.get(raw, raw)
    duration=float(getattr(goal,"duration_years",getattr(goal,"horizon_years",0)) or 0)
    types=[GOAL_TYPE_ALIASES.get(t.strip().lower(),t.strip().lower()) for t in getattr(strategy,"applicable_goal_types",[])]
    if types and canonical and canonical not in types and "other" not in types: reasons.append(f"Goal type '{raw}' not allowed")
    for c in getattr(strategy,"constraints",[]) or []:
        try:
            if c.startswith("horizon<=") and duration > float(c.split("<=",1)[1]): reasons.append(f"Goal horizon {duration:g} exceeds strategy limit")
            elif c.startswith("horizon>=") and duration < float(c.split(">=",1)[1]): reasons.append(f"Goal horizon {duration:g} is below strategy minimum")
            elif c.startswith("funding_gap<=") and float(getattr(goal,"funding_gap",0) or 0) > float(c.split("<=",1)[1]): reasons.append("Funding gap exceeds strategy limit")
            elif c.startswith("funding_gap>=") and float(getattr(goal,"funding_gap",0) or 0) < float(c.split(">=",1)[1]): reasons.append("Funding gap is below strategy minimum")
        except ValueError: pass
    return canonical, duration, reasons

def evaluate_eligibility_fits(strategy: StrategyDefinition, *, goal: GoalSnapshot | None = None, financial_context: dict[str, Any] | None = None) -> EligibilityAssessment:
    context=dict(financial_context or {})
    results=[]
    required=_num(context,"strategy_required_monthly_contribution")
    surplus=_monthly(context,"investable_surplus_monthly","investable_surplus_annual")
    if surplus is None:
        income=_monthly(context,"take_home_income_monthly","take_home_income_annual")
        expenses=_monthly(context,"expenses_monthly","expenses_annual")
        emi=_monthly(context,"emi_burden_monthly","emi_burden_annual") or 0
        surplus=(income-expenses-emi) if income is not None and expenses is not None else None
    if surplus is None or required is None:
        results.append(_fit(EligibilityStatus.CONDITIONAL,"cashflow_fit","Cash-flow evidence is incomplete",["Provide monthly surplus and strategy contribution"]))
    elif surplus <= 0:
        results.append(_fit(EligibilityStatus.FAIL,"cashflow_fit",f"Available surplus is ₹{surplus:,.2f}", ["Create positive monthly surplus"], {"surplus":surplus}))
    elif required <= surplus:
        results.append(_fit(EligibilityStatus.PASS,"cashflow_fit",f"Required ₹{required:,.2f}/month fits ₹{surplus:,.2f} available surplus",data={"surplus":surplus,"required":required}))
    else:
        gap=required-surplus
        results.append(_fit(EligibilityStatus.CONDITIONAL,"cashflow_fit",f"Monthly shortfall is ₹{gap:,.2f}",[f"Increase monthly available surplus by ₹{gap:,.2f}"],{"surplus":surplus,"required":required,"shortfall":gap}))

    liquid=_num(context,"liquid_assets")
    reserve=_num(context,"required_liquidity")
    if liquid is None or reserve is None: results.append(_fit(EligibilityStatus.CONDITIONAL,"liquidity_fit","Liquidity requirement/evidence is incomplete",["Provide liquid assets and required safety reserve"]))
    elif liquid >= reserve: results.append(_fit(EligibilityStatus.PASS,"liquidity_fit",f"₹{liquid:,.2f} liquid resources cover ₹{reserve:,.2f} required reserve",data={"liquid":liquid,"required":reserve}))
    else: results.append(_fit(EligibilityStatus.CONDITIONAL,"liquidity_fit",f"Liquidity gap is ₹{reserve-liquid:,.2f}",[f"Maintain additional liquidity of ₹{reserve-liquid:,.2f}"],{"gap":reserve-liquid}))

    emi=_monthly(context,"emi_burden_monthly","emi_burden_annual")
    if emi is None: results.append(_fit(EligibilityStatus.CONDITIONAL,"debt_fit","Mandatory debt payment evidence is incomplete",["Provide mandatory monthly debt payments"]))
    elif surplus is not None and surplus >= 0: results.append(_fit(EligibilityStatus.PASS,"debt_fit","Mandatory monthly debt obligations remain serviceable"))
    else: results.append(_fit(EligibilityStatus.FAIL,"debt_fit","Mandatory debt obligations cannot be supported by current cash flow",["Restore debt-service capacity"]))

    required_asset=_num(context,"strategy_required_asset_resource")
    available_asset=_num(context,"available_asset_resource")
    if required_asset is None or available_asset is None: results.append(_fit(EligibilityStatus.CONDITIONAL,"asset_resource_fit","Required/available strategy resources are not fully evidenced",["Provide strategy resource requirement and available resources"]))
    elif available_asset >= required_asset: results.append(_fit(EligibilityStatus.PASS,"asset_resource_fit","Required resources are available"))
    else: results.append(_fit(EligibilityStatus.CONDITIONAL,"asset_resource_fit",f"Resource gap is ₹{required_asset-available_asset:,.2f}",[f"Create/reallocate ₹{required_asset-available_asset:,.2f} of required resources"]))

    risk_required=_num(context,"strategy_required_risk_capacity")
    risk_capacity=_num(context,"risk_capacity")
    if risk_required is None or risk_capacity is None: results.append(_fit(EligibilityStatus.CONDITIONAL,"risk_capacity_fit","Risk-capacity evidence is incomplete",["Provide strategy risk requirement and investor risk capacity"]))
    elif risk_required <= risk_capacity: results.append(_fit(EligibilityStatus.PASS,"risk_capacity_fit","Strategy risk requirement is within investor risk capacity"))
    elif _num(context,"de_risked_strategy_risk") is not None and _num(context,"de_risked_strategy_risk") <= risk_capacity: results.append(_fit(EligibilityStatus.CONDITIONAL,"risk_capacity_fit","Strategy requires de-risking",["Use the defined de-risked implementation"]))
    else: results.append(_fit(EligibilityStatus.FAIL,"risk_capacity_fit","Strategy risk requirement exceeds investor risk capacity"))

    canonical,duration,goal_reasons=_goal_gate(strategy,goal,context) if goal else ("",0,[])
    results.append(_fit(EligibilityStatus.FAIL if goal_reasons else EligibilityStatus.PASS,"goal_constraint_fit","Goal type, horizon and mandatory constraints are satisfied" if not goal_reasons else "; ".join(goal_reasons)))

    conflict=context.get("higher_priority_goal_conflict")
    if conflict is None: results.append(_fit(EligibilityStatus.CONDITIONAL,"multi_goal_conflict_fit","Higher-priority goal impact is not evidenced",["Evaluate impact on higher-priority goals"]))
    elif conflict is True: results.append(_fit(EligibilityStatus.FAIL,"multi_goal_conflict_fit","Higher-priority goal is materially compromised"))
    elif conflict == "conditional": results.append(_fit(EligibilityStatus.CONDITIONAL,"multi_goal_conflict_fit","Resource reallocation is required",["Adjust allocation without materially compromising higher-priority goals"]))
    else: results.append(_fit(EligibilityStatus.PASS,"multi_goal_conflict_fit","No higher-priority goal is compromised"))

    impl=context.get("implementation_status")
    if impl is None: results.append(_fit(EligibilityStatus.CONDITIONAL,"implementation_fit","Implementation evidence is incomplete",["Confirm required actions/resources are implementable"]))
    elif impl is True or str(impl).lower()=="pass": results.append(_fit(EligibilityStatus.PASS,"implementation_fit","Strategy is practically implementable"))
    elif str(impl).lower()=="conditional": results.append(_fit(EligibilityStatus.CONDITIONAL,"implementation_fit","Implementation requires defined changes",["Complete the defined implementation changes"]))
    else: results.append(_fit(EligibilityStatus.FAIL,"implementation_fit","Strategy cannot be practically implemented"))
    return EligibilityAssessment(tuple(results))

def evaluate_eligibility(strategy: StrategyDefinition, goal: GoalSnapshot | None, state: Any | None = None, financial_context: dict[str, Any] | None = None, rule_assessment: Any | None = None) -> Tuple[bool,List[str]]:
    context=dict(financial_context or {})
    if goal is None: return True,[]
    _,_,goal_reasons=_goal_gate(strategy,goal,context)
    reasons=list(goal_reasons)
    if rule_assessment is not None:
        for r in getattr(rule_assessment,"hard_constraints",()):
            if not r.passed: reasons.append(r.message)
    return not reasons,reasons
