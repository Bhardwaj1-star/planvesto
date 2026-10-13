# Goal Planner — Financial Planner Guide

## 1. Purpose

Goal Planner helps answer four questions:
1. What amount will this goal require by its target date?
2. What resources and contributions may be available to fund it?
3. Is the goal feasible under the stated assumptions and financial constraints?
4. If it is not feasible, what funding path or goal adjustment could make it feasible?

Goal Planner calculates goal requirements and feasibility evidence. It does not independently choose the final strategy or implement a plan.

## 2. Responsibilities across the planning system

| Component | Responsibility |
|---|---|
| Goal Planner | Goal requirements, projections, funding gap, required contribution, goal-level required return, feasibility, and funding-path comparison |
| Moneywheel | Financial ratios and metrics used as evidence by Goal Planner; Goal Planner must not duplicate their calculations |
| Budgeting | Provides income, expenses, and cash-flow/surplus information; Goal Planner must not invent available surplus |
| Whole-Plan / Multi-Goal Analysis | Checks competing goals and shared-resource conflicts when a change materially affects the broader plan |
| Strategy Builder | Selects/designs an appropriate strategy and implementation using Goal Planner's feasibility context |
| Investor decision / Accepted Plan | A proposal becomes active only through explicit investor acceptance |
| Action Plan | Converts an adopted plan into execution actions |

**Keep these concepts separate:** a funding mechanism (such as SIP, lump sum, or step-up contribution) is not itself a Strategy Builder strategy. Goal Funding is part of goal feasibility and funding-path analysis, not an extra strategy.

## 3. Information needed for a reliable assessment

Depending on the goal and calculation, use:
- Canonical goal type, target amount/current cost, target date, priority, flexibility, and status.
- Inflation assumptions and their source.
- Goal-specific details—for example, current age, retirement age, and life expectancy for retirement.
- Relevant assets mapped to the goal, resolved against authoritative asset records.
- Current financial context: assets, liabilities, income, expenses, debt payments, and available surplus.
- Funding scenario assumptions: contribution amount/timing, return assumption, eligible resources, debt repayment, and other modeled changes.
- Existing accepted plan context when evaluating a change to an active plan.
- Reference date and calculation assumptions.

Missing or invalid required inputs must produce an incomplete/unavailable result with a reason. Defaults must be identified as assumptions, not presented as facts supplied by the investor. Use authoritative financial records; do not rely on an unverified client-supplied snapshot where an authoritative source exists.

## 4. Core calculations and what they mean

| Item | Meaning |
|---|---|
| Target-date requirement | Amount needed by the goal's target date, calculated using the applicable goal rules and declared assumptions |
| Projected resources | Future value of eligible mapped resources under the stated assumptions |
| Funding gap/surplus | Difference between the target-date requirement and modeled available funding; the output must clearly state its sign convention |
| Required contribution | Contribution needed under a stated timeline and return assumption |
| Goal-Level Return Required | Annualized return mathematically required for a specific goal under a defined funding scenario |
| Feasibility | Whether a funding path fits the relevant resource, cash-flow, timing, and constraint conditions |
| Funding mechanism | SIP, lump sum, step-up contribution, use of assets, or a supported combination |
| Strategy | A separate Strategy Builder decision, not a synonym for a funding mechanism |

### Goal-Level Return Required

Goal Planner owns the required return for an individual goal. Calculate it using the target-date requirement, time remaining, eligible current resources, and the scenario's contribution schedule. Different contribution schedules can produce different required returns.

- State the cash-flow timing, compounding/annualization convention, inflation treatment, and assumptions.
- Distinguish required return from expected return, guaranteed return, and required contribution.
- Required contribution solves for the contribution using a declared return assumption; required return solves for the return using a declared funding schedule. These are different calculations.
- If the inputs do not support a meaningful solution, return unavailable/indeterminate with a reason rather than inventing a percentage.
- Recalculate when a material goal or scenario input changes.

## 5. Goal Feasibility: two ordered approaches

Goal Feasibility must use these approaches as one ordered process—not as separate features or engines.

### Approach 1 — Improve the funding path first

Keep the goal's current target amount and target date unchanged. Examine the investor's evidenced financial capacity, including income, expenses, available surplus, existing assets, debt obligations, liquidity needs, risk limits, and competing goals.

Compare relevant uses of money and funding alternatives. Where appropriate, apply **Opportunity Cost**: what material benefit might the investor give up by choosing one path instead of another? Alternatives may include goal contributions, debt prepayment, investment while servicing debt, loan/EMI restructuring, liquidity preservation, or a combination.

The objective is to find a suitable feasible use of the investor's actual financial capacity—not simply to maximize a surplus figure. Do not invent surplus, count the same asset twice, assume returns are guaranteed, or violate applicable hard constraints.

If a suitable path makes the goal feasible, present its assumptions and trade-offs. Do not proceed to goal-condition changes as though they were necessary.

### Approach 2 — Calculate goal adjustments only if still infeasible

If Approach 1 cannot make the goal feasible within applicable constraints, calculate what change may be required:
- **Reduce target amount:** estimate the target that fits the available funding capacity.
- **Extend target date:** estimate the additional time required.
- **Combine adjustments:** where needed and where the calculation supports a meaningful result.

Recalculate the target-date requirement, required return/contribution, projected resources, funding gap, cash-flow fit, and feasibility as applicable. Explain the change from the original goal and its consequences.

