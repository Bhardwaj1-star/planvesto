# Goal Planning Journey — A Simple Guide

**Document Type:** User Journey  
**Feature:** Goal Planner  
**Audience:** Financial planners and non-technical readers  
**Status:** Target journey / business design  
**Purpose:** Explain how a financial goal is defined, calculated, checked for feasibility and handed to Strategy Builder when needed.

> **Important:** This document describes the intended process. It does not, by itself, prove that every step is already implemented in the live product.

---

## 1. What Does Goal Planner Do?

Goal Planner helps answer five practical questions:

1. What is the investor trying to achieve, and by when?
2. How much might the goal cost at that time?
3. How much of the required amount may already be covered by available resources?
4. What is still needed, and can the investor reasonably fund it?
5. If the current path does not work, what alternatives could the investor consider?

### The journey at a glance

**Define the goal → Estimate its future cost → Review available resources → Calculate the shortfall and funding needs → Check affordability and feasibility → Review alternatives with the investor → Hand off to Strategy Builder when relevant.**

Goal Planner provides calculations and evidence to support a decision. It must not quietly change the investor’s goal or treat a suggested option as approved.

---

## 2. Stage One — Define the Goal

Start with the canonical goal and the details needed to understand it.

For example, an Education goal might need:
- The goal’s intended date.
- The estimated cost in today’s money.
- The relevant inflation assumption.
- Existing savings or assets that the investor wants considered for this goal.
- Relevant financial information and constraints.

The system should check whether required information is present and valid before relying on it.

**If information is missing or invalid:** show what is missing and keep the result uncertain until the information is obtained. Do not invent a value just to complete the calculation.

---

## 3. Stage Two — Estimate the Future Cost

A goal’s cost today may not be the cost when the investor needs the money.

For example, education fees may rise over time. Goal Planner uses a stated inflation or cost-growth assumption to estimate the future requirement.

The planner should be able to distinguish:
- **Cost today:** the estimated cost if the goal were paid for now.
- **Future goal cost:** the estimated amount needed at the target date.
- **Time remaining:** how long the investor has before the money is required.

These are estimates based on stated assumptions, not guarantees about future prices.

---

## 4. Stage Three — Review Existing Resources and the Funding Gap

Next, Goal Planner considers the resources that are relevant to the goal.

It may project the future value of assets mapped to the goal, using the applicable assumptions and available information.

### Understand the key terms

| Term | Meaning in everyday language |
|---|---|
| **Mapped assets** | Assets identified as relevant to this goal for planning purposes. Mapping does not automatically mean the assets have been legally or operationally earmarked. |
| **Projected resources** | An estimate of what those mapped resources may be worth by the goal date. |
| **Funding gap** | The difference between the estimated future requirement and the projected resources available for the goal. |
| **Surplus** | Projected resources exceed the estimated requirement under the assumptions used. |
| **Required contribution** | The amount of additional saving or investment that a calculation indicates may be needed to cover the gap, under its assumptions. |
| **Goal-Level Return Required** | The return assumption that would be needed for the relevant goal-funding calculation to reach its target. It is an analytical requirement, not a promise that such a return is achievable. |
| **Financial capacity** | What the investor may be able to afford after considering relevant income, expenses, surplus cash flow, debt obligations and other constraints. |

The system must explain which assumptions and resources produced the result. A projected asset value is not guaranteed, and the same asset must not be treated as freely available for multiple goals without considering the resulting conflict.

---

## 5. Stage Four — Check Goal Feasibility

A goal is not feasible simply because a calculator can produce a contribution amount. The proposed funding path also needs to be considered in the context of the investor’s financial capacity, obligations and relevant constraints.

The intended assessment has two approaches, in this order.

### Approach 1 — Review Financial Options First

First, examine relevant ways the goal might be funded while considering the investor’s broader financial position.

Depending on the case and available evidence, this may include:
- Goal-funding options.
- Existing resources and available cash flow.
- Debt prepayment or changes to loan / EMI arrangements.
- Liquidity needs and financial obligations.
- Competing goals that may need the same resources.
- Opportunity cost — what the investor may give up by using money for one option instead of another.

Then recalculate the affected results and review whether an acceptable funding path exists.

**If an acceptable path is found:** show the result and the reasons to the investor for review.

**If the goal remains infeasible:** move to Approach 2.

### Approach 2 — Show Possible Goal Adjustments

Only if the first approach remains infeasible, calculate the effect of possible changes, such as:
- **Lower target:** reduce the amount or scope of the goal, where the goal allows it.
- **Later date:** extend the time available to fund it, where the timing is flexible.
- **Combined change:** consider more than one adjustment together.

Show the revised calculations and trade-offs. These are options for the investor to consider, not automatic changes to the goal.

**Rule:** Do not force a goal to appear feasible. Do not change the goal or its date without the investor’s explicit decision.

### Other valid outcomes

- **More information needed:** important evidence is missing or invalid, so a reliable assessment cannot yet be made.
- **No acceptable path:** no path qualifies under the current evidence and constraints. Show the shortfall and the relevant reasons, and preserve the current goal rather than manufacturing a recommendation.

---

## 6. Stage Five — Let the Investor Explore Changes

The investor or planner may change an assumption or detail and ask to see the effect.

