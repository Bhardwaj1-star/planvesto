# Planvesto Strategy Architecture Conversion Specification

**Status:** Final architecture / implementation contract
**Purpose:** Define the goal-agnostic Strategy Builder architecture and the conversion required to make the current implementation conform to it.

## 1. Objective

Strategy Builder is a **goal-agnostic financial strategy decision system**. For a specific investor, financial state, and defined goal, it must determine which strategy architectures are applicable, compare the eligible architectures using explicit strategy-fit evidence, and produce an explainable Strategy Result.

The target definition of strategy is:

> For THIS investor, for THIS goal, given THIS financial state and THESE priorities, what is the appropriate way to fund and achieve the goal?

The system must produce a **strategy architecture**, not a product recommendation, portfolio allocation, or retirement-only plan.

`Safety`, `Liquidity`, `Growth`, `Flexibility`, and the legacy composite score are **not strategy-selection mechanisms**. They must not determine strategy identity, eligibility, ranking, or recommendation.

## 2. Non-negotiable architecture

```text
Investor Financial State
        +
Defined Goal
        +
Constraints / Priorities
        |
        v
   RULE / ELIGIBILITY ENGINE
        |
        | applicable architectures
        v
   STRATEGY LIBRARY
        |
        | strategy architectures
        v
 STRATEGY VARIANTS / IMPLEMENTATION LOGIC
        |
        v
 COMPARISON / DECISION ENGINE
        |
        v
 Strategy Result / Recommendation
        |
        v
 Goal-specific Output
        |
        +--> Retirement Report / PDF (retirement only)
        +--> Future goal-specific outputs
```

The engine must not invert this flow by starting with products, portfolios, retirement reports, or generic score dimensions.

## 3. Responsibilities by layer

### 3.1 Financial State

Input facts only: income, expenses, surplus/deficit, assets, liabilities, liquidity position, existing funding assets and other persisted investor facts.

Do not convert Financial State directly into a strategy without a goal.

### 3.2 Defined Goal

The goal is the strategic context. At minimum the engine needs:

- goal type / normalized goal key
- target date / horizon
- target amount or goal-specific target requirement
- funding status
- funding gap / surplus
- existing mapped assets
- relevant constraints

Retirement is one supported goal type and must use its dedicated retirement corpus calculation.

### 3.3 Rule / Eligibility Engine

This layer answers:

> Which strategy architectures are applicable for this investor and this goal?

Rules are deterministic and explainable. Each rule should return evidence/diagnostics rather than silently changing a score.

Examples include:

- goal type applicability
- time horizon
- funding shortfall / surplus
- cash-flow requirements
- existing assets available for the goal
- debt constraints
- liquidity requirements as a constraint where relevant
- feasibility constraints
- retirement-specific requirements

Eligibility is a gate. An inapplicable architecture must not enter comparison simply because of any generic numeric score.

### 3.4 Strategy Library

A strategy is a reusable architecture for achieving a goal. Examples include:

- cash-flow matching
- debt reduction / debt-first funding
- progressive de-risking
- bucket strategy
- retirement glide path
- goal funding from existing assets + future contributions

Strategy definitions should describe applicability, constraints, intended outcome, trade-offs and implementation concepts.

### 3.5 Strategy Variant

A variant is a different implementation of the same strategy architecture under different assumptions or constraints.

Do not create fake strategies by merely changing return assumptions.

### 3.6 Techniques

Techniques are not strategies. Keep these separate:

- bucketing
- laddering
- glide path
- cash-flow matching techniques
- progressive de-risking techniques

A strategy may use one or more techniques.

### 3.7 Comparison / Decision Engine

The decision layer compares **eligible strategy architectures** using explicit strategy-fit evidence, including where supported:

- goal fit
- horizon fit
- funding fit
- implementation complexity
- constraint compatibility
- assumptions
- trade-offs
- stress-test behavior
- feasibility
- applicable component/strategy evidence

These are evidence dimensions, not strategy identities.

The decision engine must never reduce the decision to a renamed or reweighted version of the legacy four-dimension score.

### 3.8 Recommendation

Recommendation must identify:

- recommended strategy architecture
- why it fits this goal/investor
- applicable constraints
- key assumptions
- important trade-offs
- alternative eligible architectures
- feasibility status

Recommendation remains at the strategy level. Product and portfolio selection happen downstream.

## 4. Legacy behavior explicitly removed

The previous model used:

```text
Composite Score = weighted Safety + weighted Liquidity
               + weighted Growth + weighted Flexibility
```

That model is no longer authoritative.

Do NOT:

- rename the four dimensions and keep the same decision logic;
- replace the composite score with another arbitrary weighted score;
- treat a scenario as a strategy;
- make the highest numeric score automatically the recommendation;
- use risk profiling as a substitute for strategy eligibility;
- select a financial product before the strategy architecture exists;
- present Safety/Liquidity/Growth/Flexibility as competing strategy architectures.

Legacy dimension fields may exist temporarily for compatibility or historical evidence, but they are non-authoritative and must not determine the Strategy Result.

## 5. Generic Strategy Result contract

A Strategy Run / Strategy Result should conceptually contain:

```text
Defined Goal snapshot
Financial State snapshot / relevant evidence
Eligible architectures
Ineligible architectures + reasons where useful
Strategy architectures
Variants / scenarios
Comparison evidence
Trade-offs
Assumptions
Stress-test outputs
Recommendation
Diagnostics
```

Every recommendation must be traceable to eligibility evidence and comparison evidence.

