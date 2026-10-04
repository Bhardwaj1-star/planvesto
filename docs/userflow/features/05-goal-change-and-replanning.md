# Goal Change & Replanning

## 1. Feature Scope

Goal Change & Replanning defines what happens when an existing Goal changes materially.

```text
User
└── Existing goal change karta hai
    └── Goal ka naya version
        └── Purani strategy current nahi rehti
            └── System dobara check karta hai
                ├── Funding
                ├── Feasibility
                └── Strategy suitability
                    └── New Strategy Version
                        └── New Approval
                            └── New Action Plan
                                ├── New plan = Current
                                └── Old plan = History
```

The feature owns the revision boundary between the current DefinedGoal and downstream planning. It does not mutate historical strategy/action records into the new revision.

## 2. User / Request Inputs

A goal revision begins from an existing Goal and a new goal input.

Relevant persisted goal inputs include:

- goal type / name
- today cost
- target month/year
- inflation
- priority
- flexibility
- status
- asset mappings
- dynamic details
- specialized data

The exact fields that constitute a material revision are a current implementation boundary and must not be inferred beyond the repository's explicit material-change logic.

## 3. Authority Boundary

```text
Goal
  ↓
DefinedGoal vN
  ↓
Material-change detection
  ↓
DefinedGoal vN+1
  ↓
Strategy re-evaluation
  ↓
New StrategyVersion
```

Goal persistence/versioning is owned by GoalService/GoalRepository.

Current strategy authority is owned by explicit StrategyVersion selection, not by the latest StrategyRun.

Historical versions remain history.

## 4. Material Change / Versioning Rules

Current repository material-change detection checks:

- today_cost
- target_month
- target_year
- mapped asset allocation type/value
- dynamic_details

GoalService also considers current status, priority and flexibility when deciding whether the existing latest DefinedGoal can be reused.

The current material-change implementation does not visibly include every persisted field, including:

- inflation_rate
- asset expected_return
- asset return_frequency
- specialized_data
- other persisted preference fields

This is an implementation gap. The feature contract must not silently claim that every field already creates a new version.

## 5. Revision Lifecycle

```text
Current DefinedGoal v1
    ↓
User changes goal
    ↓
Validate / canonicalize / calculate
    ↓
Material-change decision
    ├── No material change
    │   └── current DefinedGoal may be reused
    │
    └── Material change
        ↓
    New DefinedGoal v2
        ↓
    Re-evaluate strategy
        ↓
    New StrategyRun evaluation context
        ↓
    New StrategyVersion
        ↓
    Explicit new selection
        ↓
    New approval lifecycle
        ↓
    New Action Plan
```

StrategyRun can be used for re-evaluation provenance. It is not the final current strategy authority.

## 6. Strategy Invalidation Boundary

A StrategyVersion bound to an old DefinedGoal version must not remain current after a material goal revision.

The explicit `goal_strategy_selections` binding enforces current Goal + exact DefinedGoal ID/version consistency.

Therefore:

```text
DefinedGoal v1
    ↓
StrategyVersion v1
    ↓
v1 current before revision

DefinedGoal v2
    ↓
v1 binding no longer matches
    ↓
v1 becomes historical
    ↓
new StrategyVersion required
```

Old StrategyRun records also remain evaluation history.

## 7. Funding / Feasibility / Suitability Re-check

A goal revision can change:

- future target
- duration
- funding gap
- required contribution
- feasibility
- strategy eligibility
- strategy ranking
- implementation assumptions

Therefore the system must re-evaluate downstream decision evidence against the new DefinedGoal.

These are separate concepts:

- funding status belongs to Goal Planner;
- feasibility is goal-level planning evidence;
- strategy eligibility belongs to Strategy Builder;
- allocation funding statuses remain distinct from goal funding status.

## 8. New StrategyVersion Boundary

A revised goal requires:

1. new strategy evaluation;
2. new selected strategy/scenario;
3. new finalized StrategyVersion;
4. explicit current selection;
5. approval lifecycle for the new version;
6. new downstream Action Plan.

