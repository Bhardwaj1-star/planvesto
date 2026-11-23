# Goal Planner — Repository Impact Audit

**Status:** Documentation / planning only  
**Scope:** Proposed Case 2A and Case 2B affordability flow  
**Repository:** `bhardwaj1-star/planvesto`

> This document maps existing dependencies and anticipated changes. It does not authorize production-code changes. No production source files are modified by this audit.

## 1. Purpose

Identify repository sections outside Goal Planner that consume, display, or operationalize its feasibility decisions. Impact is grouped as:
- **Direct impact:** owns or displays feasibility decisions and requires changes.
- **Integration impact:** consumes goal/strategy data and must preserve the selected affordability scenario.
- **Source dependency:** supplies canonical financial data and should remain the source of truth.

## 2. Goal Planner behaviour in scope

### Case 1 — Current affordability
Case 1's verified Available Monthly Surplus is the funding-capacity reference for subsequent affordability checks.

### Case 2A — Adjust goal amount or timeline
Test one condition at a time:
- **Option A — Reduce goal amount:** keep target month/year fixed; find the highest affordable goal amount.
- **Option B — Extend timeline:** keep today's goal amount fixed; find the earliest affordable target month.
- A scenario passes when its additional required monthly SIP is within verified Available Monthly Surplus.

### Case 2B — Keep goal amount and target date fixed
Goal amount and target date remain fixed. Two contribution structures:
- **Option A — Step-Up SIP:** calculate required annual step-up using the approved changing-contribution schedule method. Initial maximum annual step-up cap is 10%. If required rate is at or below 10%, show starting SIP / contribution schedule and monthly surplus capacity needed. If it exceeds 10%, do not recommend a rate above the cap; proceed to Option B.
- **Option B — Initial Lump Sum + Step-Up SIP:** use a maximum 10% annual step-up schedule and calculate the approximate initial lump sum required to bridge the remaining funding gap.

Increasing income, reducing expenses, or changing EMI outflows are budgeting actions, not Goal Planner Case 2B options.

## 3. Repository impact map

### 3.1 Directly impacted Goal Planner files

| File | Existing responsibility observed | Anticipated change |
|---|---|---|
| `frontend/app/investor/goal-planner/page.tsx` | Goal creation, editing, cancellation, asset mapping, funding status cards, feasibility component, Strategy Builder and Multi-Goal links | Preserve goal CRUD and asset mapping unless separately redesigned. Revise feasibility presentation and route through the new affordability selection flow. Reconcile direct Strategy Builder links with selected feasibility results. |
| `frontend/components/goals/GoalFeasibility.tsx` | Feasibility status/reason, surplus vs required contribution, missing-data links, feasibility workspace CTA | Redesign status and CTA for Case 1 / Case 2A / Case 2B and selected result. |
| `frontend/app/investor/goal-planner/[goalId]/feasibility/page.tsx` | Loads Financial State and latest goal; contains Case 2A revised amount/date evaluation and feasibility workspace | Primary workspace to align with the single Fund Feasibility test, Case 2A options and Case 2B Step-Up / Lump Sum + Step-Up. Keep goal amount/date fixed in Case 2B. |
| `backend/app/domain/features/goal_planner/feasibility.py` | Canonical Fund Feasibility calculation; currently SIP, Lump Sum and Combined Lump Sum + SIP | Extend domain calculations for dated Step-Up SIP cash flows and initial lump sum + Step-Up SIP. Preserve the single-test boundary and 10% product cap. |
| `backend/app/api/routers/goal_planner.py` | Builds Financial State feasibility context and evaluates current goal | Add/coordinate scenario evaluation endpoints or request modes. Continue sourcing Available Monthly Surplus from canonical Financial State; never fabricate/increase it in Goal Planner. |
| `backend/app/api/schemas/goal_planner.py` | Goal calculation/response fields including required SIP, surplus gap, required surplus increase and case | Define explicit validated inputs/outputs for selected case, step-up schedule, lump sum and scenario affordability. Avoid ambiguous reuse of legacy fields. |
| `frontend/lib/onboarding/goals/types.ts`, `frontend/lib/api/goals.ts` | Frontend goal and feasibility contracts | Extend typed contracts for scenario outputs and selected affordability context as required. |

