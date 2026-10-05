# Planvesto Financial Planning Layer Map

This document defines the current domain/layer boundaries for Planvesto's financial-planning system. It is based on the implemented onboarding, FinancialState, MoneyWheel, constraints, goal, strategy, multi-goal, action-plan, replanning, and reporting flows.

## Layer Map

| # | Layer | What it is | Purpose | Primary data source |
|---|---|---|---|---|
| 1 | Onboarding / Financial Inputs | Customer source-input layer | Collect the customer's financial picture | Personal information, family/dependents, income, expenses, assets, insurance, liabilities, goals |
| 2 | Financial State | Authoritative current financial-state aggregate | Represent the customer's current financial position | Persisted Planning Unit financial records from onboarding |
| 3 | Financial Calculations / Measures | Canonical calculation layer | Derive standardized financial metrics from the current state | Current FinancialState |
| 4 | Financial Health | Financial-condition assessment layer | Assess financial strengths, weaknesses, risks, and conditions | Current FinancialState + canonical metrics |
| 5 | MoneyWheel | Financial diagnostic framework | Measure financial health through canonical ratios and coverage rules | Current FinancialState + canonical calculation layer |
| 6 | Constraints / Rules | Decision-control layer | Identify financial limits, warnings, and hard constraints | FinancialState + canonical metrics + rule/threshold definitions |
| 7 | Investor Profile / Risk | Customer suitability and preference layer | Capture risk information, preferences, priorities, and constraints for decisions | Investor profile + risk evidence + priorities |
| 8 | Goal Planner | Individual-goal planning layer | Define goals, calculate requirements, and evaluate feasibility | Customer goals + DefinedGoal inputs + FinancialState + mapped assets |
| 9 | Strategy Builder | Strategy decision layer | Filter, compare, evaluate, rank, and recommend strategies/scenarios for a goal | Current DefinedGoal + FinancialState + investor priorities + constraints/risk evidence |
| 10 | Strategy Version / Approval | Strategy governance layer | Turn a selected/finalized strategy into an authoritative current strategy | Strategy Builder output + user selection + implementation preview/finalization + approval |
| 11 | Multi-Goal Planning | Cross-goal planning layer | Allocate shared resources across goals and resolve priorities/trade-offs | Active goals + DefinedGoals + FinancialState + current StrategyVersions + constraints |
| 12 | Complete Financial Plan | Cross-domain consolidation layer | Consolidate position, goals, funding, strategies, constraints, actions, trade-offs, trajectory, and governance | FinancialState + active goals + current StrategyVersions + constraints + funding/allocation + actions |
| 13 | Action Plan | Execution layer | Convert approved strategy into executable actions | Approved current StrategyVersion |
| 14 | Execution / Impact Update | Outcome and state-update layer | Capture decisions/completion and compare projected vs actual impact | Action completion + actual FinancialState snapshot |
| 15 | Replanning | Continuous planning layer | Reassess planning when goals, profile, or financial state changes | Updated FinancialState + revised DefinedGoal/Profile + strategy context |
| 16 | Dashboard / Reports | Presentation/reporting layer | Present consolidated financial position, goals, health, strategies, constraints, trajectory, and actions | Canonical downstream outputs |

## Responsibility Boundaries

The following concepts are intentionally distinct:

- **FinancialState != FinancialHealth != MoneyWheel != Constraints**
- FinancialState is the authoritative current financial position.
- Financial Health is an assessment of that position.
- MoneyWheel is the diagnostic framework built from canonical financial metrics and coverage rules.
- Constraints are decision controls evaluated from financial evidence and rule definitions.
- Strategy Builder consumes these contexts; it does not own the canonical FinancialState.
- Complete Financial Plan consolidates domain outputs; it does not own the underlying canonical calculations or strategy identity.

## High-Level Data Flow

```text
Customer Inputs
    ↓
Financial State
    ↓
Canonical Calculations
    ↓
Financial Health / MoneyWheel / Constraints
    ↓
Goal Planner + Investor Profile / Risk
    ↓
Strategy Builder
    ↓
StrategyVersion + Approval
    ↓
Multi-Goal Planning
    ↓
Complete Financial Plan
    ↓
Action Plan
    ↓
Execution / Actual Outcome
    ↓
Updated Financial State
    ↺
```

## Implementation Note

The architecture intends canonical calculations and centralized constraint evaluation. Current repository audits identify duplicated constraint thresholds/calculations in some areas (including the constraint evaluator/rules and FinancialPlanService), so this document describes the intended domain boundaries rather than claiming that every implementation is already a single-source-of-truth.
