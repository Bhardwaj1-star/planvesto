# Backend Rule Ownership Map

This document establishes the authoritative ownership model, audit matrix, and single source of truth across the Planvesto backend as required by `IMPLEMENTATION_PLAN.md` and `RULE_FINALIZATION_PROCESS.md`.

## 1. Ownership Model

| Layer | Responsibility | What Belongs Here | What Does NOT Belong Here |
|---|---|---|---|
| **RULES** (`backend/rules/`) | What is true / what policy condition applies | Thresholds, benchmark ranges, eligibility formulas, classification maps, goal categories, action generation templates, decision scoring weights, multi-goal priority rules | Database queries, HTTP handling, complex multi-step orchestration |
| **ENGINES** (`backend/engines/`) | Calculate or evaluate using rules | Pure math calculations, state aggregation, ratio evaluation, portfolio allocation, constraint solving, decision score evaluation | Workflow coordination, database persistence, duplicate threshold definitions |
| **LIBRARY** (`backend/library/`) | Reusable knowledge & catalogs | Strategy catalog, technique definitions, baseline scenario templates | Execution logic, client profile evaluation, dynamic eligibility state |
| **SERVICES** (`backend/services/`) | Coordinate the workflow | Database querying, assembling engine inputs, persisting snapshots, calling engines | Hardcoded business rules, inline policy thresholds, scoring algorithms |
| **API** (`backend/api/`) | Expose workflow to consumers | Request validation, auth, response serialization, status codes | Business logic, calculations, database mutations outside services |
| **DATA** (`backend/data/`) | Read/write persistent data | Supabase repositories, raw SQL/PostgREST queries, data mapping | Business rule enforcement, financial formulas |

---

## 2. Granular Audit Matrix (per `RULE_FINALIZATION_PROCESS.md` Section 5)

### A. Financial Truth

| Concept | Current Implementation | Duplicate Locations | Final Owner | Status |
|---|---|---|---|---|
| **Income & Expenses** | `rules/financial_state.py`, `engines/financial_state/engine.py` | Extracted across services and profile | `rules/financial_state.py` (formulas)<br>`engines/financial_state/engine.py` (calculation) | **Centralized** |
| **Surplus & Savings Rate** | `rules/financial_state.py`, `engines/financial_state/engine.py` | Recalculated in `constraints/evaluator.py` | `rules/financial_state.py` | **Centralized** |
| **Emergency Reserve** | `rules/moneywheel.py`, `rules/constraints.py` | Hardcoded 9.0 / 6.0 in `engines/rules/engine.py` | `rules/moneywheel.py` & `rules/constraints.py` | **Centralized** (referenced by `RuleEngine`) |
| **Debt Burden & Leverage** | `rules/moneywheel.py`, `rules/constraints.py` | Hardcoded 20.0 / 30.0 in `engines/rules/engine.py` | `rules/moneywheel.py` & `rules/constraints.py` | **Centralized** |
| **Protection / Insurance** | `rules/protection.py` | Hardcoded 10x cover formula in `services/moneywheel_service.py` | `rules/protection.py` | **Centralized** |
| **Asset & Liability Classes** | `rules/financial_metrics.py` | Hardcoded sets in `services/moneywheel_service.py` | `rules/financial_metrics.py` | **Centralized** |
| **Moneywheel Ratios** | `rules/moneywheel.py` | 12 canonical ratios and benchmarks | `rules/moneywheel.py` (rules)<br>`engines/moneywheel/engine.py` (evaluation) | **Centralized** |
| **Financial Health Diagnostics** | `engines/rules/engine.py` | None (now consumes `rules.moneywheel.RULES`) | `engines/rules/engine.py` consuming `rules/moneywheel.py` | **Centralized** |
| **Health Score** | Obsolete engine removed (`e00e12e`) | Previously unused placeholder | Consolidated into Moneywheel & diagnostic interpretation | **Removed / Consolidated** |

### B. Goal Truth

| Concept | Current Implementation | Duplicate Locations | Final Owner | Status |
|---|---|---|---|---|
| **Goal Types & Normalization** | `rules/goals.py` (`GOAL_TYPE_ALIASES`, `canonical_goal_type`) | Previously duplicated across `engines/rules/`, `engines/strategy/`, `services/` | `rules/goals.py` | **Centralized** |
| **Goal Categories (Essential vs Discretionary)** | `rules/goals.py` (`ESSENTIAL_GOAL_TYPES`, `DISCRETIONARY_GOAL_TYPES`) | Hardcoded in `engines/constraints/evaluator.py` | `rules/goals.py` | **Centralized** |
| **Goal Priority & Precedence** | `rules/multi_goal.py`, `rules/goals.py` | Priority ranks scattered in allocation & constraints | `rules/multi_goal.py` | **Centralized** |
| **Goal Horizon & Feasibility** | `engines/rules/engine.py` (`assess`) | Goal gate in `engines/strategy/eligibility.py` | `engines/rules/engine.py` & `engines/strategy/eligibility.py` | **Centralized** |
| **Goal Conflict Handling** | `rules/multi_goal.py`, `engines/strategy/eligibility.py` | Discretionary vs essential conflict rules | `rules/multi_goal.py` (rules)<br>`engines/strategy/eligibility.py` (fit evaluation) | **Centralized** |

