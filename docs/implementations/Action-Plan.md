# Action Plan — Final Implementation Specification

**Document type:** Authoritative implementation specification  
**Scope:** Accepted-path actions, action generation, investor decisions on actions, execution tracking, impact comparison, and action-history preservation  
**Status:** Feature definition aur existing-feature audit se consolidated implementation contract. User Journey sirf flow alignment ke liye aur Real-Life Decision Cases business boundaries/examples ke liye use hote hain. Current code evidence, required behavior aur unresolved points alag rakhe gaye hain; document yeh claim nahi karta ki har requirement implemented hai.

## 2. Design references

This specification keeps business requirements, user-flow alignment, Real-Life Decision Cases, and inspected code evidence distinct.

- **Primary business definition:** [docs/feature/Action-Plan.md](../feature/Action-Plan.md).
- **Existing-code baseline:** the five documents under [docs/existing features/Action-Plan/](../existing%20features/Action-Plan/). These describe the inspected code baseline; they do not prove current production behavior.
- **Journey alignment:** [docs/User Journeys/12-ACTION_PLAN_JOURNEY.md](../User%20Journeys/12-ACTION_PLAN_JOURNEY.md) confirms the high-level user flow only.
- **Real-Life Decision Cases:** use them to clarify business boundaries and examples, not as proof that code already implements them.
- **Conflict rule:** keep code-evidenced current behavior, required business behavior, and unresolved policy separate. Do not invent missing rules or claim an unverified implementation exists.


## 2. Purpose and ownership

Action Plan is the bridge between an investor's **Accepted Plan** and real-world execution. It translates an adopted financial path into concrete actions, makes each action's purpose and relationship to the plan clear, and tracks the action's lifecycle and actual impact where supported.

Action Plan is not:
- a strategy-selection engine;
- an independent goal-feasibility engine;
- a report-only presentation layer;
- a list that becomes active merely because a strategy recommendation or What-If scenario was generated.

Goal Planner / Goal Feasibility identifies goal requirements, funding gaps and feasible funding paths. Strategy Builder designs the implementation structure for the selected path. Investor Decision / Accepted Plan determines which proposal is adopted. Action Plan translates the adopted path into executable steps and tracks execution.

## 3. Sources of actions and scope

Action Plan is not limited to Strategy Builder-generated actions. Actions may arise from the accepted financial path, including:
- goal-funding or feasibility-related changes;
- debt repayment, prepayment, restructuring and EMI/cash-flow changes;
- accepted resource-allocation changes across goals;
- selected strategy, variant, technique, method/policy and implementation design;
- investor-adopted execution changes that alter required future actions.

Examples from the documented cases include increasing a goal contribution by a specified amount, deploying an available lump sum, reallocating contributions between competing goals, restructuring a liability and redirecting released cash flow, or executing a selected strategy. These are conditional examples, not unconditional actions: an action must follow from the accepted path and its evidence.

## 4. Inputs and outputs

### Inputs
- Planning unit and authoritative current Financial State.
- Relevant goals, goal-feasibility/funding context and constraints.
- Explicitly adopted decision and Accepted Plan / selected approved strategy version.
- Selected implementation structure and accepted execution parameters, where applicable.
- Existing active actions, action decisions and completed-action history.
- Baseline financial snapshot and relevant planned-impact evidence when required for execution comparison.

### Outputs
- Goal-linked and, where appropriate, plan-level actions.
- Clear action title, purpose, source and relationship to the Accepted Plan.
- Amount, timing/deadline, priority, order, dependencies, source and destination where defined by the accepted decision.
- Current action status and recorded investor decision.
- Planned impact and actual-impact/variance evidence where supported.
- Revised future actions after an adopted change, with prior decisions and completed actions preserved.

Do not invent amounts, deadlines, priorities, sources, destinations or dependencies when the accepted decision does not provide them. Represent unavailable details explicitly according to the data contract.

## 5. Action generation and authority checks

The existing audit identifies action generation in `backend/services/strategy_action_generator.py::StrategyActionGenerator.generate()` and action-spec rules in `backend/rules/action_plan.py::build_action_specs()`.

The audited generation path requires an approved Strategy Version, a linked goal and defined goal-version context, architecture, the currently selected version for that goal, and a strategy present in the active registry. The create path also checks an explicit approval snapshot. Invalid or mismatched state is recorded by the audit as a conflict rather than a valid generation source.

