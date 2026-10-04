# Strategy → Action Plan

```text
User
└── Strategy select karta hai
    └── Selected Strategy Version
        └── User approval
            └── Approved Strategy
                └── Action Plan
                    ├── Kya karna hai?
                    ├── Kis strategy ke liye?
                    └── Expected impact kya hai?
                        └── User action complete karta hai
                            └── Actual result
                                └── Financial State update
                                    └── Next planning decision
```


## 1. Feature Scope

Strategy → Action Plan converts the **current approved StrategyVersion** into executable ActionPlanItems, records user decisions, and on completion records actual FinancialState and impact variance.

```text
Current StrategyVersion
        ↓
Approval gate
        ↓
Action generation
        ↓
ActionPlanItem(s)
        ↓
User decision
   ├── add
   ├── modify
   ├── cancel
   ├── delete
   └── complete
        ↓
Actual FinancialState
        ↓
Projected vs Actual comparison
        ↓
FinancialState snapshot update
        ↓
Future planning
```

## 2. Inputs

### Action generation
`POST /api/action-plan/actions/generate`

Inputs: `planning_unit_id`, `strategy_version_id`.

### Manual action creation
`POST /api/action-plan/actions` accepts planning_unit_id, strategy_version_id, title, description, priority, deadline and planned_impact.

Priority is high / medium / low.

### Decision confirmation
`POST /api/action-plan/decisions` accepts planning_unit_id, action_id, decision, impact_preview and after_state.

Decisions: add / modify / delete / complete / cancel.

### Completion
`POST /api/action-plan/actions/{action_id}/complete` accepts planning_unit_id, action_id, actual_state and completion_preview.

The submitted actual state must contain the current FinancialState snapshot ID.

## 3. StrategyVersion Authority

An ActionPlanItem is directly bound to `strategy_version_id`.

Before creation, the API verifies planning-unit ownership, Goal context and that the StrategyVersion is the current selected StrategyVersion for that Goal.

Action Plan must never be generated from latest StrategyRun, ranking, recommendation alone, or a stale StrategyVersion.

## 4. Approval Gate

Current implementation has an approval gate, but the approval lifecycle is **not yet fully canonicalized**.

Action creation and generation require an approval snapshot. `ActionPlanRepository.is_strategy_version_approved()` currently checks existence of a `strategy_approval_snapshots` row for planning unit + StrategyVersion.

The canonical remediation audit identifies a P1 gap: no explicit application approval writer was found; approval is not yet proven to be bound to exact Goal + DefinedGoal version + suitability/context; and StrategyEditService can report `approval_snapshot_required=False` while action generation requires an approval snapshot.

Target approval contract:
- explicit user approval command
- planning unit binding
- Goal binding
- exact DefinedGoal ID/version binding
- exact StrategyVersion binding
- suitability / decision context
- acknowledgement
- cross-record ownership validation

Until implemented, approval is a known lifecycle dependency rather than a fully established canonical workflow.

## 5. Action Generation

`StrategyActionGenerator.generate()` materializes the approved StrategyVersion into deterministic actions.

It validates approval, StrategyVersion existence, planning-unit match, Goal/DefinedGoal context, architecture, current StrategyVersion authority and active strategy-library availability.

It resolves the primary strategy, supporting strategies, techniques and current FinancialState.

Canonical action specifications come from `backend/rules/action_plan.py::build_action_specs()`.

Generated actions are initially planned and contain deterministic generation keys, strategy/version lineage, implementation parameters, architecture ID and the FinancialState used as planned-impact context.

Existing generation keys are skipped, making generation idempotent for the same StrategyVersion.

## 6. ActionPlanItem Contract

Canonical fields:
- action_id
- planning_unit_id
- strategy_version_id
- title
- description
- priority
- deadline
- status
- planned_impact
- actual_impact
- created_at

ActionPlanItem has no direct goal_id. Goal association is resolved through `ActionPlanItem → StrategyVersion → Goal / DefinedGoal version`.

## 7. Action Lifecycle

Statuses: planned / confirmed / completed / cancelled.

Decision history: add / modify / delete / complete / cancel.

Add: only planned actions can be confirmed.
Modify: only planned or confirmed actions can be modified.
Complete: only planned or confirmed actions can be completed.
Cancel: only planned or confirmed actions can be cancelled.
Delete: completed/cancelled actions cannot be deleted.

Editable action fields are title, description, priority, deadline and planned_impact.

Every decision is persisted as ActionDecisionRecord with before_state, after_state, impact_preview, timestamp and historical=true.

## 8. Planned Impact

Generated actions store generation key, strategy ID, StrategyVersion ID, implementation parameters, architecture ID and the FinancialState used when actions were generated.

The action's `planned_impact.financial_state` is the projected-state input used for completion comparison. A projected FinancialState is mandatory before completion.

## 9. Completion and Actual State

Completion validates actual state as canonical FinancialState.

Required context: same planning_unit_id, scope=`family`, investor_id=None.

The submitted `snapshot_id` must equal the currently authoritative FinancialState snapshot. Stale submissions are rejected.