### C. Strategy Truth

| Concept | Current Implementation | Duplicate Locations | Final Owner | Status |
|---|---|---|---|---|
| **Strategy Library** | `library/strategies/` (catalog, techniques, registry) | None (pure knowledge catalog) | `library/strategies/` | **Authoritative** (no investor decisions) |
| **Strategy Applicability** | `engines/strategy/applicability.py`, `engines/rules/engine.py` | None | `engines/strategy/applicability.py` delegating to `StrategyRuleEngine` | **Authoritative** |
| **Strategy Eligibility (8 Fits)** | `rules/eligibility.py`, `engines/strategy/eligibility.py` | Fit enum duplicated in engine | `rules/eligibility.py` (definitions)<br>`engines/strategy/eligibility.py` (evaluator) | **Centralized** |
| **Conditional Strategy & Required Changes** | `rules/adaptation.py`, `engines/strategy/eligibility.py` | Inline string formatting in fit evaluations | `rules/adaptation.py` (adaptation rules)<br>`engines/strategy/eligibility.py` (evaluator) | **Centralized** |
| **Strategy Decision & Scoring** | `rules/strategy_decision.py`, `engines/strategy/decision.py` | Hardcoded score weights in `decision.py` | `rules/strategy_decision.py` (rules & slots)<br>`engines/strategy/decision.py` (evaluator) | **Centralized** |
| **Strategy Variants & Scenarios** | `engines/strategy/scenario.py` | None | `engines/strategy/scenario.py` | **Authoritative** |

### D. Action Truth

| Concept | Current Implementation | Duplicate Locations | Final Owner | Status |
|---|---|---|---|---|
| **Action Plan Generation Rules** | `rules/action_plan.py` (`build_action_specs`) | Hardcoded action generation specs in `services/strategy_action_generator.py` | `rules/action_plan.py` | **Centralized** |
| **Action Plan Lifecycle** | `services/action_plan_service.py`, `services/strategy_action_generator.py` | None | `services/action_plan_service.py` | **Authoritative** |
| **Action Impact Evaluation** | `engines/action_plan/impact_engine.py` | None | `engines/action_plan/impact_engine.py` | **Authoritative** |

### E. Multi-Goal Truth

| Concept | Current Implementation | Duplicate Locations | Final Owner | Status |
|---|---|---|---|---|
| **Priority Hierarchy** | `rules/multi_goal.py` (`PRIORITY_RANK_MAP`) | Evaluator and allocation hardcoding | `rules/multi_goal.py` | **Centralized** |
| **Trade-Off Policies** | `rules/multi_goal.py` (`can_discretionary_preempt_essential`) | Hardcoded in `constraints/evaluator.py` | `rules/multi_goal.py` | **Centralized** |
| **Resource Allocation** | `engines/allocation/engine.py` | Orchestration engine | `engines/allocation/engine.py` | **Authoritative** |
| **Multi-Goal Orchestration** | `engines/orchestration/orchestrator.py`, `services/multi_goal_planning_service.py` | None | `engines/orchestration/orchestrator.py` | **Authoritative** |

---

## 3. Financial Truth & Single Source of Calculation

```text
                  Financial State (Raw Inputs)
                               │
                               ▼
                    FinancialStateEngine
               (engines/financial_state/engine.py)
                               │
               Authoritative Financial Metrics:
        - income_monthly, expenses_monthly, investable_surplus_monthly
        - safety_reserve_months, safety_reserve_required_amount
        - cash_flow_ratio, savings_investment_rate
        - total_assets, total_liabilities, emi_burden_monthly, net_worth
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
  Moneywheel Engine       Health Diagnostics    Constraint Evaluator
(engines/moneywheel/)     (engines/rules/)      (engines/constraints/)
 Ratios & Visual Wheel   Evidence & Diagnostics  Hard/Soft Demotions
```

**Rule of Thumb:**
- No engine or service should calculate a ratio from raw data if that metric is already defined in `FinancialState`.
- Benchmark thresholds must always be read from `rules/moneywheel.py` or canonical rule modules.
- Health Score engine was removed as obsolete (`e00e12e`), preventing any competing scoring systems.