The contract must remain goal-agnostic. Retirement-specific report fields must not be mandatory for every strategy run.

## 6. Goal-specific outputs

Strategy Builder produces the generic Strategy Result. Goal-specific outputs consume that result downstream.

### Retirement

Retirement may provide:

- Retirement Report
- retirement-specific projections and rationale
- PDF export

### Other goals

Education, home purchase, vehicle purchase, major expense, and other supported goals use the same Strategy Builder architecture. Their future reports/presentations can be added independently without rewriting the core decision engine.

A non-retirement goal must never require a Retirement Report or retirement PDF to complete Strategy Builder.

## 7. Retirement-specific requirements

Retirement is a distinct goal type, not merely a generic future-expense goal.

The retirement pipeline must account for:

- investor date of birth / current age
- retirement target date
- desired lifestyle monthly expense
- inflation until retirement
- retirement-date expense
- life expectancy
- post-retirement horizon
- retirement-period return assumption where defined
- existing mapped retirement assets
- funding gap / surplus

The output must distinguish at least:

1. today's expense,
2. retirement-date required income/expense,
3. required retirement corpus,
4. existing mapped assets,
5. funding gap,
6. required contribution where applicable.

A single inflation-adjusted annual expense is not a retirement corpus.

## 8. Strategy Builder UI contract

The UI must represent strategy architectures and strategy-fit evidence.

### Must not be strategy identity

Do not display:

- Safety
- Liquidity
- Growth
- Flexibility

as competing strategy names, strategy cards, or ranking criteria.

### Display instead

For each eligible architecture:

- Strategy name
- What it does
- Why it is applicable
- Goal fit
- Key constraints
- Main trade-offs
- Important assumptions
- Techniques used
- Feasibility
- Stress-test/scenario summary
- Implementation direction

Recommendation should show the selected architecture, reasoning and alternatives.

## 9. Goal Planner → Strategy Builder contract

Goal Planner is the source of truth for the saved Defined Goal.

When Strategy Builder opens:

1. Load the latest saved Defined Goal.
2. Verify the goal version against the existing Strategy Run.
3. If there is no run or the run is based on an older goal version, automatically build a fresh Strategy Run.
4. Do not require manual rebuilding merely because the saved goal changed.
5. Persist immutable run versions for history.

Strategy Builder must never silently display a stale run for a changed goal.

## 10. Existing investor capabilities and navigation

Moneywheel and Budgeting are independent investor capabilities and are not part of this Strategy Builder conversion. They must remain available unless a separate authoritative product decision explicitly deprecates them.

Strategy-specific lifecycle pages may be contextual rather than primary sidebar navigation. Removing a page from the sidebar does not mean deleting its underlying route or backend capability when the workflow still depends on it.

## 11. Conversion and testing order

The project follows a test-first/refactor-second process.

### Phase A — Contract protection

Keep the baseline suite green before conversion.

### Phase B — Eligibility

Determine applicability using explicit rules and diagnostics.

### Phase C — Strategy architecture

Use reusable Strategy Library definitions. Keep strategy, variant, scenario, technique and product distinct.

### Phase D — Comparison / decision

Compare eligible architectures using explicit strategy-fit evidence. Remove composite-score decision authority.

### Phase E — Recommendation

Recommendation consumes the new decision output and exposes architecture, rationale, constraints, assumptions, trade-offs, alternatives and feasibility.

### Phase F — API/service persistence

Expose and persist the generic Strategy Result without unnecessary schema changes.

### Phase G — Frontend

Render strategy architectures and decision evidence rather than legacy dimension-score identities.

### Phase H — Goal-specific reports

Retirement Report/PDF consumes the final generic Strategy Result. It must not independently reconstruct the strategy decision.

## 12. Regression requirements

Preserve:

- goal calculation behavior outside intended changes;
- corrected retirement calculation;
- Goal Planner → Strategy Builder handoff;
- automatic fresh run when the goal version changes;
- strategy eligibility and traceability;
- generic Strategy Result for non-retirement goals;
- retirement report generation;
- PDF rendering;
- CI test suite.

Known regressions must remain covered:

- retirement goal label normalization;
- stale Strategy Run after a saved goal change;
- retirement corpus must not collapse to the old annual-expense-style target;
- no-strategy state must be distinguishable from an implementation failure.

## 13. Definition of Done

- [ ] Strategy Builder is goal-agnostic.
- [ ] Eligibility determines applicable architectures.
- [ ] Strategy Library contains reusable goal-level architectures.
- [ ] Techniques are separate from strategies.
- [ ] Variants/scenarios are separate from strategy identity.
- [ ] Safety/Liquidity/Growth/Flexibility are not strategy-selection mechanisms.
- [ ] Composite score is not decision authority.
- [ ] Recommendation is explainable and goal-specific.
- [ ] Strategy Result remains generic across goals.
- [ ] Goal version changes invalidate/rebuild stale runs.
- [ ] Retirement uses the dedicated corpus calculation.
- [ ] Retirement Report/PDF is downstream and retirement-specific.
- [ ] Non-retirement goals do not depend on retirement reporting.
- [ ] Moneywheel and Budgeting remain available.
- [ ] Existing and new regression tests pass.
- [ ] CI is green.

## 14. Important implementation rule

Do not perform a broad rewrite merely to satisfy this specification. Convert one bounded contract at a time, run relevant tests, then CI, and proceed only after validation.

The objective is **architectural conversion with behavioral safety**, not a cosmetic refactor.