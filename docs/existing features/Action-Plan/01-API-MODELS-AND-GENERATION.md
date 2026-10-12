# Action Plan — API, Models and Action Generation

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## API surface

Router prefix: `/api/action-plan` in `backend/api/action_plan.py`.
- `GET /api/action-plan`: List all action items for planning unit (optional filter `strategy_version_id`).
- `POST /api/action-plan`: Create a single action item.
- `GET /api/action-plan/{action_id}`: Fetch single action item by ID.
- `POST /api/action-plan/generate`: Bulk generate actions from approved strategy version.
- `GET /api/action-plan/decision-history`: Retrieve historical decision trail (`ActionDecisionRecord`).
- `POST /api/action-plan/confirm-decision`: Execute a lifecycle transition on an action item.
- `POST /api/action-plan/{action_id}/complete`: Complete action by comparing projected vs actual Financial State snapshot.

Action creation verifies that the Strategy Version exists, is linked to a goal (`version.goal_id`), is the currently selected Strategy Version for that goal (`selected_version_id == strategy_version_id`), and is approved via an explicit approval snapshot (`is_strategy_version_approved()`). Non-matching states return HTTP 409 Conflict.

## Models, Status Enums and Data Contracts

Defined in `backend/models/action_plan.py`:
- **`ActionStatus` Enum:** `Literal["planned", "confirmed", "completed", "cancelled"]` (default: `"planned"`).
- **`ActionDecision` Verbs:** `Literal["add", "modify", "delete", "complete", "cancel"]`.
- **`Priority` Levels:** `Literal["high", "medium", "low"]` (default: `"medium"`).
- **`ActionPlanItem`:**
  - `action_id`: str (UUID)
  - `planning_unit_id`: str (min 1, max 100)
  - `strategy_version_id`: str (min 1, max 100)
  - `title`: str (min 1, max 200)
  - `description`: str | None (max 5000)
  - `priority`: Literal["high", "medium", "low"]
  - `deadline`: str | None (max 100)
  - `status`: ActionStatus
  - `planned_impact`: dict[str, Any] (contains `generation_key`, `strategy_id`, `architecture_id`, `implementation_parameters`, and baseline `financial_state`)
  - `actual_impact`: dict[str, Any] (contains `variance_analysis` from `ActionImpactEngine`)
  - `created_at`: UTC ISO timestamp
- **`ActionImpactPreview`:** `action`, `financial_state_impact`, `goal_impacts`, `strategy_impact`, `moneywheel_impact`, `alternatives`, `cause_explanation`.
- **`ActionDecisionRecord`:** Historical audit entity (`decision_id`, `planning_unit_id`, `action_id`, `decision`, `before_state`, `after_state`, `impact_preview`, `confirmed_at`, `historical=True`).

## Exact Action Generation Algorithm and Rules

Generation is owned by `backend/services/strategy_action_generator.py::StrategyActionGenerator.generate()` and rules by `backend/rules/action_plan.py::build_action_specs()`:

1. **Precondition Validation:**
   - Must be an approved Strategy Version (`is_strategy_version_approved`).
   - Must have `version.goal_id`, `defined_goal_id`, `defined_goal_version`, and `architecture`.
   - Must match the currently selected Strategy Version for that goal.
   - Strategy definition must exist in active strategy registry.
2. **Strategy & Technique Decomposition:**
   - Collects primary strategy (`architecture.primary_strategy_id`) and supporting strategies (`architecture.supporting_strategy_ids`).
   - Collects all canonical technique IDs (`architecture.technique_ids` + `primary.technique_ids`).
3. **Canonical Action Specs Mapping (`rules/action_plan.py`):**
   - **Primary Strategy Rule:** Generates 1 action with **`priority: "high"`**:
     - *Title:* `"Implement {primary_strategy.name}"`
     - *Description:* `"Execute the approved {primary_strategy.name} strategy architecture for this goal. Core mechanism: {primary_strategy.core_mechanism}"`
   - **Supporting Strategy Rule:** Generates 1 action per supporting strategy with **`priority: "medium"`**:
     - *Title:* `"Implement supporting strategy: {supporting.name}"`
     - *Description:* `"Apply the supporting {supporting.name} component defined by the approved strategy architecture. Strategic objective: {supporting.strategic_objective}"`
   - **Technique Rule:** Generates 1 action per technique with **`priority: "medium"`**:
     - *Title:* `"Apply {technique.name}"`
     - *Description:* `"Apply this implementation technique as part of the approved strategy: {technique.description} Purpose: {technique.purpose}"`
4. **Deterministic Idempotency Key:**
   - Each action creates a unique generation key:
     `generation_key = f"{strategy_version_id}:strategy-action:{index}:{title}"`
   - Existing actions for that `strategy_version_id` with the same `generation_key` are deduplicated and skipped, guaranteeing safe repeated calls.

## Authority

Strategy evaluation/recommendation and investor approval belong upstream. Action Plan is downstream execution. A strategy version ID supplies lineage; an approval snapshot is the explicit gate used in the inspected create path.
