# Dashboard & Reports

## 1. Feature Scope

Dashboard & Reports presents the current financial picture and current planning decisions using authoritative FinancialState, current DefinedGoals, current StrategyVersions, Action Plan evidence and multi-goal/basket outputs.

```text
Current FinancialState
    +
Current DefinedGoals
    +
Current StrategyVersions
    +
Action Plan / Execution Evidence
    +
Multi-Goal / Basket Context
    ↓
Dashboard / Reports
    ↓
Current Financial Picture + Current Plan
```

Reporting is a consumer of domain authorities. It must not become a competing source of current financial or strategy truth.

## 2. User / Request Inputs

Dashboard/report views consume contextual identifiers such as:

- Planning Unit
- Goal
- current DefinedGoal version
- selected/current StrategyVersion
- report type / view context
- action-plan and multi-goal context where applicable

The report layer should resolve current state through authoritative services rather than arbitrary historical records.

## 3. Input Source / Authority Boundary

| Data | Authority |
|---|---|
| Current FinancialState | FinancialStateService |
| Goal definition/progress context | current DefinedGoal |
| Current strategy | explicit StrategyVersion selection |
| Action lifecycle | ActionPlan |
| Multi-goal allocation | Multi-goal/allocation planning |
| Financial ratios/rules | canonical calculation + MoneyWheel layers |
| Historical evidence | versioned/history records |

A report must not infer current strategy from latest StrategyRun.

## 4. Current-State Contract

```text
Dashboard / Report
    ↓
Current FinancialState
    +
Current DefinedGoal
    +
Current StrategyVersion
```

Current means:

- valid Planning Unit ownership
- current FinancialState authority
- current DefinedGoal version
- explicitly selected StrategyVersion bound to that goal version

Historical versions can be displayed as history but cannot silently replace current state.

## 5. Financial Health Output

Reports can present:

- income/expense context
- surplus
- assets/liabilities
- net worth
- liquidity
- MoneyWheel ratios/rules
- diagnostics / constraints

These values must come from their canonical owners.

Reporting code must not reimplement financial formulas.

## 6. Goal Output

For each current goal, reporting can present:

- canonical goal identity
- target
- duration
- future target
- funding gap
- funding status
- required contribution
- feasibility
- current DefinedGoal version

Goal calculations remain owned by Goal Planner.

## 7. Strategy Output

Current strategy reporting is bound to:

```text
Goal
  ↓
goal_strategy_selections
  ↓
StrategyVersion
```

A report can show:

- selected strategy
- architecture
- implementation context
- decision snapshot
- strategy status
- strategy provenance

It must not treat recommendation/ranking/latest StrategyRun as current authority.

## 8. Action Plan Output

Reports can show:

- current ActionPlanItems
- action status
- planned impact
- actual impact
- completion evidence
- projected-vs-actual variance
- FinancialState snapshot lineage

Action history remains historical evidence.

## 9. Multi-Goal / Basket Output

Where available, reports can present:

- goals considered
- priorities
- funding/feasibility
- allocations
- trade-offs
- constrained/deferred goals
- strategy context

Allocation vocabulary remains distinct from Goal Planner funding vocabulary.

## 10. Report Lifecycle / Versioning

```text
Current Domain Authorities
    ↓
Report / Dashboard Read
    ↓
Rendered Current View

Historical
    ├── old FinancialState snapshots
    ├── old DefinedGoals
    ├── old StrategyVersions
    └── old ActionPlan evidence
        ↓
Historical Reporting
```

A new DefinedGoal version changes current goal context. A new current StrategyVersion changes current strategy context. Historical records remain available for audit/history.

## 11. Output Contract

Dashboard/report output should distinguish:

### Current state

- current FinancialState
- current DefinedGoal(s)
- current StrategyVersion(s)
- current Action Plan state

### Historical evidence

- prior FinancialState snapshots
- prior DefinedGoal versions
- prior StrategyRuns
- prior StrategyVersions
- completed/cancelled actions
- decision history

### Decision evidence

- MoneyWheel classifications
- constraints
- strategy decision snapshot
- goal funding/feasibility
- multi-goal trade-offs

## 12. Ownership Boundary

- Dashboard/report API/services: current dashboard/report service modules
- FinancialState: `backend/services/financial_state_service.py`
- Goal: Goal Planner / DefinedGoal services
- Strategy current authority: `backend/data/strategy_repository.py`
- StrategyVersion: `backend/services/strategy_version_service.py`
- Action Plan: `backend/services/action_plan_service.py`
- MoneyWheel: `backend/api/moneywheel.py`, MoneyWheel engine/rules
- Summary/report engines: report/summary engine modules
- Frontend contracts: dashboard/report frontend API modules

Where an exact endpoint/service is not established by the feature source, this document does not invent one.

## 13. Downstream Dependencies

Dashboard & Reports is primarily a terminal read/communication layer.

It can feed:

- user decision review
- planning navigation
- historical/audit review
- next action selection

It must not become an upstream authority for FinancialState, Goal, StrategyVersion or ActionPlan.

## 14. Regression Contract

Tests must protect:

- current FinancialState authority;
- current DefinedGoal version;
- explicit StrategyVersion selection;
- no latest-StrategyRun current authority;
- canonical financial outputs;
- goal funding/feasibility semantics;
- action lineage;
- historical/current separation;
- ownership boundaries.

## 15. Known Implementation Notes / Gaps

1. Dashboard/report code must be checked for any remaining latest-StrategyRun or historical-record shortcuts.
2. Report calculation duplication must remain prohibited.
3. Current-vs-history semantics must remain explicit when new Goal/StrategyVersion revisions occur.
4. Where report-specific projections exist, they must identify their source/version rather than masquerading as current FinancialState.

## 16. Important Semantic Boundaries

1. Report ≠ domain authority.
2. Dashboard ≠ FinancialStateService.
3. Recommendation ≠ current strategy.
4. Historical StrategyRun ≠ current StrategyVersion.
5. Goal report ≠ Goal Planner authority.
6. Action history ≠ current action state.
7. Allocation status ≠ goal funding status.
8. Current view ≠ historical snapshot.

## 17. Final Dashboard & Reports Output

```text
Current FinancialState
    +
Current DefinedGoals
    +
Current StrategyVersions
    +
Current Action Plan
    +
Multi-Goal / Basket Context
    ↓
Dashboard / Reports
    ├── Financial Health
    ├── Goals / Progress
    ├── Current Strategy
    ├── Action Plan
    ├── Multi-Goal View
    └── Historical / Decision Evidence
```

The final output must make clear which records are current, which are historical, and which domain authority produced each decision-relevant value.

## 18. Dashboard & Reports End-to-End Contract

CURRENT FINANCIALSTATE
    ↓
CURRENT DEFINEDGOALS
    ↓
CURRENT STRATEGYVERSION(S)
    ↓
ACTION PLAN / EXECUTION EVIDENCE
    ↓
MULTI-GOAL / BASKET CONTEXT
    ↓
DASHBOARD / REPORTS
    ↓
CURRENT FINANCIAL PICTURE + CURRENT PLAN + HISTORY

Scope: Dashboard & Reports only.