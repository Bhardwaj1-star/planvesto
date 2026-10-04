# Strategy → Action Plan

## 1. Feature Scope

Converts the current approved StrategyVersion into executable ActionPlanItems, records user decisions, and on completion records actual FinancialState plus projected-vs-actual impact.

```text
Current StrategyVersion
    ↓
Approval Gate
    ↓
Action Generation
    ↓
ActionPlanItems
    ↓
User Decision / Execution
    ↓
Projected + Actual State
    ↓
Impact Comparison
    ↓
Authoritative FinancialState Update
    ↓
Completion / History
    ↓
Next Planning Cycle
```

Action Plan owns execution planning and action lifecycle. It does not own StrategyVersion identity, canonical financial formulas, or independent FinancialState calculation.

## 2. User / Request Inputs

### Generate

POST `/api/action-plan/actions/generate`

- `planning_unit_id`
- `strategy_version_id`

### Manual creation

POST `/api/action-plan/actions`

- `planning_unit_id`
- `strategy_version_id`
- `title`
- `description`
- `priority`
- `deadline`
- `planned_impact`

### Decision

POST `/api/action-plan/decisions`

- `planning_unit_id`
- `action_id`
- `decision`
- `impact_preview`
- `after_state`

Decisions:

- add
- modify
- delete
- complete
- cancel

### Completion

POST `/api/action-plan/actions/{action_id}/complete`

- `planning_unit_id`
- `action_id`
- `actual_state`
- `completion_preview`

Submitted `actual_state` must carry the current authoritative FinancialState snapshot identity.

## 3. Input Source / Authority Boundary

| Source | Authority |
|---|---|
| Current strategy | Explicitly selected StrategyVersion |
| Goal context | StrategyVersion → Goal / DefinedGoal version |
| Action specification | `backend/rules/action_plan.py` |
| Current FinancialState | FinancialStateService |
| Projected/actual comparison | ActionImpactEngine |
| User action decision | ActionPlan decision lifecycle |

ActionPlanItem is directly bound to `strategy_version_id`. Goal association is inherited through the StrategyVersion.

Latest StrategyRun, ranking, recommendation, or stale StrategyVersion cannot authorize current actions.

## 4. Canonical Rules and Decision Logic

Before action creation/generation, the system validates:

- authenticated Planning Unit ownership
- Goal context
- current StrategyVersion
- exact DefinedGoal binding
- architecture consistency
- approval requirement
- active strategy-library availability

Canonical generated action specifications come from:

`backend/rules/action_plan.py::build_action_specs()`

Generation is deterministic and uses a generation key so repeated requests do not create duplicate actions.

ActionImpactEngine compares projected and actual state. It does not own canonical financial metric formulas.

## 5. Action Generation Contract

```text
Current StrategyVersion
    ↓
Approval validation
    ↓
Strategy / architecture resolution
    ↓
Canonical action specifications
    ↓
Generation key
    ↓
ActionPlanItems
```

Generated actions preserve:

- StrategyVersion lineage
- strategy / technique identity
- implementation parameters
- architecture identity
- generation key
- FinancialState context used for generation
- planned impact

## 6. Lifecycle / State Transitions

Statuses:

- planned
- confirmed
- completed
- cancelled

Decisions:

- add
- modify
- delete
- complete
- cancel

Transition rules:

- add/confirm: planned
- modify: planned/confirmed
- complete: planned/confirmed
- cancel: planned/confirmed
- completed/cancelled actions cannot be deleted

Every decision is persisted as historical ActionDecisionRecord evidence.

## 7. Approval / Decision Gate

Current implementation requires an approval snapshot for action generation/creation.

The current approval path is not fully canonicalized:

- `is_strategy_version_approved()` checks approval-row existence for Planning Unit + StrategyVersion;
- an explicit application approval writer was not established in the audited implementation;
- exact Goal + DefinedGoal version + suitability/context binding is not fully established;
- StrategyEditService can expose `approval_snapshot_required=False` while action generation requires approval.

Target contract:

```text
User Approval
├── Planning Unit
├── Goal
├── exact DefinedGoal ID/version
├── exact StrategyVersion
├── suitability / decision context
└── acknowledgement
    ↓
Action Generation Gate
```

Until implemented, approval existence is a lifecycle dependency, not a complete approval authority contract.

## 8. Planned Impact Contract

A planned action contains the implementation context needed to understand its expected effect.

Projected FinancialState is required before completion.

Planned impact may include:

- generation key
- strategy ID
- StrategyVersion ID
- implementation parameters
- architecture ID
- FinancialState used during generation
- projected FinancialState
- expected action impact

The projection is evidence for comparison; it does not replace the authoritative current FinancialState.

## 9. Completion / Actual-State Contract

```text
Projected State + Actual State
        ↓
ActionImpactEngine.compare()
        ↓
Projected-vs-Actual Variance
        ↓
FinancialStateService.save_actual_state()
        ↓
New authoritative FinancialState snapshot
        ↓
Action actual_impact + history
```

Completion validates:

- Planning Unit
- scope family
- investor context
- current FinancialState snapshot
- StrategyVersion lineage

Stale submitted snapshots are rejected.

The validated completion path is an explicit FinancialState authority update path.

## 10. Impact Contract

ActionImpactEngine compares projected and actual outcomes.

It can produce:

- action impact
- FinancialState impact
- goal impacts
- strategy impact
- financial-health impact
- alternatives
- cause explanation
- variance

It does not redefine savings, DTI, liquidity, emergency coverage, or other canonical financial formulas.

## 11. Output Contract

Action Plan outputs:

### Action execution data

- `action_id`
- `planning_unit_id`
- `strategy_version_id`
- title
- description
- priority
- deadline
- status
- planned impact
- actual impact
- created timestamp

### Lifecycle evidence

- decision records
- before/after context
- timestamps
- historical transition evidence

### Completion evidence

- projected state
- actual state
- FinancialState snapshot lineage
- projected-vs-actual variance
- actual impact

## 12. Ownership Boundary

- API: `backend/api/action_plan.py`
- Schemas: `backend/schemas/action_plan.py`
- Lifecycle/service: `backend/services/action_plan_service.py`
- Generation: `backend/services/strategy_action_generator.py`
- Canonical action rules: `backend/rules/action_plan.py`
- Impact comparison: `backend/engines/action_plan/impact_engine.py`
- Model: `backend/models/action_plan.py`
- Repository: `backend/data/action_plan_repository.py`
- Strategy authority: `backend/data/strategy_repository.py`, StrategyVersion repository/service
- FinancialState authority: `backend/services/financial_state_service.py`
- Frontend contract: `frontend/lib/api/action-plan.ts`

Ownership rule:

```text
StrategyVersion
└── owns finalized strategy implementation

Action Plan
└── owns executable action lifecycle

ActionImpactEngine
└── owns projected-vs-actual comparison

FinancialStateService
└── owns authoritative FinancialState persistence

Canonical calculation layer
└── owns financial mathematics
```

## 13. Downstream Dependencies

Action completion feeds:

- current FinancialState
- impact history
- future planning cycles
- goal progress evidence
- strategy execution evidence

Action state is execution/history evidence. It does not replace StrategyVersion authority.

## 14. Versioning / Replanning Boundary

```text
Old DefinedGoal
    ↓
Old StrategyVersion
    ↓
Old actions
    └── history

New DefinedGoal
    ↓
New StrategyVersion
    ↓
New approval
    ↓
New actions
    └── current
```

Old actions must not silently migrate to a new StrategyVersion.

## 15. Regression Contract

Tests must protect:

### Authority

- stale StrategyVersion cannot create actions;
- current StrategyVersion and Goal/DefinedGoal context are required;
- architecture consistency is enforced.

### Approval

- unapproved versions cannot create/generate actions;
- approval must eventually bind exact Goal + DefinedGoal version + StrategyVersion;
- edited versions require fresh approval where policy requires it.

### Generation

- generation is deterministic;
- duplicate generation keys do not create duplicates;
- StrategyVersion lineage is preserved.

### Lifecycle

- invalid transitions are rejected;
- editable fields remain limited;
- every decision creates historical evidence.

### Completion

- projected state is required;
- actual state is validated;
- scope/ownership is enforced;
- stale snapshot is rejected;
- variance is recorded;
- actual FinancialState is persisted through canonical authority.

## 16. Known Implementation Gaps

1. Approval lifecycle writer and exact-context validation are not fully established.
2. Approval-row existence is weaker than the target approval contract.
3. StrategyEditService approval-required behavior is inconsistent with action-generation gating.
4. Completion authority depends on the validated actual-state path and current-snapshot contract.

## 17. Important Semantic Boundaries

1. StrategyVersion → Action Plan is the valid strategy-to-action lineage.
2. Approval is a gate, not StrategyVersion identity.
3. ActionPlanItem is execution data, not strategy definition.
4. ActionImpactEngine compares states; it does not own financial formulas.
5. Actual FinancialState becomes authoritative through validated completion persistence.
6. Old StrategyVersion actions remain history after revision.
7. Decision history is audit evidence, not current planning authority.
8. Planned impact is not actual impact.
9. Current FinancialState is not an ActionPlanItem snapshot.

## 18. Final Strategy → Action Plan Output

```text
Current Approved StrategyVersion
    ↓
Canonical Action Specifications
    ↓
ActionPlanItems
    ├── strategy_version_id
    ├── architecture
    ├── planned impact
    └── lifecycle status
    ↓
User Decisions
    ↓
Execution
    ↓
Projected + Actual Financial State
    ↓
Impact Comparison
    ├── variance
    ├── goal impact
    ├── strategy impact
    └── financial-health impact
    ↓
Authoritative FinancialState Update
    ↓
Completed Action + Historical Evidence
```

The final output must make clear which StrategyVersion generated the action, what was planned, what happened, what changed financially, and which authoritative FinancialState snapshot resulted.

## 19. Strategy → Action Plan End-to-End Contract

CURRENT SELECTED STRATEGYVERSION
    ↓
APPROVAL GATE
    ↓
STRATEGY ACTION GENERATOR
    ↓
DETERMINISTIC ACTION SPECS
    ↓
ACTIONPLANITEMS
    ↓
USER DECISION / EXECUTION
    ↓
ACTUAL STATE SUBMISSION
    ↓
PROJECTED-VS-ACTUAL COMPARISON
    ↓
FINANCIALSTATE AUTHORITY UPDATE
    ↓
ACTION COMPLETION + HISTORY
    ↓
NEXT PLANNING CYCLE

Scope: Strategy → Action Plan only.