These are proposed Goal Feasibility adjustments—not a separate What-If feature. Do not change the canonical goal automatically. The investor decides whether to accept a proposed adjustment. If no acceptable path exists, explain the binding constraints and shortfall; never force a recommendation.

## 6. Funding-path comparison and Opportunity Cost

Compare relevant paths on a consistent reference date and with clearly stated assumptions. For each modeled path, show where applicable:
- Funding mechanism, contribution amount/schedule, and timing.
- Resources used and remaining liquidity.
- Target requirement, projected funding, residual gap/surplus, and feasibility.
- Debt balance, payments/EMI, interest and duration when debt is involved and data is available.
- Return/inflation assumptions and projected outcome, clearly labelled as uncertain.
- Material impact on other goals or an Accepted Plan.
- Binding constraints, missing inputs, risks, and limitations.
- Opportunity cost relative to another comparable path.

Relevant options depend on the client's circumstances; do not force a fixed set of options or show a path that cannot be modeled from available evidence.

### Debt versus investment

Debt existence, a high DTI, leverage, or a negative Investment–Debt Spread does not by itself prove that debt reduction is the best choice. Likewise, an assumed investment return above a debt rate does not prove that investing is best.

Use Moneywheel's metrics and metadata rather than duplicating its formulas. Compare complete alternatives, considering cash flow, liquidity, debt terms, goal timing, competing goals, uncertainty, and relevant fees/taxes when data is available. Disclose missing inputs rather than fabricating a complete comparison.

## 7. Constraints and result interpretation

Keep these distinct:
- **Hard constraint:** makes a path unacceptable when a defined rule is breached.
- **User-adjustable goal parameter:** target amount or date may be proposed for adjustment, but the canonical goal changes only after acceptance.
- **Financial-state fact:** income, expenses, debt obligations, or available surplus; do not edit these merely to make a goal appear feasible.
- **Projection assumption:** return, inflation, or another modeling assumption; do not silently increase it to force feasibility.
- **Warning/diagnostic:** signals a condition for review and is not automatically a hard block.

Use clear result meanings:
- **Feasible under stated assumptions:** a path fits the relevant conditions.
- **Feasible only with changes:** specify the required contribution, resource, target, date, or assumption change.
- **Not feasible under stated assumptions:** explain the shortfall or binding condition.
- **Incomplete / cannot determine:** authoritative evidence or required inputs are missing, invalid, or insufficient.
- **No acceptable path:** the modeled options do not meet applicable hard constraints or investor-defined limits.

If the interface uses labels such as “Constrained” or “Unknown,” explain their exact meaning and preserve the underlying result state. Do not treat a warning as a hard constraint without an explicitly owned rule.

## 8. Asset mapping and shared resources

**Mapping is not earmarking.** Mapping associates an asset with a goal for planning; it does not mean the asset is sold, locked, reserved, or unavailable for another goal.

- Resolve mapped assets from authoritative records and show the projection assumptions.
- Do not count one asset or the same surplus as fully available to multiple goals.
- Surface shared-resource conflicts when goals compete for the same money or assets.
- Earmarking, partial allocation, release, and remapping are separate decisions with their own defined lifecycle.
- Cancelling a goal must not delete the underlying asset from Financial State.

## 9. When to assess the whole plan

Start with the affected goal's requirement, mapped resources, funding gap, and feasibility. Check broader multi-goal impact when a change may materially affect shared resources, competing goals, or an Accepted Plan—for example:
- A new goal competes for existing assets or surplus.
- A goal's target, date, or contribution change reduces resources another goal relies on.
- A material change in income, expenses, debt, or asset values changes feasibility.
- A funding path changes debt payments or reallocates resources among goals.

When relevant, identify affected goals, before/after funding gaps and feasibility, shared-resource conflicts, assumptions, and decisions that need revalidation. Do not rebuild unrelated decisions automatically.

## 10. Decision and handoff

A calculation or preview is a proposal, not an accepted plan. Keep goal calculation, saving goal details, accepting a funding path, accepting a goal-condition adjustment, and executing actions as distinct steps.

After the relevant goal/feasibility decision is established, provide Strategy Builder with:
- Goal identity and target requirements.
- Timeline and calculation assumptions.
- Mapped-resource evidence and availability caveats.
- Funding gap/surplus, required contribution, and goal-level required return where calculable.
- Feasibility result and its reasons.
- Relevant funding paths, trade-offs, constraints, and missing evidence.
- Material whole-plan impact and revalidation needs.

Strategy Builder designs the strategy and implementation; Action Plan follows the adopted plan. A recalculation must not silently accept a proposal, change goal priority, or overwrite an Accepted Plan.

## 11. Illustrative cases

Real-life examples are test illustrations, not default values for other investors. For example:
- A retirement case can compare retirement contributions, debt prepayment, and loan restructuring using the case's stated assumptions.
- An education case can test the future target, asset projection, funding gap, required contribution/return, and feasibility over its stated horizon.

Calculate outputs from each case's explicit inputs. Do not hardcode illustrative outcomes or require one option to win regardless of the assumptions.

## 12. Important limitations

- Calculations depend on the accuracy and freshness of financial data and scenario assumptions.
- Projected returns are uncertain and must not be presented as guarantees.
- A high required return is not permission to exceed risk limits.
- No acceptable path is a valid outcome.
- Proposed goal changes require investor acceptance.
- Goal Planner must consume Moneywheel's canonical metrics rather than reimplementing them.
- This guide describes intended planning behavior; it does not by itself prove that every calculation or workflow is currently implemented in the live system.
