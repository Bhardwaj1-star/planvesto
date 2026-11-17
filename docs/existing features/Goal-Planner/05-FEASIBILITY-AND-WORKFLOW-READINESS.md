# Goal Planner — Feasibility and Workflow Readiness

**Source revision:** `5a3b060e1b27915ede226f5173364e23dca1263e`

## 1. Ownership in code

The feasibility check lives in `GoalService._apply_feasibility`, not inside the pure `GoalEngine.calculate_defined_goal` method.

Source: [backend/services/goal_service.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/services/goal_service.py#L83-L242`).

The service docstring at lines 151–156 explicitly describes this as a planning feasibility check and says the Financial State snapshot is the source of available surplus.

## 2. Financial State prerequisite

The service calls `FinancialStateService.get_current_snapshot(planning_unit_id, scope="family")` (lines 157–164).

Two unavailable cases are handled:
1. No usable Financial State dictionary from the snapshot → `feasibility_status = "unknown"`.
2. Missing or unavailable `investable_surplus_monthly` metric → `feasibility_status = "unknown"`.

The service stores a reason, a `goal_feasibility` object in version metadata, a missing prerequisite, and a next action labelled `Complete Financial State` with route `/investor/financial-state`. Missing income/expense metrics can add routes to onboarding income/expense.

A metric represented as a dictionary uses its `value` and `available` fields; objects with equivalent attributes are also accepted by helper methods at lines 83–99.

## 3. Feasibility status decision

Once investable monthly surplus is available:
- surplus is clamped to at least zero;
- required contribution is clamped to at least zero;
- funding strategies are built from funding gap, return assumption, duration and surplus;
- `monthly_contribution_surplus_gap = required - surplus`.

The status branch at lines 217 onward is:
- `feasible` if funding gap ≤ 0;
- `feasible` if required monthly contribution ≤ available surplus;
- `constrained` if surplus is positive but lower than required contribution;
- `infeasible` if there is a funding gap and no positive investable monthly surplus.

The status is not the same as `funding_status`: a goal may have `funding_status = "Shortfall"` while feasibility is `feasible` if the required contribution fits the available surplus.

## 4. Workflow readiness attachment

Helpers at lines 101–149 construct a `WorkflowPrerequisite` for `financial_state`, then call `PlanningOrchestrationService.build_workflow_readiness`.

The process route is constructed as `/investor/goal-planner/{goal_id}/feasibility`. The result is assigned to `DefinedGoal.workflow_readiness` and serialized into `version_metadata.workflow_readiness`.

When readiness already exists, `_ensure_workflow_readiness` returns the goal as-is. If feasibility is unknown without readiness, it records the missing-surplus reason and attaches blocked readiness; otherwise it attaches available readiness.

## 5. When feasibility is recalculated

- `calculate_preview` enriches retirement context, calculates a DefinedGoal and applies feasibility (lines 242–246).
- `save_and_define_goal` calculates a new DefinedGoal, applies feasibility, then persists it (lines 248–309).
- `get_latest_defined_goal` reads latest and applies feasibility again (lines 311–315).
- `get_defined_goal_version` reads a specified historical version and calls `_ensure_workflow_readiness`, rather than unconditionally applying current feasibility to it (lines 317–321).

This distinction matters: latest snapshot retrieval can refresh feasibility against current financial state, while historical version retrieval preserves the stored calculation and only ensures readiness is attached if needed.


## 6. Current API and UI integration

The current Goal Planner API resolves Available Monthly Surplus from the latest family Financial State snapshot; the browser does not submit or override this value. When monthly component metrics are present, the backend applies:

`Available Monthly Surplus = Income Monthly − Expenses Monthly − Monthly Savings / Investments`

Savings/investment values are read from Financial State fields where present, including monthly investment totals, existing SIP totals, goal-wise SIP totals, or the savings-investment rate. Goal-wise existing SIP is separately deducted from the goal's total required SIP to calculate the additional SIP needed for that goal. If Financial State has no usable surplus metric, feasibility remains `unknown` rather than treating missing data as zero.

The latest defined-goal endpoint refreshes affordability against the current Financial State snapshot while preserving the saved goal amount, target date, and mapped-asset assumptions. Family scope is used for the snapshot lookup.

The Goal Feasibility page exposes:
- Case 1 when the additional SIP fits Available Monthly Surplus or eligible mapped assets already cover the future target.
- Case 2A as an unsaved preview that recalculates the goal after changing today's goal cost and/or target month.
- Case 2B with the surplus gap and required surplus increase, plus the supported routes to review income/expense changes, Step-Up SIP, Lump Sum + SIP, and verified EMI/debt changes.

Step-up rates and lump-sum assets are not invented by the system. They remain investor-specified scenarios requiring affordability and asset suitability checks before a route can be marked feasible.


### 6.1 Backend-owned surplus and recurring contributions

Financial State build now normalizes income and expenses to monthly amounts, includes recurring monthly/annual investment contributions recorded against assets, calculates `Income − Expenses − Savings/Investments`, and persists the resulting immutable snapshot. Goal-wise SIP amounts are allocated from mapped assets using the mapping percentage (or mapped currency share), so the goal's additional SIP is calculated after deducting its existing mapped SIP. The browser submits contribution facts only; it never submits Available Monthly Surplus.

Existing assets default to zero recurring contribution until the investor records their actual SIP / investment amount in the asset form. Apply migration `021_asset_monthly_contributions.sql` before deploying this change.
