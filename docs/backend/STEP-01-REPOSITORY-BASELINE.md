# Step 1 — Repository Baseline & Backend Architecture Contract

## Objective
Establish the exact backend boundaries before implementation. This step is documentation/architecture only; do not redesign the frontend or database.

## Verified repository facts
The current `main` tree already contains these backend layers:
- `backend/api/` — HTTP/API routes, including `orchestration.py`, `strategy.py`, `strategy_edit.py`, `strategy_version.py`.
- `backend/services/` — application/service layer.
- `backend/data/` — repositories and Supabase access.
- `backend/engines/` — calculation/strategy decision logic.
- `backend/models/` and `backend/schemas/` — domain/request/response contracts.

The existing `backend/engines/strategy/engine.py` already performs the single-goal strategy flow: applicability filtering, scenarios, comparison, architecture composition, decision evaluation, ranking and recommendation. Reuse it as the per-goal engine.

The existing `backend/api/orchestration.py` exposes `/api/orchestration/context`. It authenticates/authorizes the planning context and delegates to `PlanningOrchestrationService`.

The existing `PlanningOrchestrationService` currently builds shared planning context and module availability. It explicitly does not perform financial classification, suitability rules, strategy ranking or aggregate Moneywheel status. Therefore it is not the final multi-goal planning engine.

## Branch verification
At the time this document was created:
- `feature/multi-goal-financial-plan-v2` == `main` (no commit difference).
- `feature/multi-goal-plan-v2` == `main` (no commit difference).
Therefore these branches must not be treated as containing completed multi-goal implementation.

## Architecture contract
Use this separation:

1. **API layer**
   - Validate/authenticate requests.
   - Call services.
   - No financial decision logic.

2. **Planning orchestration/service layer**
   - Assemble the investor/family financial state and selected goals.
   - Coordinate the multi-goal planning workflow.
   - Do not duplicate StrategyEngine calculations.

3. **Multi-goal decision/orchestration engine**
   - Resolve goal priority using client-selected priority plus defined financial-ratio checks/constraints.
   - Detect cross-goal resource conflicts.
   - Decide how available resources are allocated across goals.
   - Invoke the existing single-goal StrategyEngine for each goal after its context is resolved.
   - Preserve both client priority and final system-resolved priority for traceability.

4. **Existing StrategyEngine**
   - Remains responsible for the strategy decision for one defined goal under its supplied context.
   - Do not fork or rewrite it merely to support multiple goals.

5. **Consolidation layer**
   - Combine goal-level strategy results into one coherent Financial Plan.
   - Preserve goal-level recommendations and cross-goal trade-offs.

6. **Report layer**
   - Produce structured report data for each goal and for the complete plan.
   - PDF generation should consume this structured output; PDF formatting must not contain business rules.
   - If the system internally resolves a client priority because a financial-ratio rule conflicts with it, the explanation belongs in the report output. It is not a separate screen override control.

## Explicitly out of scope for this step
- Frontend changes.
- Supabase schema changes.
- SQL migrations.
- New financial-product logic.
- Risk-profile redesign.
- Changing the existing StrategyEngine decision model.

## Step 1 acceptance criteria
- [ ] Coding agent can identify the existing StrategyEngine and reuse boundary.
- [ ] Coding agent can identify the current orchestration context layer and does not mistake it for multi-goal decisioning.
- [ ] No frontend/schema/migration work is introduced.
- [ ] All new multi-goal logic has a clear engine/service boundary.
- [ ] Later steps consume this contract rather than creating parallel architecture.