Flow:

```text
Projected FinancialState + Actual FinancialState
        ↓
ActionImpactEngine.compare()
        ↓
Variance analysis
        ↓
FinancialStateService.save_actual_state()
        ↓
FinancialState snapshot
        ↓
ActionPlanItem.actual_impact + ActionDecisionRecord
```

Action completion is therefore an explicit FinancialState authority update path, not merely an audit event.

## 10. Impact Calculation

`ActionImpactEngine` compares projected and actual FinancialState values. It owns comparison/variance analysis, not financial planning metric definitions.

Actual impact stores actual financial state, FinancialState snapshot ID, StrategyVersion ID and variance analysis.

Completion preview separately carries action impact, financial state impact, goal impacts, strategy impact, financial health impact, alternatives and cause explanation.

## 11. Ownership and API Boundary

All Action Plan endpoints authenticate the user.

Ownership is checked at planning-unit, StrategyVersion and action boundaries. Completion additionally verifies the action's StrategyVersion ownership.

## 12. Source / Calculation / Persistence Boundary

| Concern | Authoritative owner |
|---|---|
| Strategy identity/configuration | StrategyVersion |
| Current strategy selection | goal_strategy_selections |
| Action specification policy | rules/action_plan.py |
| Action materialization | StrategyActionGenerator |
| Action lifecycle | ActionPlanService |
| Action persistence | ActionPlanRepository |
| FinancialState authority | FinancialStateService |
| Projected-vs-actual comparison | ActionImpactEngine |
| Decision history | ActionDecisionRecord / repository |

Action Plan must not recalculate or redefine canonical FinancialState metrics.

## 13. Versioning and Replanning

Actions are bound to a specific StrategyVersion.

```text
Old Goal version → Old StrategyVersion → Old actions = history
New Goal version → New StrategyVersion → New approval → New actions = current
```

Old actions must not silently migrate to a new StrategyVersion.

## 14. Code Ownership

- API: `backend/api/action_plan.py`
- Request contracts: `backend/schemas/action_plan.py`
- Action lifecycle: `backend/services/action_plan_service.py`
- Strategy-to-action generation: `backend/services/strategy_action_generator.py`
- Action generation rules: `backend/rules/action_plan.py`
- Impact comparison: `backend/engines/action_plan/impact_engine.py`
- Action model: `backend/models/action_plan.py`
- Action persistence: `backend/data/action_plan_repository.py`
- StrategyVersion authority: `backend/data/strategy_repository.py` + `backend/data/strategy_version_repository.py`
- FinancialState authority: `backend/services/financial_state_service.py`
- Frontend contract: `frontend/lib/api/action-plan.ts`

## 15. Regression / Test Contract

### Strategy authority
- stale StrategyVersion cannot create actions
- action generation requires current StrategyVersion
- Goal/DefinedGoal context must exist
- architecture is required for generated actions

### Approval
- unapproved StrategyVersion cannot create/generate actions
- approval must eventually be tested against exact Goal + DefinedGoal version + StrategyVersion + suitability context
- edited StrategyVersion requires fresh approval where lifecycle policy requires it

### Generation
- generation is deterministic
- duplicate generation keys do not create duplicate actions
- generated actions contain strategy/version/architecture lineage

### Lifecycle
- invalid status transitions are rejected
- editable fields are limited
- every decision creates historical evidence

### Completion
- projected state is required
- actual state is validated as FinancialState
- planning-unit/scope/investor ownership is enforced
- stale snapshot is rejected
- projected vs actual variance is recorded
- actual FinancialState is persisted through the canonical FinancialState authority path

## 16. Important Boundaries

1. StrategyVersion → Action Plan is the valid strategy-to-action lineage.
2. Approval is a gate, not a substitute for StrategyVersion authority.
3. ActionPlanItem is execution data, not strategy definition.
4. ActionImpactEngine compares states; it does not own financial metric formulas.
5. Actual FinancialState becomes authoritative through validated completion persistence.
6. Old StrategyVersion actions are history after goal/strategy revision.
7. Action decision history is audit evidence, not current planning authority.

## 17. End-to-End Contract

```text
CURRENT SELECTED STRATEGY VERSION
        ↓
APPROVAL GATE
        ↓
STRATEGY ACTION GENERATOR
        ↓
DETERMINISTIC ACTION SPECS
        ↓
ACTION PLAN ITEMS
        ↓
USER DECISION
        ↓
EXECUTION
        ↓
ACTUAL STATE SUBMISSION
        ↓
PROJECTED vs ACTUAL VARIANCE
        ↓
FINANCIAL STATE AUTHORITY UPDATE
        ↓
ACTION COMPLETION + HISTORY
        ↓
NEXT PLANNING CYCLE
```

## 18. Known P1 Gap

Approval lifecycle is the main unresolved boundary in this feature.

Current code has an approval snapshot read/gate, but the canonical write/approval command and exact-context validation are not established. This must be resolved before the Action Plan workflow can be considered fully canonical.