The old StrategyVersion remains immutable history.

## 9. Action Plan Boundary

Old actions belong to the old StrategyVersion and therefore remain historical.

```text
Old DefinedGoal
    ↓
Old StrategyVersion
    ↓
Old ActionPlanItems
    └── History

New DefinedGoal
    ↓
New StrategyVersion
    ↓
New ActionPlanItems
    └── Current
```

No silent migration of old actions to the new version is allowed.

## 10. Output Contract

A successful material revision produces:

- new DefinedGoal version
- new funding/feasibility evaluation
- new strategy evaluation context
- new StrategyVersion lifecycle
- new explicit current selection
- new approval lifecycle
- new Action Plan

Historical outputs remain queryable as history.

## 11. Ownership Boundary

- Goal API: `backend/api/goals.py`
- Goal persistence/versioning: `backend/data/goal_repository.py`
- Goal lifecycle: `backend/services/goal_service.py`
- Goal calculations: `backend/engines/goal/*`
- Strategy re-evaluation: `backend/services/strategy_service.py`
- Strategy authority: `backend/data/strategy_repository.py`
- StrategyVersion lifecycle: `backend/services/strategy_version_service.py`
- Action Plan lifecycle: `backend/services/action_plan_service.py`
- FinancialState authority: `backend/services/financial_state_service.py`
- Frontend goal contract: `frontend/lib/api/goals.ts`

## 12. Regression Contract

Tests must protect:

- historical DefinedGoal versions remain immutable;
- material revisions create new versions;
- non-material updates do not unnecessarily create versions;
- old StrategyVersion cannot become current for a new DefinedGoal version;
- explicit current selection is invalidated by exact DefinedGoal binding;
- new strategy evaluation is required after material revision;
- old actions remain history;
- new Action Plan binds to new StrategyVersion.

## 13. Known Implementation Gaps

1. Material-change detection does not visibly cover every persisted goal field.
2. Strategy re-evaluation currently uses the previous StrategyRun as evaluation context; this must not become current strategy authority.
3. Approval lifecycle is a separate incomplete canonicalization boundary.
4. Exact downstream invalidation must remain tied to DefinedGoal ID/version, not merely Goal ID.

## 14. Important Semantic Boundaries

1. Goal ≠ DefinedGoal version.
2. DefinedGoal revision ≠ StrategyVersion revision.
3. StrategyRun re-evaluation ≠ current strategy authority.
4. Old StrategyVersion ≠ current StrategyVersion.
5. Old Action Plan ≠ new Action Plan.
6. Funding status ≠ strategy eligibility.
7. Goal revision ≠ deletion of history.
8. Material change detection ≠ arbitrary field change unless policy says so.

## 15. Final Goal Change & Replanning Output

```text
Existing Goal
    ↓
Material Change Detection
    ↓
New DefinedGoal Version
    ↓
Funding / Feasibility Recalculation
    ↓
Strategy Re-evaluation
    ↓
New StrategyVersion
    ↓
Explicit Selection
    ↓
New Approval
    ↓
New Action Plan
    ↓
Current Planning State

Old DefinedGoal / StrategyVersion / Actions
    └── Historical State
```

## 16. Goal Change & Replanning End-to-End Contract

CURRENT DEFINEDGOAL
    ↓
USER REVISION
    ↓
VALIDATION / CANONICALIZATION / CALCULATION
    ↓
MATERIAL-CHANGE DECISION
    ↓
NEW DEFINEDGOAL VERSION
    ↓
FUNDING / FEASIBILITY RECHECK
    ↓
STRATEGY RE-EVALUATION
    ↓
NEW STRATEGYVERSION
    ↓
EXPLICIT CURRENT SELECTION
    ↓
APPROVAL
    ↓
NEW ACTION PLAN

OLD VERSIONS / STRATEGIES / ACTIONS → HISTORY

Scope: Goal Change & Replanning only.