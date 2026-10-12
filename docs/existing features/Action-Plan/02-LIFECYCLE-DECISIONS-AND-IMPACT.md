# Action Plan — Lifecycle, Decisions and Impact Comparison

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## Decision transitions

`ActionPlanService.confirm_decision()` validates the requested verb and action status:
- **add:** planned → confirmed;
- **modify:** planned/confirmed; only title, description, priority, deadline and planned impact are editable;
- **complete:** planned/confirmed → completed;
- **cancel:** planned/confirmed → cancelled;
- **delete:** removes an action unless it is already completed/cancelled.

The service records before-state, after-state and impact preview in decision history. A decision record is historical evidence; it is not the same object as the current action row.

## Actual-state completion & ActionImpactEngine Execution

The completion endpoint (`POST /api/action-plan/{action_id}/complete`) requires:
1. The submitted `source_financial_state_snapshot_id` to match the current family Financial State snapshot.
2. A projected Financial State snapshot in the action's `planned_impact["financial_state"]`.
3. Validation that both projected and actual snapshots belong to the same planning unit and family scope.

`ActionImpactEngine.compare()` (`backend/engines/action_plan/impact_engine.py`) deterministically calculates variances across the following 8 tracked metrics:
1. `income_monthly` (₹)
2. `expenses_monthly` (₹)
3. `investable_surplus_monthly` (₹)
4. `total_assets` (₹)
5. `total_liabilities` (₹)
6. `emi_burden_monthly` (₹)
7. `net_worth` (₹)
8. `safety_reserve_months` (months)

For each metric, it computes:
$$\text{variance} = \text{actual} - \text{projected}$$
If any metric is missing or not available in either state, that metric is skipped. The result is stored directly inside `actual_impact["projected_vs_actual"]` on the action item and saved to `ActionDecisionRecord.after_state`.

## Consistency risk to test

Snapshot persistence, action update and decision-history insertion are separate operations in the inspected path. A failure between writes may leave partial state unless transaction/compensation behavior exists elsewhere. Do not claim atomicity without evidence.

## Lifecycle boundary

A completed action is evidence of execution and updated financial-state input. It does not alone prove that all goals/strategies were revalidated, that a revised strategy was accepted, or that a report was regenerated.