The audited generator decomposes architecture into:
- primary strategy;
- supporting strategies;
- canonical techniques from the architecture and primary strategy definitions.

The audited rule mapping creates:
- one high-priority action for the primary strategy;
- one medium-priority action per supporting strategy;
- one medium-priority action per technique.

These are current-code audit findings for the inspected baseline, not a declaration that these rules cover every required Action Plan source. In particular, planning-level actions arising from goal funding, debt/cash-flow changes or multi-goal allocation must not be assumed complete merely because strategy actions can be generated.

### Idempotency

The audit documents a deterministic `generation_key` based on strategy version, action index and title, used to skip duplicate actions when generation is repeated. Preserve safe repeat-generation behavior and verify that edits or changed accepted versions do not cause stale actions to be silently treated as current.

## 6. Action data contract and lifecycle

The audited model in `backend/models/action_plan.py` defines:
- **ActionStatus:** `planned`, `confirmed`, `completed`, `cancelled`.
- **ActionDecision verbs:** `add`, `modify`, `delete`, `complete`, `cancel`.
- **Priority:** `high`, `medium`, `low`.
- **ActionPlanItem:** planning-unit and strategy-version linkage, title/description, priority, optional deadline, status, planned impact, actual impact and creation timestamp.
- **ActionImpactPreview:** action, Financial State impact, goal impacts, strategy impact, Moneywheel impact, alternatives and cause explanation.
- **ActionDecisionRecord:** historical decision record with before/after state and impact preview where available.

These are the audited current model contracts, not a substitute for verifying the live schema and API behavior before changing them.

An action's status, an investor's decision about that action, the action's execution, and the financial outcome are separate facts. Marking an action complete does not by itself prove that the expected financial or goal result was achieved.

## 7. Action review, confirmation and execution

The canonical journey is:

```text
Accepted Plan
    ↓
Implementation Requirements
    ↓
Action Plan
    ↓
Investor Reviews Actions
    ↓
Prioritise / Confirm
    ↓
Execution and Progress Tracking
```

Each action should make clear, where defined:
- what to do and why;
- amount;
- timing/deadline;
- source and destination;
- order and dependencies;
- status;
- expected impact;
- revalidation trigger, where relevant.

The investor may review actions, confirm practical execution, adjust timing where permitted, and track completion. Exact validation rules for changes to amounts, dates, priorities, dependencies and other execution parameters must follow the existing approved contract; do not assume every field is freely editable.

## 8. Planned impact, actual impact and completion

The audited model records `planned_impact`, including generation lineage, strategy/architecture identifiers, implementation parameters and a baseline Financial State. The audited `actual_impact` can contain variance analysis from the Action Impact Engine.

The audited completion endpoint compares projected and actual Financial State snapshots. The implementation must preserve the distinction between:
- the action instruction and its status;
- the baseline and expected impact;
- the actual observed financial state;
- variance between expected and actual impact;
- whether the goal or broader plan remains feasible.

Completing an action must not automatically mark a goal achieved, assert a projected return was realized, or silently change the Accepted Plan. Where actual evidence is unavailable, do not fabricate a successful outcome.

## 9. Accepted Plan, proposals and What-If isolation

Keep these states separate:
1. Strategy decision/recommendation generated.
2. Proposal or What-If scenario explored.
3. Investor decision recorded.
4. Accepted Plan updated through explicit adoption.
5. Active Action Plan reconciled with the accepted path.
6. Actions executed and progress/actual impact recorded.

A recommendation, saved scenario, report, historical strategy version or generated action list does not by itself prove investor adoption. A What-If experiment must not overwrite the active Accepted Plan or active Action Plan.

If the investor rejects or defers an alternative, the existing Accepted Plan and its applicable actions remain unchanged. If the investor adopts a revised path, reconcile the affected actions only after the adoption transition is recorded.

## 10. Impact analysis, execution changes and targeted revalidation

The documented change loop is:

```text
Accepted Plan
    ↓
Execution / What-If Change
    ↓
Impact Analysis
    ↓
Targeted Revalidation when required
    ↓
Investor Decision
    ↓
Updated Accepted Plan
    ↓
Updated Action Plan
```

