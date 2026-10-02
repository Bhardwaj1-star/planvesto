# Rule Engine Model: Policy, Ownership & Precedence

> **Document Status:** Authoritative Audit & Target Architecture  
> **Source Primary Reference:** `docs/domain-ontology/CODE_FIRST_DOMAIN_ONTOLOGY.md`  
> **Audit Scope:** `backend/rules/`, `backend/engines/rules/`, `backend/engines/constraints/`, `backend/engines/profile/`, `backend/engines/risk_profiler/`  
> **Core Principle:** Code-first truth. No business rules or architecture invented. Every finding backed by exact file, class, function, and line evidence.

---

## 1. Rule Engine Architecture Overview

The Planvesto rule architecture defines what conditions and thresholds are considered business truth across financial health, goals, constraints, suitability, and strategy selection.

```text
               RAW FINANCIAL STATE / CLIENT GOAL
                              │
                              ▼
            ┌────────────────────────────────────┐
            │       CANONICAL RULES LAYER        │
            │          (backend/rules/)          │
            ├────────────────────────────────────┤
            │  financial_state.py                │
            │  financial_metrics.py              │
            │  constraints.py                    │
            │  moneywheel.py                     │
            │  goals.py                          │
            │  eligibility.py                    │
            │  strategy_decision.py              │
            │  adaptation.py                     │
            │  action_plan.py                    │
            │  protection.py                     │
            │  risk_profiler.py                  │
            │  multi_goal.py                     │
            └────────────────────────────────────┘
                              │
               Evaluated By Mechanics Layer
                              │
                              ▼
            ┌────────────────────────────────────┐
            │        ENGINES EVALUATION          │
            │         (backend/engines/)         │
            ├────────────────────────────────────┤
            │  rules/engine.py (RuleEngine)      │
            │  constraints/evaluator.py          │
            │  moneywheel/engine.py              │
            │  strategy/eligibility.py           │
            │  strategy/decision.py              │
            │  allocation/engine.py              │
            │  orchestration/engine.py           │
            └────────────────────────────────────┘
                              │
                              ▼
            ┌────────────────────────────────────┐
            │        DECISION AUTHORITY          │
            │  DecisionRole Categorization       │
            ├────────────────────────────────────┤
            │  1. HARD_CONSTRAINT (Gate)         │
            │  2. ELIGIBILITY (8 Fits)           │
            │  3. RANKING_INPUT (Scoring)        │
            │  4. ARCHITECTURE_CONSTRAINT        │
            │  5. RECOMMENDATION_ONLY            │
            │  6. EXPLANATORY_EVIDENCE           │
            └────────────────────────────────────┘
```

---

## 2. Comprehensive Business Rules Inventory

The table below catalogs every business rule implemented in the backend, its exact source file, input/output types, ownership layer, precedence, and classification status (`CANONICAL | DUPLICATED | CONFLICTING | IMPLICIT | MISSING | PROVISIONAL`).