### 3.2 Strategy workflow — integration impact

| File | Existing responsibility observed | Anticipated change |
|---|---|---|
| `frontend/app/investor/strategy-builder/page.tsx` | Loads goals, selects a goal, calls `buildStrategy(planningUnitId, goalId)`, performs funding assessment and displays surplus | Receive selected affordability scenario and its version/context. Do not silently substitute fallback/sample values when verified surplus or scenario inputs are missing. |
| `frontend/lib/api/strategy.ts` | Strategy Build request currently sends planning unit, goal ID and investor priorities | Carry a stable affordability-scenario reference or validated snapshot, not only goal ID. |
| `backend/app/api/schemas/strategy_builder.py` | `StrategyBuildRequest` currently includes planning unit, goal ID and optional priorities; runs/versions carry goal-version references | Add scenario reference/snapshot validation so a Strategy Run is traceable to its affordability decision. |
| `backend/app/api/routers/strategy_builder.py`, `backend/app/domain/features/strategy_builder/` | Builds strategy runs and evaluates strategy/funding paths | Consume approved affordability scenario as an input constraint. Keep strategy selection distinct from Goal Planner feasibility calculation. |
| `frontend/app/investor/strategy-comparison/page.tsx` | Displays comparison for a selected Strategy Run | Preserve linked goal version and affordability context; do not compare incompatible scenario assumptions. |
| `frontend/app/investor/strategy-scenarios/page.tsx` | Loads Strategy Run, checks goal version and compares monthly contribution with available surplus | Reconcile implementation inputs with selected Step-Up or lump-sum scenario. A flat SIP boundary must not incorrectly reject a valid dated step-up schedule or conceal its affordability requirements. |
| `frontend/components/StrategyWorkflowNav.tsx` | Navigation across Strategy Builder, Comparison, Implementation and History; Planning Basket button | No structural change inherently required; preserve selected goal/scenario context in navigation and return paths. |

### 3.3 Action Plan and multi-goal planning

| File / area | Existing responsibility observed | Anticipated change |
|---|---|---|
| `frontend/app/investor/action-plan/page.tsx` | Loads goals and selected Strategy Versions; links back to Strategy Builder by goal ID | Keep Action Plan based on finalized Strategy Versions. Preserve the affordability scenario reference in finalized strategy and show it as decision context where useful. |
| `frontend/components/PlanningBasketButton.tsx` | Creates/selects browser-local baskets containing goal IDs | No immediate change for individual Case 2A/2B. If basket planning consumes selected scenarios, add versioned scenario references to basket storage/event payloads. |
| Backend multi-goal planning: `goal_coordination.py`, `consolidated_plan.py`, `cross_goal_impact.py` | Coordinates goals, consolidated plan and cross-goal impacts | Ensure a single-goal scenario's full surplus or lump-sum capital is not treated as independently available to every goal. Prevent double allocation. |

### 3.4 Reports and history

| File / area | Existing responsibility observed | Anticipated change |
|---|---|---|
| `frontend/app/investor/reports/page.tsx` | Selects goals, baskets and finalized Strategy Versions; offers individual and basket reports | Individual reports should identify selected case, scenario inputs, step-up rate, starting SIP, lump sum (if any), assumptions and result. |
| `backend/app/api/routers/reports.py`, report domain/schemas | Generates goal strategy and basket reports | Include selected affordability scenario and provenance. Distinguish individual goal scenarios from consolidated basket allocation. |
| `frontend/app/investor/strategy-history/page.tsx`, `frontend/app/investor/goal-history` | Review/history navigation and versioned goal/strategy records | Preserve scenario history/version links so later goal edits or recalculations do not rewrite earlier decision context. |

