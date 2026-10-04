# Strategy → Action Plan

## 1. Feature Scope
Converts the current approved StrategyVersion into executable ActionPlanItems, records user decisions, and on completion records actual FinancialState and projected-vs-actual impact.

## 2. User / Request Inputs
Action generation: POST /api/action-plan/actions/generate → planning_unit_id, strategy_version_id.

Manual creation: POST /api/action-plan/actions → planning_unit_id, strategy_version_id, title, description, priority, deadline, planned_impact.

Decision: POST /api/action-plan/decisions → planning_unit_id, action_id, decision, impact_preview, after_state. Decisions: add / modify / delete / complete / cancel.

Completion: POST /api/action-plan/actions/{action_id}/complete → planning_unit_id, action_id, actual_state, completion_preview. Submitted actual_state must contain the current FinancialState snapshot ID.

## 3. Input Source / Authority Boundary
Action Plan consumes the current selected StrategyVersion and current FinancialState. ActionPlanItem is directly bound to strategy_version_id; Goal association is through StrategyVersion → Goal / DefinedGoal version.

FinancialState remains owned by FinancialStateService. Action Plan must not recalculate canonical FinancialState metrics.

## 4. Canonical Rules and Decision Logic
Before action creation/generation, the API validates Planning Unit ownership, Goal context and current selected StrategyVersion. Latest StrategyRun, ranking, recommendation alone or stale StrategyVersion cannot authorize actions.

StrategyActionGenerator validates approval, StrategyVersion, Planning Unit, Goal/DefinedGoal context, architecture, current StrategyVersion authority and active strategy-library availability. Canonical action specifications come from backend/rules/action_plan.py::build_action_specs(). Generation is idempotent by deterministic generation key.

Projected FinancialState is mandatory before completion. ActionImpactEngine compares projected and actual state and does not own financial metric formulas.

## 5. Lifecycle / State Transitions
Statuses: planned / confirmed / completed / cancelled.

Decisions: add / modify / delete / complete / cancel.

- add/confirm: planned only
- modify: planned/confirmed
- complete: planned/confirmed
- cancel: planned/confirmed
- completed/cancelled actions cannot be deleted

Every decision is persisted as ActionDecisionRecord.

Completion:
Projected State + Actual State → ActionImpactEngine.compare() → Variance → FinancialStateService.save_actual_state() → FinancialState snapshot → actual impact/history.

Submitted actual state must match the currently authoritative snapshot; stale submissions are rejected.

## 6. Approval / Decision Gate
Current implementation requires an approval snapshot for action generation/creation.

Approval is not yet fully canonicalized:
- is_strategy_version_approved() checks approval-row existence for Planning Unit + StrategyVersion;
- no explicit application approval writer was found;
- exact Goal + DefinedGoal version + suitability/context binding is not established;
- StrategyEditService can report approval_snapshot_required=False while action generation requires approval.

Target approval contract: explicit user approval command, Planning Unit binding, Goal binding, exact DefinedGoal ID/version, exact StrategyVersion, suitability/decision context, acknowledgement and ownership validation.

## 7. Output Contract
Outputs include deterministic ActionPlanItems, StrategyVersion lineage, planned impact, lifecycle status, decision history, actual impact after completion, FinancialState snapshot lineage and projected-vs-actual variance.

ActionPlanItem fields: action_id, planning_unit_id, strategy_version_id, title, description, priority, deadline, status, planned_impact, actual_impact, created_at.

## 8. Ownership Boundary
Ownership is checked at authenticated user/Planning Unit, StrategyVersion, Goal/DefinedGoal context and ActionPlanItem. Completion additionally validates StrategyVersion ownership and FinancialState scope.

## 9. Downstream Dependencies
Action completion produces updated FinancialState and impact history for future planning. Action state is execution/history evidence, not a replacement for StrategyVersion authority.

## 10. Versioning / Replanning Boundary
Old DefinedGoal → Old StrategyVersion → Old actions = history.
New DefinedGoal → New StrategyVersion → New approval → New actions = current.

Old actions must not silently migrate to a new StrategyVersion.

## 11. Code Ownership
- API: backend/api/action_plan.py
- Schemas: backend/schemas/action_plan.py
- Lifecycle: backend/services/action_plan_service.py
- Generation: backend/services/strategy_action_generator.py
- Action rules: backend/rules/action_plan.py
- Impact comparison: backend/engines/action_plan/impact_engine.py
- Model: backend/models/action_plan.py
- Repository: backend/data/action_plan_repository.py
- Strategy authority: backend/data/strategy_repository.py + backend/data/strategy_version_repository.py
- FinancialState authority: backend/services/financial_state_service.py
- Frontend: frontend/lib/api/action-plan.ts

## 12. Regression Contract
Authority: stale StrategyVersion cannot create actions; current StrategyVersion, Goal/DefinedGoal context and architecture are required.

Approval: unapproved versions cannot create/generate actions; eventual approval must bind exact Goal + DefinedGoal version + StrategyVersion + suitability context; edited versions require fresh approval where policy requires it.

Generation: deterministic; duplicate generation keys do not create duplicates; lineage is preserved.

Lifecycle: invalid transitions are rejected, editable fields remain limited, and every decision creates historical evidence.

Completion: projected state required, actual state validated, scope/ownership enforced, stale snapshot rejected, variance recorded, actual FinancialState persisted through canonical authority.

## 13. Known Implementation Gaps
1. Approval lifecycle writer and exact-context validation are not established.
2. Approval existence is weaker than the target approval contract.
3. StrategyEditService approval-required behavior is inconsistent with action-generation gating.

## 14. Important Boundaries
1. StrategyVersion → Action Plan is the valid strategy-to-action lineage.
2. Approval is a gate, not StrategyVersion authority.
3. ActionPlanItem is execution data, not strategy definition.
4. ActionImpactEngine compares states; it does not own financial formulas.
5. Actual FinancialState becomes authoritative through validated completion persistence.
6. Old StrategyVersion actions remain history after revision.
7. Decision history is audit evidence, not current planning authority.

## 15. End-to-End Contract
Current Selected StrategyVersion → Approval Gate → StrategyActionGenerator → Deterministic Action Specs → ActionPlanItems → User Decision / Execution → Actual State Submission → Projected-vs-Actual Variance → FinancialState Authority Update → Action Completion + History → Next Planning Cycle.

Scope: Strategy → Action Plan only.