Treat a changed execution parameter first as an execution change; it does not automatically imply a canonical strategy change. Assess the consequences relevant to the change, which may include goal outcome, funding gap, contribution, cash flow, liquidity, debt/EMI and effects on other goals.

If the change materially affects feasibility, constraints, strategy suitability or dependencies, revalidate the affected decisions before adopting the revised path. Do not silently replace a strategy or active plan.

Whole-Plan / Multi-Goal Impact is conditional: invoke it for a plan-level decision, shared-resource conflict or material cross-goal effect. It is not a mandatory gate for every individual-goal change. Keep revalidation targeted and preserve unrelated valid actions unless a material dependency requires a change.

Exact materiality thresholds, dependency mapping and invalidation triggers remain unverified/not frozen.

## 11. Reconciliation after an adopted plan change

After explicit investor adoption:
- add actions required by the newly accepted path;
- revise or deactivate active actions that are no longer applicable according to the approved lifecycle contract;
- preserve unaffected actions unless their dependencies or evidence have materially changed;
- preserve completed actions as historical records;
- retain the decision trail explaining what changed and why;
- ensure the current Action Plan represents the current accepted implementation, without erasing prior execution history.

The audit/feature source leaves the exact old-action migration, revision/deactivation mechanics and historical version model not yet frozen. Do not invent a replacement policy or delete completed actions to make the new plan look clean.

## 12. Multiple goals and plan-level actions

A complete financial plan may contain multiple coordinated strategies and actions across different goals. Action Plan must not assume that one goal or one Strategy Builder run represents the entire financial plan.

When goals compete for the same surplus or assets, the Goal Planner / Multi-Goal Planning layer establishes feasibility, shared-resource consequences and the accepted allocation path. Action Plan executes the accepted changes; it must not independently optimize or allocate the same resources without an accepted decision.

A new goal against an existing plan is initially a proposal/scenario. Rejection leaves the existing plan/actions unchanged. Acceptance updates the plan through the investor-decision lifecycle and reconciles only the relevant actions.

## 13. Code evidence and API surface

### Code references identified by the existing audit
- Frontend: `frontend/app/investor/action-plan/page.tsx`
- API: `backend/api/action_plan.py`
- Repository: `backend/data/action_plan_repository.py`
- Service: `backend/services/action_plan_service.py`
- Generation: `backend/services/strategy_action_generator.py`
- Rules: `backend/rules/action_plan.py`
- Models: `backend/models/action_plan.py`
- Impact engine: `backend/engines/action_plan/impact_engine.py`
- Frontend API client: `frontend/lib/api/action-plan.ts`

### API surface recorded in the audit
- `GET /api/action-plan`: list actions for a planning unit, optionally filtered by strategy version.
- `POST /api/action-plan`: create one action.
- `GET /api/action-plan/{action_id}`: fetch one action.
- `POST /api/action-plan/generate`: generate actions from an approved strategy version.
- `GET /api/action-plan/decision-history`: retrieve historical action-decision records.
- `POST /api/action-plan/confirm-decision`: execute an action lifecycle decision.
- `POST /api/action-plan/{action_id}/complete`: complete an action using projected-versus-actual Financial State comparison.

These are API contracts reported by the inspected audit baseline. Confirm current `main` behavior before treating the route list as a current runtime guarantee.

## 14. Unverified implementation facts

The feature definition and audit leave the following unresolved:
- Completeness of action generation for goal funding, debt, cash-flow, multi-goal allocation and strategy implementation.
- Exact rules for amount, timing, sequencing, dependencies, source/destination and deadlines.
- The exact investor-adoption contract for each accepted path.
- Technical isolation and persistence of What-If scenarios from the Accepted Plan and active Action Plan.
- Materiality thresholds, dependency graph and targeted-revalidation triggers.
- Exact migration/revision/deactivation behavior for old active actions after plan changes.
- Preservation and editing policy for completed actions and historical records.
- Reminder/due-date behavior and dependency enforcement.
- Whether every action completion reliably compares authoritative, correctly scoped Financial State snapshots.
- Current database/schema and runtime behavior relative to the cited audit baseline.

Keep code-evidenced behavior, required business behavior and unresolved decisions separate. A UI route, model field, generator, history record or design document alone does not prove that the complete business lifecycle is implemented.