### 3.5 Navigation and supporting pages

| File / area | Existing responsibility observed | Anticipated change |
|---|---|---|
| `frontend/components/InvestorSidebar.tsx` | Main navigation for Financial State, Budgeting, Goal Planner, Strategy Builder, Action Plan, Reports and History | No navigation restructure required by feasibility logic alone. Change only if a distinct route/stage is introduced. |
| `frontend/app/investor/financial-state/page.tsx` | Financial State dashboard | Remains source of verified monthly surplus and financial evidence. Change only for source-data correctness, not to accommodate Goal Planner scenarios. |
| `frontend/app/investor/budgeting/page.tsx` | Budget data, expense limits and cash-flow targets | Keep budgeting actions here. Do not expose income increases, expense cuts or EMI changes as Case 2B Goal Planner alternatives. |
| Moneywheel and other overview pages | Overview-level financial presentation | No direct dependency confirmed in this audit; review only if they display feasibility or consume changed response fields. |

## 4. Critical data and calculation contracts

1. **Canonical surplus:** Backend feasibility context reads `investable_surplus_monthly` from the Financial State snapshot. Continue using it as the monthly capacity reference.
2. **Existing goal SIP:** Backend reads `existing_goal_sips_by_goal`. Distinguish existing goal-specific contributions from additional contribution required.
3. **Goal version:** Strategy Run and Strategy Version already carry `goal_id`, `defined_goal_id` and `defined_goal_version`. Link affordability scenario identity/version to these records to prevent stale or mismatched decisions.
4. **Step-up calculation:** Use Chapter 05's dated cash-flow method for changing schedules. Do not use a constant-SIP formula for Step-Up SIP.
5. **Combined funding:** Project initial lump sum and each dated step-up contribution to the fixed goal date using a consistent return/timing basis.
6. **10% cap:** Never display or recommend annual step-up above 10%. If required rate exceeds the cap, evaluate the capped schedule and calculate the remaining initial lump-sum requirement.
7. **Lump-sum evidence:** A calculated requirement is a scenario amount, not proof the investor owns or has committed it. Confirm eligibility, liquidity, timing and competing commitments.
8. **No double counting:** Existing assets, goal-specific SIPs, new contributions and initial lump sums must not be counted twice. Multi-goal allocation must prevent the same surplus/capital being committed to multiple goals.
9. **No implicit mutation:** Scenario previews must not modify saved goals, allocate/sell assets, commit lump-sum capital or change contributions without explicit investor approval through an authorized workflow.
10. **Missing evidence:** Missing inputs, unsupported methods or unavailable source evidence must result in unresolved / insufficient-evidence status, not invented defaults.

## 5. Recommended implementation sequence

1. Finalize Goal Planner functional contract and scenario result fields.
2. Implement and test canonical backend calculations for Case 2A, Step-Up SIP and Initial Lump Sum + Step-Up SIP.
3. Update feasibility workspace and GoalFeasibility summary UI.
4. Add scenario identity/version and snapshot linkage to Strategy Builder API and Strategy Run.
5. Update Strategy Builder, Comparison and Implementation to preserve and validate that context.
6. Update Action Plan, reports and history to retain approved decision context.
7. Review multi-goal allocation and basket reporting for shared-surplus / lump-sum double counting.
8. Run regression tests for goal CRUD, asset mapping, Case 1, Case 2A, Case 2B, strategy build, implementation, reports and multi-goal planning.

## 6. Scope boundaries and audit caveats

- This is a documentation-only repository impact audit; no production source files are changed.
- The map is based on reviewed frontend routes/components, API schemas/clients and backend domain code. It is not a complete line-by-line audit of every report renderer, migration, persistence mapper or test.
- Budgeting remains the place for budget changes; Case 2B remains limited to Step-Up SIP and Initial Lump Sum + Step-Up SIP.
- Financial State remains the source of verified surplus; Goal Planner must not create a new surplus figure.
- Add other modules to the impact map only when an actual dependency is confirmed.