| What changes? | What should be checked again? |
|---|---|
| Target date | Time remaining, future requirement, funding calculations and feasibility. |
| Target amount or cost | Future requirement, funding gap, required contribution / return and feasibility. |
| Asset mapping or value | Projected resources, funding gap and affected funding options. |
| Income, expenses or surplus | Financial capacity, affordability and feasibility. |
| Debt, EMI or loan terms | Cash flow, relevant debt options and feasibility. |
| Return or inflation assumption | The projections and calculations affected by that assumption. |
| Goal priority, flexibility or constraint | Which options qualify and whether the feasibility conclusion changes. |

Only affected calculations should be revisited. The system should explain what changed and why.

A changed calculation is not investor approval. The existing Accepted Plan must not be replaced just because a new scenario was calculated.

---

## 7. Stage Six — Explain the Result to the Investor

The result should tell the investor more than a number. Where the evidence supports it, explain:
- The goal and its target date.
- The estimated future requirement.
- The projected resources considered.
- The funding gap or surplus.
- The contribution or return requirement calculated under the stated assumptions.
- Financial capacity and relevant obligations.
- The feasibility outcome and the reasons behind it.
- Available funding options, trade-offs and any important limitations.
- The next decision or information needed.

### What do the result labels mean?

| Result | Plain-language meaning |
|---|---|
| **Feasible** | An acceptable funding path appears to meet the defined requirements under the stated assumptions and checks. It is not a guarantee of the outcome. |
| **Constrained** | The goal or its funding path has important limitations, trade-offs or conditions that the investor needs to understand. |
| **Infeasible** | The assessed path does not meet the goal’s requirements under the current assumptions and constraints. |
| **Unknown** | There is not enough valid information to reach a reliable conclusion. |
| **No Acceptable Path** | The available options have been assessed, but none qualifies under the applicable evidence and constraints. |

These labels should not be used interchangeably. In particular, missing information should not be presented as proof that a goal is infeasible.

---

## 8. When Does the Goal Affect the Rest of the Financial Plan?

Some goals can be assessed largely on their own. Others compete for the same money, assets or monthly surplus as other goals.

A broader review is needed when a material decision may affect:
- Other financial goals.
- Shared assets or available cash.
- Debt obligations or liquidity.
- The investor’s existing plan or competing priorities.

In those cases, identify the affected goals and resources, explain the trade-offs where evidence is available, and reassess the affected parts of the plan.

Do not make a full review of every goal a mandatory step for an isolated decision that has no material wider impact.

---

## 9. Handoff to Strategy Builder

Goal Planner and Strategy Builder have different responsibilities.

| Feature | Responsibility |
|---|---|
| **Goal Planner** | Defines the goal requirement, estimates the funding gap, evaluates relevant funding paths and assesses goal feasibility. |
| **Strategy Builder** | Uses the goal and feasibility evidence to consider the appropriate strategy and develop a strategy-side proposal. |
| **Investor adoption** | The investor explicitly decides whether to accept a proposal. Only then can it become the Accepted Plan. |

### What is passed to Strategy Builder?

Where available and relevant:
- The defined goal and its context.
- The current financial state.
- Funding and feasibility findings.
- Relevant constraints, assumptions and unresolved information.

Strategy Builder must not silently repeat or redefine Goal Planner’s feasibility decision. If evidence is missing, that uncertainty must remain visible.

---

## 10. Simple Example — An Education Goal

Imagine an investor is planning for an education expense several years from now.

1. **Define the goal:** record the intended date and estimated cost today.
2. **Estimate the future requirement:** apply the selected education-cost inflation assumption.
3. **Review existing resources:** consider assets mapped to the goal and estimate their future value.
4. **Calculate the gap:** compare the future requirement with the projected resources.
5. **Check affordability:** consider the required contribution alongside income, expenses, debt obligations and competing goals.
6. **Review options:** assess relevant funding paths first. If none is acceptable, show possible changes to the target or date where appropriate.
7. **Explain the result:** show the calculation, assumptions, limitations and trade-offs.
8. **Ask the investor to decide:** do not change the goal automatically. If a strategy-side decision is needed, pass the relevant evidence to Strategy Builder.

This example explains the intended journey only. It does not prescribe a specific contribution, return, strategy or feasibility result, and it does not claim every step is already implemented in the product.

---

## 11. Rules That Must Not Change

1. Use the canonical goal and validate the relevant inputs before relying on them.
2. Keep the future requirement, projected resources, funding gap, required contribution, Goal-Level Return Required and financial capacity conceptually distinct.
3. Keep Goal Planner responsible for goal funding and feasibility.
4. Review relevant financial options before proposing changes to the goal itself.
5. Only consider goal adjustments through the defined second approach when the first approach remains infeasible.
6. Never invent missing financial data, thresholds or decision rules.
7. Treat unknown information, infeasibility and no acceptable path as different outcomes.
8. Do not automatically change a goal, target date or Accepted Plan.
9. Recalculate affected outputs when a relevant input changes; do not needlessly redo unrelated work.
10. Review whole-plan impact when a material decision affects other goals or shared resources.
11. Pass relevant goal and feasibility evidence to Strategy Builder without duplicating its responsibilities.
12. This document describes the intended journey; it is not proof that every step is implemented in the live product.

---

## Related Journey

- `05-STRATEGY_BUILDER_JOURNEY.md` — how goal and feasibility evidence is used for strategy decisions and investor review.
