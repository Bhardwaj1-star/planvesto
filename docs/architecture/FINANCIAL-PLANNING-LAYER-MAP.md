# Planvesto Financial Planning Layer Map

This document defines the current domain/layer boundaries for Planvesto's financial-planning system. The layer map is anchored to the implemented frontend and backend code. The reference model for this map is the layer structure represented by this document; other documentation is not used as evidence for the code audit.

## Layer Map

| # | Layer | What it is | Purpose | Primary data source |
|---|---|---|---|---|
| 1 | Onboarding / Financial Inputs | Customer source-input layer | Collect the customer's financial picture | Personal information, family/dependents, income, expenses, assets, insurance, liabilities, goals |
| 2 | Financial State | Authoritative current financial-state aggregate | Represent the customer's current financial position | Persisted Planning Unit financial records |
| 3 | Financial Calculations / Measures | Canonical calculation layer | Derive standardized financial metrics from the current state | Current FinancialState |
| 4 | Financial Health | Financial-condition assessment layer | Assess financial strengths, weaknesses, risks, and conditions | Current FinancialState + canonical metrics |
| 5 | MoneyWheel | Financial diagnostic framework | Measure financial health through canonical ratios and coverage rules | Current FinancialState + canonical calculation layer |
| 6 | Constraints / Rules | Decision-control layer | Identify financial limits, warnings, and hard constraints | FinancialState + canonical metrics + rule/threshold definitions |
| 7 | Investor Profile / Risk | Customer suitability, risk, behavioral, identity, and preference context layer | Build the decision context used by downstream planning | Investor profile + RiskProfile + behavioral evidence + identity evidence + priorities |
| 8 | Budgeting | Cash-flow control layer | Set budget limits and compare actual spending against budget | Expenses + liabilities + budget_limits |
| 9 | Goal Planner | Individual-goal planning layer | Define goals, calculate requirements, funding gap/contribution, and feasibility | Customer goals + DefinedGoal inputs + FinancialState + mapped assets |
| 10 | Goal Basket | Logical goal-grouping layer | Group existing goals together for combined planning and reporting | Existing goals + GoalBasket definition |
| 11 | Strategy Builder / StrategyRun | Strategy decision and evaluation layer | Filter, compare, evaluate, rank, and recommend strategies/scenarios for a goal; persist the evaluation run | DefinedGoal + FinancialState + investor priorities + constraints/risk evidence |
| 12 | Strategy Version / Primary Strategy | Strategy governance layer | Persist immutable strategy versions and identify the current primary strategy authority | StrategyRun + user selection + finalization/approval + PrimaryStrategyState |
| 13 | Planning Orchestration | Workflow/context coordination layer | Assemble current FinancialState, goals, strategy context, module availability, and workflow readiness for downstream planning | FinancialState snapshot + goal versions + StrategyVersion/context |
| 14 | Multi-Goal Planning | Cross-goal planning layer | Coordinate multiple goals, priorities, shared resources, conflicts, and trade-offs | Active goals + DefinedGoals + FinancialState + current StrategyVersions + constraints |
| 15 | Resource Allocation | Cross-goal allocation engine | Allocate available resources across goals and produce funding outcomes/trade-offs | Goals + priorities + available resources + constraints |
| 16 | Complete Financial Plan | Cross-domain consolidation layer | Consolidate position, goals, funding, strategies, constraints, actions, trade-offs, trajectory, and governance | FinancialState + active goals + StrategyVersions + constraints + allocation + actions |
| 17 | Action Plan | Execution layer | Convert approved strategy into executable actions | Approved current StrategyVersion |
| 18 | Execution / Impact Update | Outcome and state-update layer | Capture decisions/completion and compare projected vs actual impact | Action completion + actual FinancialState snapshot |
| 19 | Replanning | Continuous planning layer | Reassess planning when goals, profile, or financial state changes | Updated FinancialState + revised DefinedGoal/Profile + strategy context |
| 20 | Financial Memory / Investor Diary | User-authored financial context layer | Persist financial notes and decision context so important reasoning/context remains available across planning cycles | DiaryEntry + FinancialDecision |
| 21 | Dashboard / Reports / History | Presentation and historical-review layer | Present consolidated outputs and expose goal/strategy history and reporting views | Canonical downstream outputs + historical records |

## Code-Verified Layer Boundaries

- FinancialState != FinancialHealth != MoneyWheel != Constraints.
- Investor Profile / Risk is a composite decision-context layer. The backend has ProfileEngine/ProfileService, a dedicated RiskProfilerEngine with RiskProfile and the dimensions risk_required, risk_capacity, and risk_tolerance, plus behavioral and identity profile components.
- Behavioral Profile is implemented as an internal component of the profile/risk context through engines/profile/behavioral.py and BehavioralRules; it is not a separate top-level layer.
- Suitability is not a separate completed layer. SuitabilityEngine exists as a rules-ready assessment boundary, but the code does not expose a separate end-to-end suitability planning workflow comparable to the 21 layers.
- Investment Engine is not a separate top-level layer yet. engines/investment/engine.py and its models exist, but the current frontend/backend surface does not establish an independent end-to-end investment-planning layer with its own user workflow/API authority.
- Insurance / Protection is not a separate top-level layer. Insurance has onboarding data/model/API and policy-PDF extraction, but it currently participates as financial input/protection context rather than an independent planning workflow.
- Scenario Planning is part of Strategy Builder / StrategyRun. Strategy scenario UI and backend scenario logic exist, but do not constitute a separate domain layer.
- Goal Feasibility is part of Goal Planner. The frontend has a dedicated feasibility view, while the backend goal engine owns the calculations.
- Reports are part of Dashboard / Reports / History. Goal reports, basket reports, summary reports, and the complete-plan renderer are reporting outputs rather than independent planning layers.
- PlanningUnit is a root planning context/entity, not a user-facing computational layer.
- Strategy techniques/components are internal strategy mechanisms, not separate top-level layers.
- Decision/audit trace is a cross-cutting governance concern around execution/history, not a separate planning layer.

