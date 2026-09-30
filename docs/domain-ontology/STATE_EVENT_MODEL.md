# State & Event Model: Lifecycle, Transitions & Action Feedback Loop

> **Document Status:** Authoritative Audit & Target Architecture  
> **Source Primary Reference:** `docs/domain-ontology/CODE_FIRST_DOMAIN_ONTOLOGY.md`  
> **Audit Scope:** `backend/models/financial_state.py`, `backend/engines/financial_state/`, `backend/services/financial_state_service.py`, `backend/data/financial_state_repository.py`, `backend/services/action_plan_service.py`, `backend/services/strategy_edit_service.py`, `backend/models/action_plan.py`  
> **Core Principle:** Code-first truth. No architecture invented. Verified against exact source files and line evidence.

---

## 1. Domain State Lifecycle & Invariants

The Planvesto backend operates on immutable, versioned domain snapshots to ensure auditability, historical reproducibility, and clean transaction boundaries.

```text
 ┌──────────────────────┐
 │ Raw Financial Data   │ (incomes, expenses, assets, liabilities, insurance)
 └──────────┬───────────┘
            │ Event: RAW_FINANCIAL_DATA_MUTATED
            ▼
 ┌──────────────────────┐
 │ FinancialStateEngine │ (engines/financial_state/engine.py:build)
 └──────────┬───────────┘
            │ Emits Immutable Aggregate
            ▼
 ┌──────────────────────┐
 │ FinancialState       │ (models/financial_state.py)
 └──────────┬───────────┘
            │ Saved via FinancialStateSnapshotRepository
            ▼
 ┌──────────────────────┐
 │ Snapshot Store       │ (financial_state_snapshots table)
 └──────────┬───────────┘
            │
            ├──────────────────────┬──────────────────────┐
            ▼                      ▼                      ▼
  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐
  │ Moneywheel Engine │  │ Goal Engine       │  │ Strategy Engine   │
  └───────────────────┘  └───────────────────┘  └─────────┬─────────┘
                                                          │
                                                          │ Strategy Selected
                                                          ▼
                                                ┌───────────────────┐
                                                │ StrategyVersion   │
                                                └─────────┬─────────┘
                                                          │
                                                          │ Generates Actions
                                                          ▼
                                                ┌───────────────────┐
                                                │ ActionPlanItem    │
                                                └─────────┬─────────┘
                                                          │
                                                          │ Action Completed
                                                          ▼
                                                ┌───────────────────┐
                                                │ Actual State Gap! │
                                                └───────────────────┘
```

---

## 2. Domain State Entities & Immutability Matrix