| Rule Identifier / Function | Source File & Location | Inputs | Outputs / Return Types | Decision Role / Precedence | Status | Description & Policy Thresholds |
|---|---|---|---|---|---|---|
| **`cash_flow_ratio`** | [`rules/financial_state.py:4-7`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/financial_state.py#L4-L7) | `expenses: float`, `income: float` | `float \| None` | Calculation Formula | `CANONICAL` | Computes `(expenses / income) * 100`. Returns `None` if `income == 0`. |
| **`savings_investment_rate`** | [`rules/financial_state.py:10-13`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/financial_state.py#L10-L13) | `investable_surplus: float`, `income: float` | `float \| None` | Calculation Formula | `CANONICAL` | Computes `(investable_surplus / income) * 100`. Returns `None` if `income == 0`. |
| **`required_safety_reserve_months`** | [`rules/financial_state.py:16-24`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/financial_state.py#L16-L24) | `cash_flow_ratio_value: float` | `int` (3, 6, 9, 12) | Rule Formula | `CANONICAL` | Tiered emergency reserve policy: `<=50%` ➔ 3 mo; `<=70%` ➔ 6 mo; `<=85%` ➔ 9 mo; `>85%` ➔ 12 mo. |
| **`RULE_EMERGENCY_RESERVE_CRITICAL`** | [`rules/constraints.py:6,13`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/constraints.py#L6) | `emergency_reserve_months: float` | `bool` (breached if `< 3.0`) | `HARD_CONSTRAINT` (Gate) | `DUPLICATED` | Threshold `3.0` months. Redundantly defined in `rules/moneywheel.py` (`emergency_fund_coverage.critical = (None, 3.0)`). |
| **`WARN_EMERGENCY_RESERVE_ATTENTION`** | [`rules/constraints.py:7,14`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/constraints.py#L7) | `emergency_reserve_months: float` | `bool` (warning if `< 6.0`) | `RANKING_INPUT` / Diagnostic | `DUPLICATED` | Threshold `6.0` months. Duplicated from `rules/moneywheel.py` (`healthy = (6.0, 9.0)`). |
| **`RULE_DEBT_BURDEN_EXCEEDED`** | [`rules/constraints.py:8,16`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/constraints.py#L8) | `debt_to_income_percent: float` | `bool` (breached if `> 40.0%`) | `HARD_CONSTRAINT` (Gate) | `DUPLICATED` | Threshold `40.0%` DTI. Duplicated from `rules/moneywheel.py` (`debt_to_income_ratio.critical = (40.0, None)`). |
| **`WARN_DEBT_BURDEN_ATTENTION`** | [`rules/constraints.py:9,17`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/constraints.py#L9) | `debt_to_income_percent: float` | `bool` (warning if `> 30.0%`) | `RANKING_INPUT` / Diagnostic | `DUPLICATED` | Threshold `30.0%` DTI. Duplicated from `rules/moneywheel.py` (`debt_to_income_ratio.healthy = (20.0, 30.0)`). |
| **`WARN_SAVINGS_RATE_DEFICIT`** | [`rules/constraints.py:10,19`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/constraints.py#L10) | `savings_ratio: float` | `bool` (warning if `< 20.0%`) | `RANKING_INPUT` / Diagnostic | `CANONICAL` | Threshold `20.0%` savings rate baseline. |
| **`classify` (Moneywheel)** | [`rules/moneywheel.py:30-41`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/moneywheel.py#L30-L41) | `key: str`, `value: float` | `Status: 'excellent' \| 'healthy' \| 'attention' \| 'critical'` | Diagnostic Rule Engine | `CANONICAL` | Versioned rule engine (Rule Set `1.3`) classifying 12 core financial ratios against benchmark intervals. |
| **`is_short_term_liability`** | [`rules/financial_metrics.py:12-14`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/financial_metrics.py#L12-L14) | `liability_type: str \| None` | `bool` | Classification Rule | `CANONICAL` | Classified against set: `{'Credit Card', 'Personal Loan', 'Consumer Loan', 'Other'}`. |
| **`is_essential_expense`** | [`rules/financial_metrics.py:23-25`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/financial_metrics.py#L23-L25) | `expense_type: str \| None` | `bool` | Classification Rule | `CANONICAL` | Classified against set: `{'Housing', 'Utilities', 'Groceries', 'Healthcare', 'Insurance', 'Education', 'Debt Payments'}`. |
| **`calculate_required_insurance_cover`** | [`rules/protection.py:26-31`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/protection.py#L26-L31) | `annual_income: float`, `total_liabilities: float` | `float` | Policy Calculation Formula | `CANONICAL` | Pure protection rule: `(annual_income * 10.0) + total_liabilities`. Assets are deliberately not netted off. |
| **`is_life_insurance` / `is_health_insurance`** | [`rules/protection.py:34-44`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/protection.py#L34-L44) | `policy_type: str \| None` | `bool` | Classification Rule | `CANONICAL` | Normalizes policy strings to qualify coverage as life or health. |
| **`canonical_goal_type`** | [`rules/goals.py:40-44`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/goals.py#L40-L44) | `value: str \| None` | `str` (canonical key) | Taxonomy Normalization | `CONFLICTING` | Normalizes aliases via `GOAL_TYPE_ALIASES`. In conflict: maps `passive income`, `debt repayment`, `philanthropy` to `other`. |
| **`is_discretionary_goal` / `is_essential_goal`** | [`rules/goals.py:47-56`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/goals.py#L47-L56) | `goal_type: str \| None` | `bool` | Priority Classification | `CANONICAL` | Categorizes goal types into essential (`emergency_fund`, `debt_repayment`, `retirement`) vs discretionary (`vacation`, `car`, `luxury`, `other`). |
| **`can_discretionary_preempt_essential`** | [`rules/multi_goal.py:26-32`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/multi_goal.py#L26-L32) | `discretionary: str`, `essential: str` | `bool` (`False` if discretionary vs essential) | Multi-Goal Precedence | `CANONICAL` | Hard policy: Discretionary goals must NEVER preempt funding for essential goals or safety reserve. |
| **`PRIORITY_RANK_MAP` (Rules)** | [`rules/multi_goal.py:9-14`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/multi_goal.py#L9-L14) | `priority: str \| None` | `int` (1, 2, 3, 4, default 3) | Precedence Ordering | `CONFLICTING` | 1-indexed rank: `critical: 1, high: 2, medium: 3, low: 4`. Conflicts with engines using 0-indexed scale. |
| **`PRIORITY_RANKS` (Engines)** | [`engines/orchestration/engine.py:16-21`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/engines/orchestration/engine.py#L16-L21)<br>[`engines/allocation/engine.py:14-19`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/engines/allocation/engine.py#L14-L19) | `priority: str \| None` | `int` (0, 1, 2, 3, default 4) | Precedence Ordering | `CONFLICTING` | 0-indexed rank: `critical: 0, high: 1, medium: 2, low: 3`. Duplicated in both engines and conflicting with rules. |
| **`assess_risk_capacity`** | [`rules/risk_profiler.py:4-10`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/risk_profiler.py#L4-L10) | `required: float \| None`, `capacity: float \| None` | `tuple[str, str]` (`PASS \| CONDITIONAL \| FAIL`, message) | `ELIGIBILITY` Gate | `CANONICAL` | Compares strategy risk requirement with investor risk capacity. Returns `FAIL` if required > capacity. |
| **`strategy_required_risk_capacity`** | [`rules/risk_profiler.py:13-22`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/risk_profiler.py#L13-L22) | `strategy: object` | `float \| None` | Parameter Extraction | `CANONICAL` | Reads `required_risk_capacity` or `risk_capacity_required` from strategy definition. |
| **`ELIGIBILITY_FITS` (8 Fits)** | [`rules/eligibility.py:14-23`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/eligibility.py#L14-L23) | `strategy`, `goal`, `financial_context` | `tuple[str, ...]` (8 fits) | `ELIGIBILITY` Gate | `CANONICAL` | Canonical tuple defining the 8 mandatory fits evaluated by `engines/strategy/eligibility.py`. |
| **`evaluate_decision_score`** | [`rules/strategy_decision.py:78-95`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/strategy_decision.py#L78-L95) | `status`, `goal_fit`, `horizon_fit`, `funding_fit`, `feasibility`, `component_fit` | `float` | Decision Scoring | `CANONICAL` | Evaluates total decision score. Forces score to `-100.0` (`INFEASIBLE_DECISION_SCORE`) if status is `fail`. |
| **`calculate_feasibility_score`** | [`rules/strategy_decision.py:55-64`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/strategy_decision.py#L55-L64) | `status: EligibilityStatus` | `float` (`pass=50.0, conditional=25.0, fail=-100.0`) | Decision Scoring | `CANONICAL` | Strongly enforces Pass precedence over Conditional in strategy selection. |
| **`build_action_specs`** | [`rules/action_plan.py:10-44`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/action_plan.py#L10-L44) | `primary_strategy`, `supporting_strategies`, `techniques` | `list[tuple[str, str, str]]` | Action Generation | `CANONICAL` | Deterministic action item generator. Assigns `high` priority to primary mechanism, `medium` to supporting & techniques. |

---

## 3. Hard vs. Soft Rules & Decision Roles

In [`engines/rules/engine.py:12-19`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/engines/rules/engine.py#L12-L19), the backend establishes `DecisionRole`, an authoritative classification of how rules govern the planning workflow:

```python
class DecisionRole(str, Enum):
    HARD_CONSTRAINT = "HARD_CONSTRAINT"          # Hard gate: blocks eligibility or triggers immediate action
    ELIGIBILITY = "ELIGIBILITY"                  # Strategy gate: must be satisfied to recommend a strategy
    RANKING_INPUT = "RANKING_INPUT"              # Scoring modifier: influences comparative order, not eligibility
    RECOMMENDATION_ONLY = "RECOMMENDATION_ONLY"  # Explanatory advisory text attached to output
    ARCHITECTURE_CONSTRAINT = "ARCHITECTURE_CONSTRAINT" # Governs combination of primary & supporting components
    EXPLANATORY_EVIDENCE = "EXPLANATORY_EVIDENCE"# Diagnostics retained for audit trail
```

### Precedence Hierarchy:
1. **`HARD_CONSTRAINT`:** Evaluated first (`emergency_reserve < 3.0 mo`, `debt_to_income > 40.0%`). If breached, demotes strategy feasibility or forces corrective action plans.
2. **`ELIGIBILITY`:** Evaluated across the 8 fits. If any fit returns `FAIL`, the strategy is rejected (`score = -100.0`).
3. **`CONDITIONAL` Adaptation:** If no `FAIL` occurs but conditional fits exist, required change text is generated via [`rules/adaptation.py`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/adaptation.py).
4. **`RANKING_INPUT`:** Feasible and conditional strategies are scored and ranked via [`rules/strategy_decision.py`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/strategy_decision.py).
5. **Behavioral Constraints Isolation:** Per [`docs/behavioral-profile-rules.md`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/docs/behavioral-profile-rules.md) and [`engines/profile/strategy_context.py`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/engines/profile/strategy_context.py), behavioral profile constraints are `soft` by default and isolated from strategy selection.

---

## 4. Current Implementation vs. Target Canonical Model

### Current Implementation:
- Rules are distributed across `backend/rules/`, but duplicate constants and thresholds reside inside `engines/constraints/evaluator.py`, `engines/rules/engine.py`, `engines/orchestration/engine.py`, and `engines/allocation/engine.py`.
- Two parallel priority scales exist: 1-indexed in `rules/multi_goal.py` and 0-indexed in `engines/orchestration/engine.py`.
- Duplicate module `backend/engines/risk_profiler/risk.py` is byte-for-byte identical to `backend/engines/profile/risk.py`.

### Target Canonical Model:
- **`backend/rules/` is the single source of truth for all thresholds, formulas, and score weights.**
- Engines must import rules strictly from `backend/rules/` and never hardcode fallback constants.
- Remove duplicate engine implementations (`engines/risk_profiler/` vs `engines/profile/`).

---

## 5. Gaps & Refactoring Implications

1. **Unify Goal Priority Ranking:** Change `engines/orchestration/engine.py` and `engines/allocation/engine.py` to import `PRIORITY_RANK_MAP` from `rules/multi_goal.py`.
2. **Consolidate Risk Profile Engines:** Delete `backend/engines/risk_profiler/risk.py` or redirect it to import from `backend/engines/profile/risk.py`.
3. **Reconcile Goal Taxonomy in `rules/goals.py`:** Update `GOAL_TYPE_ALIASES` to preserve `passive_income`, `debt_repayment`, and `philanthropy` as distinct canonical types rather than collapsing them into `other`.
4. **Relocate Rule Engine Models:** Move `RuleAssessment`, `RuleResult`, and `DecisionRole` from `backend/engines/rules/engine.py` into `backend/models/rule_assessment.py`.