## Responsibility Boundaries

- FinancialState is the authoritative current financial position.
- Financial Health is an assessment of that position.
- MoneyWheel is the diagnostic framework built from canonical financial metrics and coverage rules.
- Constraints are decision controls evaluated from financial evidence and rule definitions.
- Budgeting controls spending limits/variance; it does not replace FinancialState or MoneyWheel.
- Goal Planner defines/version individual goals; Goal Basket groups existing goals and does not replace them.
- StrategyRun records a strategy evaluation run; it is not the same thing as the current StrategyVersion.
- StrategyVersion is immutable strategy configuration; PrimaryStrategyState identifies the current primary strategy authority.
- Planning Orchestration coordinates workflow context; it does not become the owner of the underlying financial or strategy data.
- Multi-Goal Planning coordinates cross-goal decisions; Resource Allocation performs the concrete allocation calculation.
- Complete Financial Plan consolidates domain outputs; it does not own the underlying canonical calculations or strategy identity.
- Action Plan executes an approved current strategy; execution updates the authoritative financial state for the next planning cycle.
- Financial Memory / Investor Diary stores user-authored notes and decision context; it is not an authoritative FinancialState, strategy authority, or calculated financial-history substitute.
- Dashboard / Reports / History presents and reviews canonical outputs; it does not become the owner of those outputs.

## High-Level Data Flow

Financial Memory / Investor Diary is a review/context layer rather than a mandatory computational step, so it is shown as cross-cutting around the planning cycle:

Customer Inputs
    ↓
Financial State
    ↓
Canonical Calculations
    ↓
Financial Health / MoneyWheel / Constraints
    ↓
Investor Profile / Risk + Budgeting
    ↓
Goal Planner
    ↓
Goal Basket (when grouping goals)
    ↓
Strategy Builder / StrategyRun
    ↓
StrategyVersion + Primary Strategy
    ↓
Planning Orchestration
    ↓
Multi-Goal Planning
    ↓
Resource Allocation
    ↓
Complete Financial Plan
    ↓
Action Plan
    ↓
Execution / Actual Outcome
    ↓
Updated Financial State
    ↺

Financial Memory / Investor Diary
    ↕
Planning and review cycles

## Frontend / Backend Implementation Evidence

- Onboarding: frontend onboarding routes cover personal information, family/dependents, income, expenses, assets, insurance, liabilities, and goals.
- Financial State: financial_state API/service/model/engine provide the authoritative current-state path.
- Calculations: engines/calculation/canonical.py and the calculation engine provide canonical measures consumed downstream.
- MoneyWheel: dedicated frontend page plus backend API/service/engine.
- Constraints: dedicated constraint engine with evaluator, aggregator, adapters, and models.
- Profile / Risk: ProfileEngine, ProfileService, /api/profile, engines/risk_profiler/, RiskProfile, and profile history/latest APIs.
- Budgeting: dedicated frontend investor budgeting page and budget persistence/API/types.
- Goal Planner: goal frontend routes, goal API/service/model, and goal engines including target, funding-gap, asset-projection, and specialized calculations.
- Goal Basket: GoalBasket model, service, engine, API, and basket reporting.
- Strategy Builder / StrategyRun: strategy frontend routes plus strategy service/API and strategy engines for applicability, eligibility, composition, comparison, decision, ranking, recommendation, and scenarios.
- Strategy Version / Primary Strategy: StrategyVersion model/service/API plus PrimaryStrategyState and its repository/persistence.
- Planning Orchestration: orchestration frontend/backend context and service/API.
- Multi-Goal Planning: multi-goal planning service plus allocation/rules integration.
- Resource Allocation: ResourceAllocationEngine and allocation result models.
- Complete Financial Plan: FinancialPlanService and summary/report rendering surface.
- Action Plan / Execution: action-plan frontend/API/service/model plus impact engine and completion/update flow.
- Replanning: implemented through goal/profile/financial-state changes feeding downstream recalculation and strategy context.
- Financial Memory / Investor Diary: frontend /investor/diary, backend diary API/service/repository/model/schema, plus DiaryEntry and FinancialDecision.
- Dashboard / Reports / History: dashboard, reports, goal-history, and strategy-history frontend routes with corresponding backend reporting services/APIs.

## Code-Audit Conclusion

Using only the frontend and backend folders as implementation evidence, the current architecture has 21 top-level layers.

No additional candidate was found that satisfies all three conditions for a separate top-level layer:
1. a distinct domain responsibility,
2. a distinct implemented backend capability, and
3. a distinct frontend/end-user workflow or authoritative system surface.

The main candidates that fail this test are Investment Engine, Suitability, Insurance/Protection, Behavioral Profile, Scenario Planning, Goal Feasibility, Reports, PlanningUnit, Strategy Techniques, and Decision/Audit Trace. They are implemented components or sub-capabilities, but not additional top-level layers.

This conclusion is intentionally code-first and does not infer a layer merely from a folder, class, route, or documentation concept in isolation.