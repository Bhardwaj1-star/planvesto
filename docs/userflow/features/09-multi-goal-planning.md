# Multi-Goal Planning

## 1. Feature Scope

Multi-Goal Planning evaluates multiple current DefinedGoals together, considers priority and funding/feasibility evidence, and produces an allocation/planning view of competing goals.

```text
Multiple Current Goals
    ↓
Goal priority / funding / feasibility
    ↓
Available resources
    ↓
Goal competition / trade-offs
    ↓
Allocation / planning evaluation
    ↓
Multi-goal plan
```

The feature coordinates multiple goals. It does not redefine individual goal calculation or canonical financial formulas.

## 2. User / Request Inputs

Multi-goal planning consumes:

- Planning Unit
- current DefinedGoals
- goal priority
- goal funding position
- goal feasibility
- current FinancialState / available resources
- allocation/planning context

Goal identity and version come from the current DefinedGoal lifecycle.

## 3. Input Source / Authority Boundary

| Input | Authority |
|---|---|
| Goal identity/version | DefinedGoal |
| Goal funding | Goal Planner |
| Goal feasibility | Goal Planner / goal service |
| FinancialState | FinancialStateService |
| Priority normalization | canonical goal priority rules |
| Allocation status | allocation/planning layer |
| Strategy implementation | selected StrategyVersion |

Multi-goal planning consumes these outputs; it must not create competing definitions.

## 4. Priority Contract

Goal priority is canonicalized through the canonical goal-priority authority.

Priority is a planning decision input.

It is distinct from:

- strategy eligibility
- funding status
- financial ratio classification
- investor safety/liquidity/growth/flexibility preferences

## 5. Funding / Feasibility Vocabulary

Multi-goal planning must preserve the distinction between:

### Goal funding status

- Shortfall
- On Track
- Overfunded

### Allocation funding status

- fully_funded
- partially_funded
- unfunded
- within_surplus
- surplus_shortfall
- requires_review

### Goal feasibility

Goal-level feasibility remains separate from allocation funding status.

These vocabularies must not be merged simply because they describe resource pressure.

## 6. Allocation / Trade-off Logic

```text
Current Goals
    ↓
Priority + Funding + Feasibility
    +
Available Resources
    ↓
Goal Competition
    ↓
Allocation Evaluation
    ↓
Trade-offs
    ├── fund
    ├── partially fund
    ├── defer / constrain
    └── review
```

The resulting plan explains how available resources are distributed across competing goals.

## 7. Strategy Boundary

Multi-goal planning may consume current StrategyVersions as planning context.

It must not derive current strategy from:

- latest StrategyRun
- ranking alone
- recommendation alone
- `is_latest`
- stale StrategyVersion

Current strategy authority remains explicit StrategyVersion selection.

## 8. Output Contract

A multi-goal result should communicate:

- goals considered
- current goal versions
- priority
- funding position
- feasibility
- available resources
- allocation
- trade-offs
- constrained/deferred goals where applicable
- strategy context where available

The exact allocation output vocabulary remains owned by the allocation/planning layer.

## 9. Ownership Boundary

- Multi-goal orchestration: `backend/services/multi_goal_planning_service.py`
- Goal priority: `backend/rules/goals.py` / canonical priority authority
- Goal planning/funding: Goal Planner services/engines
- FinancialState: `backend/services/financial_state_service.py`
- Allocation: `backend/engines/allocation/engine.py`
- Strategy authority: `backend/data/strategy_repository.py`
- Frontend strategy/multi-goal API contracts: current frontend API modules

## 10. Downstream Dependencies

Multi-goal planning feeds:

- dashboard / reports
- basket/multi-goal views
- planning decisions
- strategy context where applicable

It does not replace the individual Goal Planner or Strategy Builder authorities.

## 11. Versioning / Replanning Boundary

A revised DefinedGoal changes the goal version consumed by multi-goal planning.

Historical goal/strategy/action state remains history.

A new current plan must consume the new current DefinedGoal and valid current StrategyVersion.

## 12. Regression Contract

Tests must protect:

- current DefinedGoal version usage;
- canonical priority;
- distinct funding vocabularies;
- FinancialState authority;
- explicit StrategyVersion authority;
- allocation output consistency;
- historical versions not silently becoming current.

## 13. Known Implementation Notes / Gaps

1. Allocation funding vocabulary is distinct from Goal Planner funding vocabulary.
2. Feasibility and allocation status remain separate semantic layers.
3. Interactive trade-off negotiation is described in broader decision documentation, but the solver behavior should not be claimed as implemented unless code supports it.
4. Multi-goal orchestration must remain aligned with current StrategyVersion authority.

## 14. Important Semantic Boundaries

1. Multi-goal plan ≠ individual Goal definition.
2. Allocation status ≠ goal funding status.
3. Allocation status ≠ feasibility.
4. Goal priority ≠ investor priority.
5. Multi-goal evaluation ≠ StrategyVersion authority.
6. Historical goal version ≠ current goal version.

## 15. Final Multi-Goal Planning Output

```text
Current DefinedGoals
    ↓
Priority + Funding + Feasibility
    ↓
Available Financial Resources
    ↓
Allocation / Competition Evaluation
    ↓
Multi-Goal Plan
    ├── allocation
    ├── trade-offs
    ├── constrained/deferred goals
    └── current strategy context
```

## 16. Multi-Goal Planning End-to-End Contract

CURRENT DEFINEDGOALS
    ↓
CANONICAL PRIORITY
    ↓
FUNDING / FEASIBILITY
    ↓
CURRENT FINANCIALSTATE
    ↓
RESOURCE / ALLOCATION EVALUATION
    ↓
GOAL COMPETITION / TRADE-OFFS
    ↓
MULTI-GOAL PLAN
    ↓
DASHBOARD / REPORTING / DOWNSTREAM PLANNING

Scope: Multi-Goal Planning only.