| State Aggregate | Storage Mechanism & Table | Immutability / Versioning Model | Exact Code Evidence | Lifecycle Status |
|---|---|---|---|---|
| **`FinancialState`** | `financial_state_snapshots` (Supabase / In-Memory Mock) | **Append-only historical snapshots**. Every calculation builds a full snapshot with timestamp and UUID. | [`models/financial_state.py:11`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/models/financial_state.py#L11)<br>[`data/financial_state_repository.py:12-45`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/data/financial_state_repository.py#L12-L45) | `CANONICAL` |
| **`DefinedGoal`** | `defined_goals` | **Explicit integer versioning** (`version: int`, `is_latest: bool`). Editing a goal creates `version + 1` and marks previous as `is_latest = False`. | [`models/defined_goal.py:20-47`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/models/defined_goal.py#L20-L47)<br>[`data/goal_repository.py:15-60`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/data/goal_repository.py#L15-L60) | `CANONICAL` |
| **`StrategyRun`** | `strategy_runs` | **Versioned run container** (`run_version: int`, `is_latest: bool`). Tracks all candidate architectures, rankings, recommendation, and selection. | [`models/strategy.py:170-196`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/models/strategy.py#L170-L196)<br>[`data/strategy_repository.py:10-70`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/data/strategy_repository.py#L10-L70) | `CANONICAL` |
| **`StrategyVersion`** | `strategy_versions` | **Immutable configuration versioning** (`version: int`, `parent_version: int \| None`, `status: StrategyVersionStatus`). | [`models/strategy_version.py:10-24`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/models/strategy_version.py#L10-L24)<br>[`data/strategy_version_repository.py:10-60`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/data/strategy_version_repository.py#L10-L60) | `CANONICAL` |
| **`PrimaryStrategyState`** | `primary_strategy_state` | **Singleton state pointer per planning unit**. Tracks active primary strategy version and archives previous. | [`models/primary_strategy_state.py:7-20`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/models/primary_strategy_state.py#L7-L20)<br>[`data/primary_strategy_repository.py:10-50`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/data/primary_strategy_repository.py#L10-L50) | `CANONICAL` |
| **`ActionPlanItem`** | `action_plan_items` | **State machine transition entity** (`status: ActionStatus`). Status transitions audited in `ActionDecisionRecord`. | [`models/action_plan.py:11-34`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/models/action_plan.py#L11-L34)<br>[`data/action_plan_repository.py:10-70`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/data/action_plan_repository.py#L10-L70) | `CANONICAL` |
| **`ActionDecisionRecord`**| `action_decision_records` | **Immutable append-only audit trail** recording before_state, after_state, decision verb, and impact preview. | [`models/action_plan.py:47-59`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/models/action_plan.py#L47-L59) | `CANONICAL` |

---

## 3. Events, Triggers & Re-evaluation Points

The domain triggers discrete lifecycle events when client inputs mutate or decisions are executed:

### Event Inventory

```text
Event: RAW_FINANCIAL_INPUT_MUTATED
├── Trigger: API POST/PUT to /api/financial_state or data repository mutation
├── Handler: FinancialStateService.build_financial_state()
├── Output: New FinancialState snapshot created
└── Re-evaluation: Moneywheel ratios, constraint assessment, and goal feasibility become stale.

Event: GOAL_DEFINED_OR_UPDATED
├── Trigger: API POST to /api/goals/save-and-define
├── Handler: GoalService.save_and_define_goal() -> GoalEngine.calculate_defined_goal()
├── Output: New DefinedGoal version (version + 1)
└── Re-evaluation: Strategy runs and multi-goal allocations for this goal become stale.

Event: STRATEGY_RUN_EXECUTED
├── Trigger: API POST to /api/strategy/build
├── Handler: StrategyService.build_strategy() -> StrategyEngine.execute()
├── Output: StrategyRun persisted with applicable strategies, architectures, and recommendation
└── Re-evaluation: Produces DecisionResult.

Event: STRATEGY_VERSION_SELECTED
├── Trigger: API POST to /api/strategy/select
├── Handler: StrategyService.select_strategy()
├── Output: Creates StrategyVersion; updates PrimaryStrategyState; generates ActionPlanItems
└── Re-evaluation: Action Plan generator generates deterministic action items.

Event: STRATEGY_EDIT_COMMITTED
├── Trigger: API POST to /api/strategy/edit
├── Handler: StrategyEditService.edit_strategy()
├── Output: StrategyEditResult with reassessment flags:
│   ├── suitability_reassessment_required: bool
│   ├── approval_snapshot_required: bool
│   └── primary_replacement_required: bool
└── Re-evaluation: Forces re-run of suitability engine if parameters exceed threshold bounds.

Event: ACTION_STATUS_TRANSITIONED
├── Trigger: API POST to /api/action-plan/decision
├── Handler: ActionPlanService.confirm_decision()
├── Output: ActionStatus changes (planned -> confirmed | deferred | cancelled); ActionDecisionRecord saved
└── Re-evaluation: Updates action queue.

Event: ACTION_COMPLETED
├── Trigger: API POST to /api/action-plan/complete
├── Handler: ActionPlanService.complete_action_with_actual_state()
├── Output: ActionPlanItem.status = 'completed'; actual_impact recorded; ActionDecisionRecord saved
└── Re-evaluation: [GAP] Should trigger FinancialState snapshot update, but currently does not!
```

---

## 4. Deep Audit of the Action ➔ State Update Flow (The Feedback Gap)

The critical architectural question in an agentic financial decision engine is:  
> *When an investor completes an agreed action, how does the resulting actual financial state feed back into the canonical Financial State store?*

### Source Code Inspection of `ActionPlanService`:

Lines 102–136 of [`backend/services/action_plan_service.py`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/services/action_plan_service.py#L102-L136):

```python
    def complete_action_with_actual_state(
        self,
        action: ActionPlanItem,
        actual_state: dict[str, Any],
        completion_preview: ActionImpactPreview,
    ) -> tuple[ActionPlanItem, ActionDecisionRecord, dict[str, Any]]:
        # 1. Validates projected state presence
        projected_state = action.planned_impact.get("financial_state")
        projected = FinancialState.model_validate(projected_state)
        actual = FinancialState.model_validate(actual_state)

        # 2. Computes variance analysis
        comparison = self.impact_engine.compare(projected, actual)
        actual_impact = {
            "financial_state": actual.model_dump(mode="json"),
            "variance_analysis": comparison,
        }

        # 3. Updates Action Item in action repository
        updated = self.repository.update_action(
            action.planning_unit_id,
            action.action_id,
            {"status": "completed", "actual_impact": actual_impact},
        )

        # 4. Records decision audit record
        record = self.repository.record_decision(ActionDecisionRecord(
            planning_unit_id=action.planning_unit_id,
            action_id=action.action_id,
            decision="complete",
            before_state=action.model_dump(mode="json"),
            after_state=updated.model_dump(mode="json"),
            impact_preview=completion_preview,
        ))

        # 5. Returns tuple
        return updated, record, comparison
```

### Critical Findings:
1. **Quarantined State Mutation (`IMPLICIT` / `MISSING`):**
   - The confirmed `actual_state` is saved **only** inside the `ActionPlanItem.actual_impact` dictionary and in the `ActionDecisionRecord.after_state` JSON blob.
   - It is **never written** to `FinancialStateSnapshotRepository` (`backend/data/financial_state_repository.py`).
2. **Broken Re-evaluation Loop (`MISSING`):**
   - Because no new `FinancialState` snapshot is created in the snapshot repository, downstream consumers (`MoneywheelService`, `GoalService`, `StrategyService`, `DashboardService`) continue reading the old financial snapshot.
   - The system does not reflect the positive variance or capital change achieved by completing the action.

---

## 5. Current Implementation vs. Target Canonical Model

### Current Implementation:
- State snapshots are strictly immutable and cleanly decoupled.
- Action items have a full lifecycle (`planned` ➔ `confirmed` ➔ `completed`).
- However, completing an action terminates as a leaf event without propagating into the global financial state store.

### Target Canonical Model:
- **Bidirectional Decision Loop:**
  $$\text{Selected Strategy} \xrightarrow{} \text{Action Plan} \xrightarrow{} \text{Execution / Completion} \xrightarrow{} \text{New FinancialState Snapshot} \xrightarrow{} \text{Recalculate Health \& Goals}$$
- `ActionPlanService.complete_action_with_actual_state()` must call `FinancialStateSnapshotRepository.save_snapshot()` to emit a new official financial snapshot.
- Add an explicit invalidation signal or domain event notification when financial state changes, alerting the user that previous strategy recommendations require review.

---

## 6. Gaps & Refactoring Implications

1. **Close the Action Completion Feedback Loop:** Inject `FinancialStateSnapshotRepository` into `ActionPlanService` and call `save_snapshot(actual_state)` upon successful action completion.
2. **Add Snapshot Source Tracking:** Add `source: Literal['user_input', 'action_completion', 'system_reconciliation']` to `FinancialState` model metadata.
3. **Formalize Event Payloads:** Create typed Pydantic event models in `backend/models/events.py` for state invalidation triggers.
