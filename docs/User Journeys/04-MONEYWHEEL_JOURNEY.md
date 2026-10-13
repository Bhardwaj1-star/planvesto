# Moneywheel User Journey

**Document Type:** User Journey  
**Status:** CANONICAL DESIGN  
**Feature:** Moneywheel  
**Scope:** Financial State evidence → Moneywheel measurements → Investor review → Downstream planning use

---

## 1. Main Journey

```
Authoritative Financial State + Relevant Goal Context
                         ↓
               Check Required Inputs
                         ↓
               Calculate Available Metrics
                         ↓
        Show Values + Availability + Evidence
                         ↓
                  Investor Reviews
                         ↓
       ┌─────────────────┼─────────────────┐
       ↓                 ↓                 ↓
  Understand         Correct / Update    Continue to
  current position   missing inputs      Planning
       ↓                 ↓                 ↓
  Review evidence    Recalculate affected Goal Planner /
  and limitations    measurements         Strategy Builder
```

This journey describes the specified feature contract. It does not claim that every specified metric or integration is already implemented in runtime.

## 2. Entry and Inputs

Moneywheel uses:
- Server-owned Financial State as the authoritative financial input.
- Relevant goal context for metrics that depend on goal targets, funding, projections or duration.
- Explicit scenario assumptions where a metric, such as Investment–Debt Spread, requires an investment-return assumption.
- Versioned Goal Planner results and explicit portfolio cash-flow/resource assumptions for Portfolio-Level Return Required, once that calculation contract is finalized.

Client-supplied snapshots must not override authoritative server data. Missing or invalid inputs remain visible; the system must not invent a value.

## 3. Calculation and Results

The system calculates the metrics defined by the Moneywheel implementation specification and presents, where available:
- Metric name and value.
- Unit and status, where a status rule exists.
- Availability and reason when a value cannot be calculated.
- Relevant assumptions, source context, timestamp and version/evidence metadata.

A missing input, invalid denominator or non-finite result is **unavailable**, not zero and not healthy. Do not invent status bands for Weighted Debt Rate, Investment–Debt Spread or Portfolio-Level Return Required.

The current runtime contract includes the legacy `required_rate_of_return` metric. The specification assigns Goal-Level Return Required to Goal Planner and defines Portfolio-Level Return Required as a planned Moneywheel measurement. Do not treat that target contract as already deployed or remove the legacy field without an approved compatibility and migration plan.

## 4. Investor Review

The investor can:
- Review the measurements and the financial evidence behind them.
- Correct or update missing or inaccurate source information through the relevant financial-input flow.
- Review the stated assumptions and limitations.
- Continue to Goal Planner or Strategy Builder with the available evidence.

Moneywheel reports measurements; it does not independently decide which goal to fund, select a strategy, choose a variant or technique, or recommend a concrete solution.

## 5. Downstream Handoff

```
Moneywheel Measurements + Availability + Evidence
                       ↓
              Goal Planner / Feasibility
                       ↓
             Funding Paths + Feasibility
                       ↓
                Strategy Builder
```

- **Goal Planner** owns goal-level requirements, funding-path comparison and Goal Feasibility. It may use relevant Moneywheel measurements as evidence.
- **Strategy Builder** consumes Goal Planner feasibility context and relevant Moneywheel evidence; it must not recreate Moneywheel formulas.
- The canonical constraint/decision layer determines whether a metric is diagnostic, a warning, an eligibility input, a hard constraint or recommendation evidence. A critical Moneywheel status is not automatically a universal planning block.

## 6. Portfolio-Level Return Required

The specified dependency is one-way:

```
Goal Planner calculates versioned goal-level requirements
                         ↓
Moneywheel evaluates combined dated obligations,
portfolio resources and explicit cash-flow assumptions
                         ↓
Portfolio-Level Return Required, or unavailable with reason
                         ↓
Goal Feasibility may consume the result as additional evidence
```

This measure must not be calculated as the arithmetic average of goal-level required returns. The calculation contract, resource scope, dated cash flows and solver semantics must be finalized before implementation. It is a required return under stated assumptions—not an expected or guaranteed return and not an automatic instruction to increase investment risk.

## 7. Changes and Recalculation

When relevant Financial State, goal data or scenario assumptions change:
1. Identify the measurements affected by the changed input.
2. Recalculate those measurements using authoritative inputs.
3. Show updated values, availability, assumptions and evidence.
4. Let downstream planning assess the impact where relevant.

A recalculation does not automatically replace a strategy, accept a proposal, change the Accepted Plan, allocate shared assets, earmark assets or complete an Action Plan item. Material changes may trigger targeted revalidation, but plan changes require the applicable planning process and investor decision.

## 8. Core Boundaries

- Moneywheel owns its metric calculations and traceable measurement snapshots.
- Goal Planner owns goal-level required return, funding paths and Goal Feasibility.
- Strategy Builder owns strategy selection and its implementation proposal.
- Shared canonical rules determine the role and severity of constraint-derived evidence.
- Asset mapping alone does not reserve an asset or make it unavailable to other goals.
- Missing evidence remains unavailable/unknown; no arbitrary defaults or forced recommendations.
- This document describes the specified journey, not proof that each target capability is live.
