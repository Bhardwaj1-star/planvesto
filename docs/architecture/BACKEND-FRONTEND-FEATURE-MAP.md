# Backend Structure → Frontend Feature Map

Repository: Bhardwaj1-star/planvesto

## Purpose

This document maps the current backend structure to investor-facing frontend features.

It has two views:
1. Backend file/folder responsibility table.
2. Frontend feature mind-map showing which backend domains power each investor-visible feature.

The important architectural distinction is that backend decision infrastructure does not automatically imply a separate frontend screen.

## 1. System overview

\`\`\`
Investor UI
  ↓
Frontend API clients / hooks
  ↓
FastAPI API layer
  ↓
Service layer
  ↓
Domain engines
  ├── Financial State / Calculation
  ├── Goals
  ├── Constraints / Rules
  ├── Risk Profiler
  ├── Strategy
  ├── Allocation / Investment
  ├── Orchestration
  └── Reports / Action Plan
  ↓
Models / Schemas / Data
  ↓
Supabase / persistence
\`\`\`

## 2. Backend API layer

| File | Responsibility | Frontend surface |
|---|---|---|
| backend/main.py | FastAPI bootstrap, router registration and application setup | All API traffic |
| backend/api/auth.py | Authentication endpoints | Auth/session |
| backend/api/dashboard.py | Dashboard aggregation endpoints | Investor Dashboard |
| backend/api/financial_state.py | Financial-state read/write endpoints | Financial State |
| backend/api/goals.py | Goal CRUD and goal endpoints | Goals / Goal Planner |
| backend/api/strategy.py | Strategy recommendation/execution endpoints | Strategy |
| backend/api/strategy_edit.py | Strategy editing endpoints | Strategy Edit |
| backend/api/strategy_version.py | Strategy version/history endpoints | Strategy History |
| backend/api/orchestration.py | Planning/orchestration endpoints | Goal Planner / planning |
| backend/api/moneywheel.py | MoneyWheel endpoints | MoneyWheel |
| backend/api/action_plan.py | Action-plan endpoints | Action Plan |
| backend/api/diary.py | Diary endpoints | Diary |
| backend/api/insurance.py | Insurance endpoints | Insurance |
| backend/api/profile.py | Profile endpoints | Profile-related surfaces |
| backend/api/goal_basket.py | Goal-basket endpoints | Multi-goal |
| backend/api/basket_report.py | Basket report endpoints | Reports |
| backend/api/summary_report.py | Summary report endpoints | Reports |

## 3. Backend service layer

| File | Responsibility |
|---|---|
| backend/services/financial_state_service.py | Builds/reads canonical financial state and coordinates financial-state operations |
| backend/services/goal_service.py | Goal lifecycle/business operations |
| backend/services/strategy_service.py | Strategy workflow and constraint/rule coordination |
| backend/services/strategy_edit_service.py | Strategy editing and version operations |
| backend/services/strategy_service.py | Builds the authoritative ConstraintSet and coordinates StrategyEngine inputs |
| backend/services/multi_goal_planning_service.py | Multi-goal planning; consumes canonical ConstraintSet |
| backend/services/goal_report_service.py | Goal report construction |
| backend/services/financial_plan_service.py | Financial-plan workflow orchestration |
| backend/services/basket_report_service.py | Basket-level report construction |

Service layer should orchestrate engines, not create competing financial or constraint policy.

## 4. Financial State and Calculation

Calculation is a distinct backend layer and should not be collapsed into the Constraint layer. The canonical shared-math owner is `backend/engines/calculation/canonical.py`; domain-specific calculations sit in their domain engines.

### Calculation infrastructure

| File | Responsibility | Main outputs / calculations | Frontend features |
|---|---|---|---|
| backend/engines/calculation/canonical.py | **Canonical owner of shared financial mathematics and derived facts** | Cash-flow ratio, savings rate, liquid-asset ratio, expense coverage, emergency coverage, DTI, leverage, financial-asset ratio, insurance coverage, goal funding ratio, future funding ratio, required return / risk-required, portfolio concentration, future goal target, funding gap, required monthly contribution | Financial State, MoneyWheel, Goal Planner, Risk, Strategy |
| backend/engines/calculation/engine.py | Calculation utilities | `round_money`, monthly/annual frequency conversion, percentage helper | Shared backend utility |
| backend/engines/calculation/__init__.py | Public calculation API | Exposes canonical calculation functions and DerivedFact builders | Internal package boundary |
| backend/engines/financial_state/engine.py | Builds/derives authoritative current financial state | Aggregated income, expenses, assets, liabilities, surplus and related state facts | Financial State, Dashboard |
| backend/rules/financial_state.py | Compatibility/domain wrappers around canonical calculations | Financial-state ratios/reserve helpers | Internal compatibility layer |
| backend/engines/moneywheel/engine.py | Applies canonical calculations to MoneyWheel domain inputs and classifications | Savings, liquidity, coverage, leverage, required return and other MoneyWheel metrics | MoneyWheel |
| backend/services/moneywheel_service.py | Builds MoneyWheel result from authoritative FinancialState | Server-side calculation workflow | MoneyWheel |
| backend/api/moneywheel.py | Exposes MoneyWheel calculation endpoint | `POST /api/moneywheel/calculate` | MoneyWheel page |

### Goal-specific calculation layer

| File | Responsibility | Main calculations | Frontend feature |
|---|---|---|---|
| backend/engines/goal/target_calculator.py | Goal target/time calculations | Duration, inflation-adjusted future target, retirement corpus, education target | Goal Planner |
| backend/engines/goal/funding_gap.py | Goal funding calculations | Funding gap, required monthly contribution, weighted funding return assumption | Goal Feasibility |
| backend/engines/goal/asset_projection.py | Asset projection | Allocated amount/percentage and projected future asset value | Goal Feasibility |
| backend/engines/goal/specialized.py | Specialized goal mathematics | Retirement corpus, education target and other goal-specific targets | Goal Planner |
| backend/engines/goal/engine.py | Goal calculation orchestration | Combines target, projection, funding-gap and feasibility calculations into DefinedGoal | Goal Planner |

### Canonical calculation formulas

| Calculation | Canonical function | Formula / meaning |
|---|---|---|
| Cash-flow ratio | `calculate_cash_flow_ratio` | Monthly Expenses / Monthly Income × 100 |
| Savings rate | `calculate_savings_rate` | Monthly Surplus / Monthly Income × 100 |
| Liquid asset ratio | `calculate_liquid_asset_ratio` | Liquid Assets / Total Assets × 100 |
| Expense coverage | `calculate_expense_coverage` | Liquid Assets / Monthly Expenses, in months |
| Emergency coverage | `calculate_emergency_coverage` | Liquid Assets / Essential Monthly Expenses, in months |
| Debt-to-income | `calculate_debt_to_income_ratio` | Monthly Debt Payments / Gross Monthly Income, optionally × 100 |
| Leverage | `calculate_leverage_ratio` | Total Liabilities / Total Assets × 100 |
| Financial asset ratio | `calculate_financial_asset_ratio` | Financial Assets / Total Assets × 100 |
| Insurance coverage | `calculate_insurance_coverage_ratio` | Existing Sum Assured / Required Insurance Cover × 100 |
| Goal funding ratio | `calculate_goal_funding_ratio` | Current Goal Funding / Goal Target × 100 |
| Future funding ratio | `calculate_future_funding_ratio` | Projected Goal Funding / Future Goal Target × 100 |
| Required return | `calculate_required_rate_of_return` | CAGR needed to grow current funding to future target |
| Future goal target | `calculate_goal_future_target` | Today Cost × (1 + Inflation)^Years |
| Goal funding gap | `calculate_goal_funding_gap` | Future Target − Projected Mapped Asset Value |
| Required monthly contribution | `calculate_required_monthly_contribution` | End-of-month contribution needed to close a positive funding gap |

**Calculation ownership rule:** shared financial mathematics and derived facts belong to `engines/calculation/canonical.py`. Domain engines may orchestrate or add domain-specific mathematics, but they should reuse canonical shared calculations where the same financial fact already exists. Calculation produces facts/metrics; constraint policy and decision effects belong to `engines/constraints`.

**Important distinction:** a calculation being used by a constraint evaluator does not make the calculation itself a constraint. Example: DTI calculation is canonical math; the decision that a DTI level constrains a discretionary goal belongs to `engines/constraints/evaluator.py` + `policy.py`.

## 5. Goal engine

| File | Responsibility | Features |
|---|---|---|
| backend/engines/goal/engine.py | Goal calculation orchestration | Goal Planner |
| backend/engines/goal/target_calculator.py | Future target calculations | Goal Planner |
| backend/engines/goal/funding_gap.py | Funding-gap calculation | Goal Feasibility |
| backend/engines/goal/asset_projection.py | Asset/funding projection | Goal Feasibility |
| backend/engines/goal/specialized.py | Specialized goal calculations | Goal-specific planning |

## 6. Constraints — canonical decision-control layer

| File | Responsibility | Ownership |
|---|---|---|
| backend/engines/constraints/policy.py | Constraint IDs, thresholds, normalization, conflicts, priority semantics and policy | CANONICAL OWNER |
| backend/engines/constraints/evaluator.py | Evaluates financial/goal constraint conditions | CANONICAL EVALUATOR |
| backend/engines/constraints/adapters.py | Converts rule/risk/strategy/domain outputs to CanonicalConstraint | CANONICAL ADAPTER |
| backend/engines/constraints/aggregator.py | Aggregates all constraints into one ConstraintSet | CANONICAL AGGREGATOR |
| backend/engines/constraints/models.py | CanonicalConstraint, ConstraintSet, conflict/severity/role models | CANONICAL CONTRACT |
| backend/engines/constraints/__init__.py | Public constraint-layer API | Package boundary |

Canonical flow:

\`\`\`
Domain facts / evidence
      ↓
Rules / Domain Evaluators
      ↓
constraints/adapters.py
      ↓
constraints/aggregator.py
      ↓
Canonical ConstraintSet

constraints/policy.py provides the authoritative IDs, thresholds and policy semantics
used by evaluators/adapters/consumers; it is not a sequential processing stage.
      ↓
Strategy / Multi-goal / downstream consumers
\`\`\`

Compatibility facades:
- backend/rules/constraints.py
- backend/engines/profile/constraints.py

These should not become new policy owners.

## 7. Rules

| File | Responsibility | Boundary |
|---|---|---|
| backend/engines/rules/engine.py | Goal/rule evaluation and backward-compatible RuleAssessment | Rule evaluation; delegates constraint policy |
| backend/rules/canonical.py | Canonical rule registry and metadata | Rule identity/scope/role |
| backend/rules/goals.py | Goal type and priority normalization | Goal classification |
| backend/rules/multi_goal.py | Multi-goal allocation/priority rules | Multi-goal behavior |
| backend/rules/moneywheel.py | MoneyWheel diagnostic definitions/classification | Financial diagnostics |
| backend/rules/constraints.py | Compatibility facade | No independent constraint policy |

Rule = business condition, classification, eligibility or diagnostic logic.

Constraint = canonical decision-control representation/policy outcome.

## 8. Risk and Profile

| File | Responsibility | Features |
|---|---|---|
| backend/engines/risk_profiler/engine.py | Risk Required, Risk Capacity, Risk Tolerance and evidence assembly | Risk / Strategy suitability |
| backend/engines/risk_profiler/models.py | Risk profile contracts | Risk |
| backend/engines/profile/engine.py | Investor/profile evidence assembly | Profile / onboarding |
| backend/engines/profile/constraints.py | Compatibility facade to canonical constraint policy | Internal |
| backend/engines/profile/behavioral.py | Observed behavior normalization | Risk tolerance / product selection |

Risk/Profile engines produce domain evidence; canonical decision normalization happens through the constraints layer.

## 9. Strategy

| File/folder | Responsibility | Features |
|---|---|---|
| backend/engines/strategy/engine.py | Strategy workflow coordinator; consumes canonical ConstraintSet | Strategy |
| backend/services/strategy_service.py | Builds authoritative ConstraintSet from rule, ratio, risk and strategy-domain outputs | Strategy |
| backend/engines/strategy/applicability.py | Strategy applicability filtering | Strategy |
| backend/engines/strategy/eligibility.py | Strategy eligibility | Strategy |
| backend/engines/strategy/scenario.py | Baseline and what-if scenarios | Strategy Scenarios |
| backend/engines/strategy/comparison.py | Strategy/scenario comparison | Strategy Scenarios |
| backend/engines/strategy/ranking.py | Ranking | Strategy Recommendation |
| backend/engines/strategy/recommendation.py | Recommendation generation | Strategy Recommendation |
| backend/engines/strategy/composition.py | Strategy architecture composition | Strategy |
| backend/engines/strategy/decision.py | Final decision evaluation | Strategy |

Strategy consumes ConstraintSet as decision context.

## 10. Allocation, Investment and Technique

| File | Responsibility |
|---|---|
| backend/engines/allocation/engine.py | Allocation calculations |
| backend/engines/allocation/models.py | Allocation contracts |
| backend/engines/investment/engine.py | Investment-level decision/calculation flow |
| backend/engines/investment/models.py | Investment contracts |
| backend/engines/technique/engine.py | Deterministic implementation techniques |

These are downstream of financial facts, strategy decisions and constraints.

## 11. Orchestration

| File | Responsibility |
|---|---|
| backend/engines/orchestration/engine.py | Multi-goal planning orchestration |
| backend/engines/orchestration/models.py | Orchestration input/output contracts |
| backend/services/multi_goal_planning_service.py | Service boundary around multi-goal orchestration and canonical constraints |

Core flow:

\`\`\`
Goals
 ↓
Goal calculations
 ↓
Financial State
 ↓
ConstraintSet
 ↓
Strategy evaluation
 ↓
Multi-goal orchestration
 ↓
Plan / trade-offs / notes / audit
\`\`\`

## 12. Reports / Action Plan / Suitability

| File | Responsibility | Feature |
|---|---|---|
| backend/engines/summary_report/engine.py | Summary report assembly | Reports |
| backend/engines/action_plan/impact_engine.py | Action impact calculations | Action Plan |
| backend/engines/suitability/engine.py | Suitability logic | Strategy / suitability |
| backend/engines/basket/engine.py | Goal-basket analysis | Multi-goal / Reports |

## 13. Models, schemas and data

### Models

backend/models/ contains domain/application models such as:
- defined_goal.py
- strategy.py
- strategy_version.py
- financial_state.py
- primary_strategy.py
- primary_strategy_state.py
- moneywheel.py
- orchestration.py
- action_plan.py
- insurance.py
- profile.py
- goal_basket.py
- summary_report.py
- diary.py

### Schemas

backend/schemas/ contains API validation and serialization contracts for:
- goals
- strategy
- strategy versions
- financial state
- MoneyWheel
- orchestration
- action plan
- insurance
- dashboard
- profile
- goal basket
- summary report
- diary

### Data

backend/data/ contains repository/persistence concerns. Database access should remain isolated from domain engines.

# 14. Frontend investor feature map

| Route | Investor feature | Main backend domains |
|---|---|---|
| frontend/app/investor/page.tsx | Dashboard | Dashboard, Financial State, Goals, Reports |
| frontend/app/investor/onboarding/* | Onboarding | Profile, Financial State, Goals, Insurance |
| frontend/app/investor/financial-state/page.tsx | Financial State | Financial State, Calculation, MoneyWheel |
| frontend/app/investor/moneywheel/page.tsx | MoneyWheel | MoneyWheel engine/rules |
| frontend/app/investor/goal-planner/page.tsx | Goal Planner | Goal, Constraints, Orchestration |
| frontend/app/investor/strategy-scenarios/page.tsx | Strategy Scenarios | Strategy Scenario, Comparison, Ranking, Decision |
| frontend/app/investor/strategy-edit/page.tsx | Strategy Edit | Strategy Edit Service, Strategy Version |
| frontend/app/investor/strategy-history/page.tsx | Strategy History | Strategy Version |
| frontend/app/investor/action-plan/page.tsx | Action Plan | Action Plan |
| frontend/app/investor/reports/page.tsx | Reports | Summary, Goal Report, Basket Report |
| frontend/app/investor/onboarding/insurance/page.tsx | Insurance | Insurance |
| frontend/components/InvestorSidebar.tsx | Investor navigation | Connects investor feature surfaces |

Frontend API clients live primarily under frontend/lib/api/.

# 15. Frontend feature mind-map

\`\`\`
INVESTOR EXPERIENCE
│
├── Dashboard
│   ├── api/dashboard.py
│   ├── financial_state_service.py
│   ├── goal_service.py
│   └── summary_report/engine.py
│
├── Calculation Foundation (shared across features)
│   ├── engines/calculation/canonical.py
│   ├── engines/calculation/engine.py
│   └── feeds Financial State, MoneyWheel, Goals, Risk and Strategy
│
├── Onboarding
│   ├── Personal Information
│   │   └── Profile / identity
│   ├── Income
│   │   └── Financial State
│   ├── Expenses
│   │   └── Financial State
│   ├── Assets
│   │   └── Financial State
│   ├── Liabilities
│   │   └── Financial State / debt metrics
│   ├── Goals
│   │   └── Goal Engine
│   ├── Insurance
│   │   └── Insurance Domain
│   └── Family / Dependents
│       └── Profile / Financial State inputs
│
├── Financial State
│   ├── financial_state/engine.py
│   ├── calculation/canonical.py
│   ├── rules/moneywheel.py
│   └── constraints/*
│
├── MoneyWheel
│   ├── moneywheel/engine.py
│   ├── rules/moneywheel.py
│   ├── calculation/canonical.py
│   └── api/moneywheel.py
│
├── Goal Planner
│   ├── goal/engine.py
│   ├── target_calculator.py
│   ├── funding_gap.py
│   ├── asset_projection.py
│   ├── constraints/*
│   ├── orchestration/engine.py
│   └── multi_goal_planning_service.py
│
├── Strategy
│   ├── strategy/engine.py
│   ├── applicability.py
│   ├── eligibility.py
│   ├── decision.py
│   ├── ranking.py
│   ├── recommendation.py
│   ├── composition.py
│   ├── risk_profiler/engine.py
│   └── constraints/ConstraintSet
│
├── Strategy Scenarios
│   ├── strategy/scenario.py
│   ├── strategy/comparison.py
│   ├── strategy/ranking.py
│   └── strategy/decision.py
│
├── Strategy Edit
│   ├── api/strategy_edit.py
│   ├── strategy_edit_service.py
│   └── strategy_version APIs/models
│
├── Strategy History
│   ├── api/strategy_version.py
│   ├── strategy_version model
│   └── persistence
│
├── Action Plan
│   ├── api/action_plan.py
│   └── action_plan/impact_engine.py
│
├── Reports
│   ├── api/summary_report.py
│   ├── api/basket_report.py
│   ├── goal_report_service.py
│   ├── basket_report_service.py
│   └── summary_report/engine.py
│
└── Risk / Suitability
    ├── risk_profiler/engine.py
    ├── risk_profiler/models.py
    ├── suitability/engine.py
    └── constraints/adapters.py
\`\`\`

# 16. Feature dependency matrix

| Feature | Primary backend | Secondary backend | Constraint involvement |
|---|---|---|---|
| Dashboard | Dashboard API | Financial State, Goals, Reports | Output-level |
| Onboarding | Profile + Financial State APIs | Goals, Insurance | Feeds constraints |
| Financial State | Financial State engine | Canonical calculations | Yes |
| MoneyWheel | MoneyWheel engine | MoneyWheel rules | Diagnostic/evidence |
| Goal Planner | Goal engine | Orchestration, Reports | Heavy |
| Strategy | Strategy engine | Risk Profiler, Technique | Heavy |
| Strategy Scenarios | Scenario + Ranking | Decision | Yes |
| Strategy Edit | Strategy Edit Service | Strategy Version | Indirect |
| Strategy History | Strategy Version API/model | Persistence | No direct calculation |
| Action Plan | Action Plan API/engine | Strategy/Goal context | Downstream |
| Reports | Report services/engines | Goal/Basket/Summary APIs | Reflects outputs |
| Insurance | Insurance API/domain | Financial State | Feeds protection context |

# 17. Investor-visible vs backend-only

## Investor-visible

- Dashboard
- Onboarding
- Financial State
- MoneyWheel
- Goals / Goal Planner
- Strategy Recommendation
- Strategy Scenarios
- Strategy Edit
- Strategy History
- Action Plan
- Reports
- Insurance

## Backend infrastructure

- Constraint policy
- Constraint evaluator
- Constraint adapters
- Constraint aggregator
- Rule registry
- Canonical calculations
- Domain engines
- Repositories
- API schemas/models
- Orchestration internals
- Audit/provenance

A backend layer being important to the decision engine does not mean it needs a dedicated frontend page.

Example:

\`\`\`
ConstraintSet
RuleEngine
RiskProfiler
Canonical Calculation
Strategy Decision
\`\`\`

These are decision infrastructure. Their outputs appear through Dashboard, Goal Planner, Strategy, Reports and Action Plan.

# 18. Architectural ownership rules

| Concern | Owner |
|---|---|
| Financial facts | engines/financial_state + engines/calculation |
| Financial diagnostics | engines/moneywheel + canonical calculations |
| Constraint policy | engines/constraints/policy.py |
| Constraint evaluation | engines/constraints/evaluator.py |
| Constraint normalization | engines/constraints/adapters.py |
| Constraint aggregation | engines/constraints/aggregator.py |
| Constraint data contract | engines/constraints/models.py |
| Goal calculations | engines/goal |
| Risk assessment | engines/risk_profiler |
| Strategy decision | engines/strategy |
| Multi-goal orchestration | engines/orchestration |
| Investor API contract | backend/api + backend/schemas |
| Investor UI | frontend/app/investor |
| Frontend API clients | frontend/lib/api |
| Reusable UI components | frontend/components |

# 19. Dependency direction

Intended direction:

\`\`\`
Frontend
  ↓
API
  ↓
Services
  ↓
Domain Engines
  ↓
Canonical Calculations / Constraints
  ↓
Models / Data
\`\`\`

Avoid:

\`\`\`
Frontend → engine internals
Service → duplicated policy
Rule module → competing ConstraintSet
Strategy → direct database logic
Multiple engines → independent constraint policy
\`\`\`

The canonical downstream decision contract is ConstraintSet.

# 20. Navigation index

- Constraint work: backend/engines/constraints/
- Financial calculations: backend/engines/calculation/
- Financial State: backend/engines/financial_state/
- Goals: backend/engines/goal/
- Risk: backend/engines/risk_profiler/
- Strategy: backend/engines/strategy/
- Multi-goal: backend/engines/orchestration/ and backend/services/multi_goal_planning_service.py
- APIs: backend/api/
- Models: backend/models/
- Schemas: backend/schemas/
- Investor UI: frontend/app/investor/
- Frontend API clients: frontend/lib/api/
- Frontend components: frontend/components/

## Status

This is a navigation and ownership map. When a domain engine, API surface or investor-facing feature materially changes, update this document with the implementation change.
