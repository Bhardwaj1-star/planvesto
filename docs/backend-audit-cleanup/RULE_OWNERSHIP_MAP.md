# Backend Rule Ownership Map

This document establishes the authoritative ownership model and audit map across the Planvesto backend as required by `IMPLEMENTATION_PLAN.md`.

## 1. Ownership Model

| Layer | Responsibility | What Belongs Here | What Does NOT Belong Here |
|---|---|---|---|
| **RULES** (`backend/rules/`) | What is true / what policy condition applies | Thresholds, benchmark ranges, eligibility formulas, classification maps, goal categories, action generation templates | Database queries, HTTP handling, complex multi-step orchestration |
| **ENGINES** (`backend/engines/`) | Calculate or evaluate using rules | Pure math calculations, state aggregation, ratio evaluation, portfolio allocation, constraint solving | Workflow coordination, database persistence, duplicate threshold definitions |
| **LIBRARY** (`backend/library/`) | Reusable knowledge & catalogs | Strategy catalog, technique definitions, baseline scenario templates | Execution logic, client profile evaluation, dynamic eligibility state |
| **SERVICES** (`backend/services/`) | Coordinate the workflow | Database querying, assembling engine inputs, persisting snapshots, calling engines | Hardcoded business rules, inline policy thresholds, scoring algorithms |
| **API** (`backend/api/`) | Expose workflow to consumers | Request validation, auth, response serialization, status codes | Business logic, calculations, database mutations outside services |
| **DATA** (`backend/data/`) | Read/write persistent data | Supabase repositories, raw SQL/PostgREST queries, data mapping | Business rule enforcement, financial formulas |

---

## 2. Audit Matrix

| Decision / Metric | Current Files | Current Owner | Duplicate? | Final Owner | Cleanup Action |
|---|---|---|---|---|---|
| **Moneywheel Ratios & Benchmarks** | `rules/moneywheel.py`, `engines/moneywheel/engine.py` | `rules/moneywheel.py` | Yes (thresholds duplicated in `engines/rules/engine.py` & `engines/constraints/evaluator.py`) | `rules/moneywheel.py` | Canonical ratio thresholds and classification remain in `rules/moneywheel.py`; consumers import from it rather than duplicating thresholds. |
| **Financial Health Diagnostics** | `engines/rules/engine.py`, `engines/constraints/evaluator.py` | Fragmented in engine files | Yes (hardcoded thresholds 9.0, 6.0, 1.5, 1.0, 20.0, 30.0 in `engines/rules/engine.py`) | Rules: `rules/moneywheel.py` & `rules/financial_metrics.py`<br>Evaluator: `engines/rules/engine.py` | Point `RuleEngine._health_diagnostic` to canonical benchmarks in `rules/moneywheel.py`. |
| **Health Score** | `engines/health_score/engine.py` | `engines/health_score/` | No (reserved placeholder) | `engines/health_score/engine.py` | Preserve clean placeholder; ensure it consumes canonical metrics once finalized. |
| **Financial State Metrics (Surplus, Reserve, Savings Rate)** | `rules/financial_state.py`, `engines/financial_state/engine.py`, `services/moneywheel_service.py` | Split between rules and services | Yes (re-calculated with fallbacks across services and constraints) | Formulas: `rules/financial_state.py`<br>Calculation: `engines/financial_state/engine.py` | Compute once in `FinancialStateEngine`; downstream consumers read from canonical `FinancialState`. |
| **Protection & Insurance Metrics** | `services/moneywheel_service.py`, `engines/moneywheel/financial_state_adapter.py` | `services/moneywheel_service.py` | Yes (required cover rule `10 * income + liabilities` hardcoded in service) | Rules: `rules/protection.py`<br>Service: `services/moneywheel_service.py` | Extract required cover and policy classification rules to `rules/protection.py`. |
| **Asset & Liability Classification (Liquidity, Essential)** | `services/moneywheel_service.py`, `engines/financial_state/engine.py` | `services/moneywheel_service.py` | Yes (`SHORT_TERM_LIABILITY_TYPES`, `ESSENTIAL_EXPENSE_TYPES` hardcoded in service) | `rules/financial_metrics.py` | Centralize expense and liability classification sets into rules layer. |
| **Goal-Type Classification & Aliases** | `engines/rules/engine.py`, `engines/constraints/evaluator.py`, `engines/strategy/decision.py`, `engines/strategy/eligibility.py` | Scattered in engines | Yes (`GOAL_TYPE_ALIASES` in `engines/rules/engine.py`, `DISCRETIONARY_GOAL_TYPES` in `engines/constraints/evaluator.py`) | `rules/goals.py` | Centralize canonical goal types, aliases, and categories (essential vs discretionary) into `rules/goals.py`. |
| **Constraints & Demotion Policy** | `engines/constraints/evaluator.py`, `engines/profile/constraints.py`, `engines/rules/engine.py` | Split between engines | Yes (hardcoded rule IDs, thresholds, priority demotions in `evaluator.py`) | Rules: `rules/constraints.py`<br>Evaluator: `engines/constraints/evaluator.py` & `engines/profile/engine.py` | Extract constraint thresholds and priority override policies to `rules/constraints.py`. |
| **Strategy Eligibility (8 Fits & Goal Gate)** | `engines/strategy/eligibility.py`, `engines/rules/engine.py` | `engines/strategy/eligibility.py` | Partial (both check goal applicability) | Rules: `rules/eligibility.py`<br>Evaluator: `engines/strategy/eligibility.py` | Maintain `engines/strategy/eligibility.py` as authoritative evaluator, referencing centralized goal rules. |
| **Strategy Applicability** | `engines/strategy/applicability.py`, `engines/rules/engine.py` | `engines/strategy/applicability.py` | No (delegates to `StrategyRuleEngine`) | Evaluator: `engines/strategy/applicability.py`<br>Rule Engine: `engines/rules/engine.py` | Maintain clear boundary: rule engine matches, applicability filters catalog. |
| **Strategy Selection (Decision Scoring)** | `engines/strategy/decision.py` | `engines/strategy/decision.py` | No (slots prepared for pending rules) | Rules: `rules/strategy_decision.py`<br>Evaluator: `engines/strategy/decision.py` | Clarify decision scoring slots; do not invent unapproved business logic. |
| **Strategy Variants & Scenarios** | `engines/strategy/scenario.py`, `library/strategies/` | Library + Engine | No | Library: `library/strategies/`<br>Engine: `engines/strategy/scenario.py` | Maintain separation of catalog templates and dynamic scenario evaluation. |
| **Adaptation Conditions (Conditional Fits)** | `engines/strategy/eligibility.py`, `engines/strategy/decision.py` | `engines/strategy/eligibility.py` | No | Rules: `rules/eligibility.py`<br>Engine: `engines/strategy/eligibility.py` | Standardize required change generators for conditional status. |
| **Multi-Goal Allocation & Trade-Offs** | `engines/allocation/engine.py`, `engines/orchestration/orchestrator.py`, `services/multi_goal_planning_service.py` | Allocation & Orchestration engines | No | Rules: `rules/multi_goal.py`<br>Engine: `engines/allocation/` & `engines/orchestration/` | Centralize trade-off thresholds and priority order rules in `rules/multi_goal.py`. |
| **Action-Plan Generation Rules** | `services/strategy_action_generator.py` | `services/strategy_action_generator.py` | Yes (action template generators hardcoded directly in service) | Rules: `rules/action_plan.py`<br>Generator Service: `services/strategy_action_generator.py` | Extract action template generation logic into `rules/action_plan.py`. Service only coordinates data fetching and storage. |

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
