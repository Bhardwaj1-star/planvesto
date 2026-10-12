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

## Actual-state completion

The completion endpoint requires the submitted source snapshot ID to match the current family Financial State snapshot. The service requires a projected Financial State in the action's planned impact, validates both projected and actual Financial State against the same planning unit and family scope, and requires Financial State authority persistence.

`ActionImpactEngine.compare()` compares projected with actual state. The service saves actual state with action/version/source-snapshot lineage, updates the action with actual impact and variance analysis, then writes a completion decision record.

## Consistency risk to test

Snapshot persistence, action update and decision-history insertion are separate operations in the inspected path. A failure between writes may leave partial state unless transaction/compensation behavior exists elsewhere. Do not claim atomicity without evidence.

## Lifecycle boundary

A completed action is evidence of execution and updated financial-state input. It does not alone prove that all goals/strategies were revalidated, that a revised strategy was accepted, or that a report was regenerated.
