# Planning Orchestration — Workflow Readiness & Cross-Module Context Architecture

**Backend API:** `backend/api/orchestration.py`  
**Core Services:** `backend/services/planning_orchestration_service.py`, `backend/services/multi_goal_planning_service.py`  
**Engines & Models:** `backend/engines/orchestration/engine.py`, `backend/models/orchestration.py`, `backend/schemas/orchestration.py`

---

## 1. Role in Planvesto

Planning Orchestration serves two vital architectural roles:
1. **Module Availability & Workflow Readiness (`PlanningOrchestrationService`):**
   Acts as the central traffic controller that tracks which modules (Financial State, Goals, Strategy, MoneyWheel, Action Plan) have sufficient data to execute, returning clear blockers, missing data requirements, and redirect routes.
2. **Multi-Goal Resource Orchestration (`MultiGoalOrchestrator`):**
   Coordinates multiple goals competing for the same investable monthly surplus, resolving goal priority conflicts and allocating resources without altering individual goal strategy designs.

---

## 2. API Surface (`/api/orchestration`)

- `POST /api/orchestration/context`: Evaluates overall readiness across all Planvesto modules for a planning unit and scope.
- `POST /api/orchestration/plan`: Executes multi-goal plan calculation, competition detection, and surplus distribution across goals.

---

## 3. Workflow Readiness & Module Availability Contracts (`models/orchestration.py`)

### A. Module Availability State (`ModuleAvailability`)
For each engine/feature, it evaluates:
- `available: bool`
- `reason: str | None` (e.g., *"No Financial State snapshot exists for this planning context"* or *"Action Plan requires a strategy version reference"*).

### B. Workflow Readiness Evaluation (`WorkflowReadiness`)
- **`status`:** `"ready"` or `"blocked"`.
- **`process_route`:** Internal application route (must be absolute path, validated by `_validate_internal_route`).
- **`blockers`:** List of `WorkflowBlocker` objects containing missing data labels and the required resolution route.
- **`next_action`:** Deterministic next step to unblock the workflow (`WorkflowNextAction: label, route`).

---

## 4. Multi-Goal Resource Orchestration Engine (`engines/orchestration/engine.py`)

### A. Priority Resolution Rules
- Preserves `client_priority` for full historical auditability.
- If approved `rule_overrides` exist (e.g., from `RULE_EMERGENCY_RESERVE_CRITICAL` demoting a discretionary goal to `low`), the system computes `resolved_priority` and flags `override_applied = True`.
- Canonical rank precedence:
  $$\text{critical} (0) < \text{high} (1) < \text{medium} (2) < \text{low} (3)$$
  (Smaller rank number indicates higher precedence).

### B. Competition Detection & Allocation
- Compares total required monthly contribution across all goals against `total_available_monthly_surplus`.
- If $\sum \text{required} > \text{surplus}$, sets `competing_resources_detected = True` and uses `ResourceAllocationEngine` to allocate funds in strict priority rank order.
- Goals that do not receive full required funding are marked as `partially_funded` or `unfunded` with specific trade-off notes.
