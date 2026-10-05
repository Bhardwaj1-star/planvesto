# Planvesto Financial Planning Layer Map

This document defines the current domain/layer boundaries for Planvesto's financial-planning system. It is based on the implemented onboarding, FinancialState, budgeting, MoneyWheel, constraints, goal, goal-basket, strategy, planning orchestration, multi-goal allocation, action-plan, replanning, financial memory, and reporting flows.

## Layer Map

| # | Layer | What it is | Purpose | Primary data source |
|---|---|---|---|---|
| 1 | Onboarding / Financial Inputs | Customer source-input layer | Collect the customer's financial picture | Personal information, family/dependents, income, expenses, assets, insurance, liabilities, goals |
| 2 | Financial State | Authoritative current financial-state aggregate | Represent the customer's current financial position | Persisted Planning Unit financial records |
| 3 | Financial Calculations / Measures | Canonical calculation layer | Derive standardized financial metrics from the current state | Current FinancialState |
| 4 | Financial Health | Financial-condition assessment layer | Assess financial strengths, weaknesses, risks, and conditions | Current FinancialState + canonical metrics |
| 5 | MoneyWheel | Financial diagnostic framework | Measure financial health through canonical ratios and coverage rules | Current FinancialState + canonical calculation layer |
| 6 | Constraints / Rules | Decision-control layer | Identify financial limits, warnings, and hard constraints | FinancialState + canonical metrics + rule/threshold definitions |
| 7 | Investor Profile / Risk | Customer suitability and preference layer | Capture risk information, preferences, priorities, and constraints for decisions | Investor profile + risk evidence + priorities |
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

## Responsibility Boundaries

The following concepts are intentionally distinct:

- **FinancialState != FinancialHealth != MoneyWheel != Constraints**
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
- **Financial Memory / Investor Diary stores user-authored notes and decision context; it is not an authoritative FinancialState, strategy authority, or calculated financial-history substitute.**
- Dashboard / Reports / History presents and reviews canonical outputs; it does not become the owner of those outputs.

## High-Level Data Flow

The Financial Memory / Investor Diary is a review/context layer rather than a mandatory computational step, so it is shown as cross-cutting around the planning cycle:

```text
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
```

## Implementation Note

The following are confirmed implemented code components represented in this map:

- **Budgeting:** investor budgeting UI, budget API/types, and `budget_limits` persistence.
- **Goal Basket:** GoalBasket model, GoalBasketService, GoalBasketEngine, dedicated API, and basket-report flow.
- **StrategyRun:** persistent strategy evaluation/run entity and strategy API.
- **PrimaryStrategyState:** canonical current-primary strategy pointer and repository/API surface.
- **Planning Orchestration:** PlanningOrchestrationService, PlanningOrchestrationContext, and orchestration API.
- **Resource Allocation:** ResourceAllocationEngine and ConsolidatedAllocationResult.
- **Financial Memory / Investor Diary:** `/investor/diary` UI, `backend/api/diary.py`, DiaryService, frontend diary API/types, DiaryEntry, and FinancialDecision; the UI explicitly labels this capability as a "Memory Layer".

The architecture intends canonical calculations and centralized constraint evaluation. Current repository audits identify duplicated constraint thresholds/calculations in some areas (including the constraint evaluator/rules and FinancialPlanService), so this document describes the current domain boundaries while explicitly acknowledging those remaining implementation conflicts.

Behavioral Profile remains intentionally outside this layer map as a separate layer: documentation defines the concept, but the repository audit did not find a dedicated canonical BehavioralProfile implementation comparable to the implemented layers above.
