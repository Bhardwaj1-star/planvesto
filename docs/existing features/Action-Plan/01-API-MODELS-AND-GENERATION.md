# Action Plan — API, Models and Action Generation

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## API surface

Router prefix: `/api/action-plan` in `backend/api/action_plan.py`. Endpoints list actions (optionally filtered by strategy version), generate actions, fetch one action, list decision history, create an action, complete an action with actual state, and record an action decision. Routes authenticate and validate planning-unit, action or Strategy Version ownership according to operation.

Action creation verifies that the Strategy Version exists, is linked to a goal and is the currently selected Strategy Version for that goal. The service also requires an approval snapshot for the Strategy Version before creating an implementation action. Conflicts are returned as 409; do not treat client visibility of a strategy version as approval.

## Models and requests

`backend/models/action_plan.py` defines action items, decision records and impact preview structures; `backend/schemas/action_plan.py` defines strict request payloads for create, decision and completion. Inspect these models before changing field names or status literals. The current lifecycle uses statuses including planned, confirmed, completed and cancelled; decision verbs include add, modify, delete, complete and cancel.

## Generation

`POST /actions/generate` delegates to `StrategyActionGenerator`, which creates action candidates based on the selected strategy version and associated strategy/technique structure. This is a generation path, distinct from manually creating an action and from confirming an action decision. Idempotency and duplicate prevention must be verified against generator and repository behavior before assuming repeated calls are harmless.

## Authority

Strategy evaluation/recommendation and investor approval belong upstream. Action Plan is downstream execution. A strategy version ID supplies lineage; an approval snapshot is the explicit gate used in the inspected create path.
