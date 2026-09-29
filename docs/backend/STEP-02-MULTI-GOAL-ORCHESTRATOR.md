# Step 02 — Multi-Goal Orchestrator

## Purpose
Build the backend orchestration layer that coordinates multiple goals without replacing the existing single-goal Strategy Engine.

## Current repo context
- `backend/engines/strategy/engine.py` already performs single-goal strategy evaluation, scenario generation, ranking and recommendation.
- `backend/api/orchestration.py` currently exposes planning-context construction only.
- `backend/services/planning_orchestration_service.py` currently builds shared module availability/context; it must NOT be treated as the multi-goal decision engine.
- `feature/multi-goal-financial-plan-v2` and `feature/multi-goal-plan-v2` are currently identical to `main`; do not assume either contains completed multi-goal implementation.

## Scope
Create the orchestration layer needed to run several goals together and coordinate their resource constraints.

### Required responsibilities
1. Load the investor/family financial state and selected goals.
2. Preserve the investor's stated goal priority.
3. Run the existing Strategy Engine independently for each goal.
4. Collect each goal's feasibility, funding requirement, strategy recommendation and constraints.
5. Detect competition for shared resources (cash-flow surplus, existing assets, liquidity, etc.).
6. Resolve conflicts using explicit business rules.
7. Keep the investor priority as an input, while allowing defined system rules to override the resulting allocation when necessary.
8. Preserve both the investor-selected priority and the final system-resolved outcome for reporting/auditability.
9. Produce a consolidated multi-goal planning result for the later Financial Plan/report layer.

## Important business rule already decided
Goal priority is selected by the client. Planvesto checks relevant financial ratios/financial-health conditions against that priority. If a defined rule conflicts with the client's priority, the system may override the allocation/strategy outcome. This override should NOT be presented as an editable priority change on the screen; the final report must explain the reason.

## Architectural rule
Do NOT duplicate or rewrite the single-goal Strategy Engine. The orchestrator calls it. Strategy Engine remains responsible for single-goal strategy evaluation; orchestration is responsible for cross-goal coordination.

## Suggested structure
- `backend/engines/orchestration/` — pure multi-goal coordination logic
- `backend/services/multi_goal_planning_service.py` — application/service layer
- `backend/schemas/multi_goal_planning.py` — request/response contracts if required by existing conventions
- `backend/api/orchestration.py` — extend only after the service/engine contract is clear

Use existing repository/model/repository conventions rather than introducing a parallel architecture.

## Do NOT do in Step 02
- Do not modify Supabase schema.
- Do not create SQL migrations.
- Do not redesign frontend/UI.
- Do not implement product selection, risk profiling, or portfolio construction.
- Do not make the Strategy Engine responsible for multi-goal allocation.
- Do not invent financial-ratio thresholds unless an existing business rule explicitly defines them.

## Expected output
A deterministic multi-goal orchestration component with unit tests covering:
- one goal;
- multiple independent goals;
- competing goals sharing the same surplus;
- client priority preserved when no rule conflict exists;
- rule-driven allocation override;
- traceability of client priority vs resolved outcome;
- insufficient resources / infeasible combinations.

## Completion gate
Step 02 is complete only when the orchestrator can consume the existing financial context and selected goals, invoke the existing single-goal Strategy Engine per goal, resolve cross-goal resource conflicts through explicit rules, and return a consolidated planning result without changing the database schema or frontend.
