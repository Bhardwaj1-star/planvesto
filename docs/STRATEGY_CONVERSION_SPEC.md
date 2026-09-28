# Planvesto Strategy Architecture Conversion Specification

**Status:** Conversion plan / implementation contract
**Purpose:** This document is the source of truth for converting the current Strategy Builder from the legacy score-driven model to the goal-first strategy architecture already covered by the new tests.

## 1. Objective

Convert Strategy Builder from a model where `Safety`, `Liquidity`, `Growth`, `Flexibility` and a composite score effectively determine the strategy into a model where the system first determines **which strategy architectures are applicable to this investor and this goal**, then evaluates eligible alternatives using explicit strategy-fit evidence.

The target definition of strategy is:

> For THIS investor, for THIS goal, given THIS financial state and THESE priorities, what is the appropriate way to fund and achieve the goal?

The system must produce a **strategy architecture**, not a product recommendation and not a portfolio allocation disguised as a strategy.

---

## 2. Non-negotiable architecture

Target flow:

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
        |  applicable strategies
        v
 STRATEGY LIBRARY
        |
        |  strategy architectures
        v
 STRATEGY VARIANTS / IMPLEMENTATION LOGIC
        |
        v
 COMPARISON / DECISION ENGINE
        |
        v
 Strategy Recommendation
        |
        v
 Action Plan / Product & Portfolio Implementation
```

The engine must not invert this flow by starting with products, portfolios, or generic score dimensions.

---

## 3. Responsibilities by layer

### 3.1 Financial State

Input facts only: income, expenses, surplus/deficit, assets, liabilities, liquidity position, existing funding assets and other persisted investor facts.

Do not convert Financial State directly into a strategy without a goal.

### 3.2 Defined Goal

The goal is the strategic context. At minimum the engine needs:

- goal type / normalized goal key
- target date / horizon
- target amount or retirement-specific required corpus
- funding status
- funding gap / surplus
- existing mapped assets
- flexibility / constraints

Retirement must use the corrected retirement-specific corpus calculation already protected by tests. Do not regress to the old annual-expense-only target calculation.

### 3.3 Rule / Eligibility Engine

This layer answers:

> Which strategies are applicable for this goal and financial state?

Rules are deterministic and explainable. Each rule should return evidence/diagnostics rather than silently changing a score.

Examples of rule concepts:

- goal type applicability
- time horizon
- funding shortfall / surplus
- cash-flow requirements
- existing assets available for the goal
- debt constraints
- liquidity requirements
- feasibility constraints
- retirement-specific requirements

Eligibility is a gate. A strategy that is not applicable must not enter ranking/comparison simply because it has a high generic dimension score.

### 3.4 Strategy Library

A strategy is a reusable architecture for achieving a goal. Examples include:

- cash-flow matching
- debt reduction / debt-first funding
- progressive de-risking
- bucket strategy
- retirement glide path
- goal funding from existing assets + future contributions

The library must be extensible. Strategy definitions should describe applicability, constraints, intended outcome, trade-offs and implementation concepts.

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

The decision layer compares **eligible strategies**, using explicit evidence such as:

- eligibility
- goal fit
- funding fit
- implementation complexity
- liquidity implications
- constraint compatibility
- assumptions
- trade-offs
- stress-test behavior
- feasibility

`Safety`, `Liquidity`, `Growth`, and `Flexibility` may remain as descriptive attributes/evidence where useful, but they must NOT be the primary strategy-selection mechanism and must NOT be presented as the strategy itself.

### 3.8 Recommendation

Recommendation must identify:

- recommended strategy architecture
- why it fits this goal/investor
- applicable constraints
- key assumptions
- important trade-offs
- alternative eligible architectures
- feasibility status

Recommendation must remain goal-level. Product and portfolio selection happen downstream.

---

## 4. Legacy behavior to remove from decision authority

The current ranking implementation calculates:

```text
Composite Score = normalized safety weight * safety score
               + normalized liquidity weight * liquidity score
               + normalized growth weight * growth score
               + normalized flexibility weight * flexibility score
```

and sorts scenarios by that composite score. This is legacy behavior and must no longer determine the selected strategy.

The current implementation is visible in `backend/engines/strategy/ranking.py` and must be converted rather than cosmetically renamed.

Do NOT:

- rename the four dimensions and keep the same formula;
- replace the composite score with another arbitrary weighted score;
- treat a scenario as a strategy;
- make the highest numeric score automatically the recommendation;
- use risk profiling as a substitute for strategy eligibility;
- select a financial product before the strategy architecture exists.

---

## 5. Target data contract

A Strategy Run should conceptually contain:

```text
Defined Goal snapshot
Financial State snapshot / relevant evidence
Eligible strategies
Ineligible strategies + reasons where useful
Strategy architectures
Variants / scenarios
Comparison evidence
Trade-offs
Assumptions
Stress-test outputs
Recommendation
Diagnostics
```

Every selected recommendation must be traceable to the rule/eligibility evidence and the comparison evidence that produced it.

The run must remain reproducible from its persisted inputs.

---

## 6. Retirement-specific requirements

Retirement is a distinct goal type, not merely a generic future-expense goal.

The retirement pipeline must account for:

- investor date of birth / current age from Personal Information
- retirement target date
- desired lifestyle monthly expense
- inflation until retirement
- retirement-date expense
- life expectancy
- post-retirement horizon
- retirement-period return assumption where defined by the engine
- existing mapped retirement assets
- funding gap / surplus

The output must distinguish at least:

1. today's expense,
2. retirement-date required income/expense,
3. required retirement corpus,
4. existing mapped assets,
5. funding gap,
6. required contribution where applicable.

A single inflation-adjusted annual expense is NOT a retirement corpus.

---

## 7. Strategy Builder UI contract

The UI must represent the new architecture.

### Remove as strategy identity

Do not display cards/headings implying that a strategy is:

- Safety
- Liquidity
- Growth
- Flexibility

Do not display these as competing strategy names.

### Display instead

For each eligible strategy:

- Strategy name
- What it does
- Why it is applicable
- Goal fit
- Key constraints
- Main trade-offs
- Important assumptions
- Techniques used
- Feasibility
- Stress-test summary
- Implementation direction

Dimension scores can be retained only if they are explicitly labeled as supporting evidence and are not used as the strategy identity or sole decision criterion.

### Recommended presentation

```text
Strategy Run

Goal: Retirement / Financial Freedom

Applicable Strategies

1. Retirement Glide Path
   Purpose
   Why applicable
   Trade-offs
   Constraints
   Techniques
   Stress behavior

2. Cash-Flow Matching
   Purpose
   Why applicable
   Trade-offs
   Constraints
   Techniques
   Stress behavior

Recommendation
   Selected architecture
   Reasoning
   Alternatives
```

---

## 8. Goal Planner → Strategy Builder contract

Goal Planner is the source of truth for the saved Defined Goal.

When Strategy Builder opens:

1. Load the latest saved Defined Goal.
2. Verify the goal version against the existing Strategy Run.
3. If there is no run or the run is based on an older goal version, automatically build a fresh Strategy Run.
4. Do not require the user to manually rebuild merely because the saved goal changed.
5. Persist immutable run versions for history.

The Strategy Builder must never silently display a stale run for a changed goal.

---

## 9. Tests and conversion order

The project has intentionally followed a test-first/refactor-second process. Preserve that discipline.

Conversion order:

### Phase A — Contract protection

Keep all current tests green before each conversion batch.

### Phase B — Strategy eligibility

Convert strategy applicability from legacy score-driven behavior to explicit rule outputs.

Acceptance criteria:

- inapplicable strategies are excluded;
- applicable strategies are returned;
- diagnostics explain important exclusions;
- retirement rules are recognized consistently, including normalized goal labels.

### Phase C — Strategy architecture

Move reusable strategy definitions into the Strategy Library contract.

Acceptance criteria:

- strategy != scenario;
- strategy != product;
- strategy may contain techniques;
- strategy may have variants;
- strategy has explicit applicability/constraints/trade-offs.

### Phase D — Comparison / decision

Replace composite-dimension ranking as decision authority.

Acceptance criteria:

- no automatic selection based solely on safety/liquidity/growth/flexibility;
- eligible strategy comparison is explainable;
- recommendation references goal fit and constraints;
- alternatives remain visible.

### Phase E — Recommendation

Update recommendation generation so it consumes the new decision output rather than a legacy ranked scenario list.

Current `backend/engines/strategy/recommendation.py` still expects `ranked_items[0]` and derives a dominant priority from the four legacy dimensions. This must be converted.

### Phase F — API/service persistence

Update Strategy Run payloads, service orchestration and persistence only as required by the new contracts. Do not create unnecessary schema changes.

### Phase G — Frontend

After backend contracts stabilize, update Strategy Builder UI to render strategies/architectures rather than dimension-score cards.

### Phase H — Reports

Retirement Report and PDF renderer must consume the final Strategy Run/recommendation contract. They must not reconstruct strategy decisions independently.

---

## 10. Regression requirements

Every conversion batch must preserve:

- existing goal calculation behavior outside the intended retirement correction;
- corrected retirement calculation;
- Goal Planner → Strategy Builder handoff;
- automatic fresh run when the goal version changes;
- strategy eligibility;
- strategy recommendation traceability;
- report generation;
- PDF rendering;
- CI test suite.

Add regression tests whenever a previously observed bug is fixed.

Known regressions that must remain covered:

- retirement goal label normalization (`Retirement / Financial Freedom` vs equivalent normalized key);
- stale Strategy Run after a saved goal change;
- retirement corpus must not collapse to the old ~₹26.1L annual-expense-style target;
- no-strategy state must be distinguishable from an implementation failure.

---

## 11. Definition of Done

Conversion is complete only when all are true:

- [ ] Rule/eligibility layer determines applicability.
- [ ] Strategy Library contains reusable goal-level architectures.
- [ ] Techniques are separate from strategies.
- [ ] Strategy variants/scenarios are separate from strategy identity.
- [ ] Safety/Liquidity/Growth/Flexibility are no longer the strategy-selection engine.
- [ ] Composite score is no longer the decision authority.
- [ ] Recommendation is explainable and goal-specific.
- [ ] Goal version changes automatically invalidate/rebuild stale runs.
- [ ] Retirement uses the dedicated corpus calculation.
- [ ] Strategy Builder UI displays strategy architectures, not dimension-score identities.
- [ ] Report renderer consumes the final strategy output.
- [ ] PDF output remains functional.
- [ ] Existing and new regression tests pass.
- [ ] CI is green.

---

## 12. Important implementation rule

Do not perform a broad rewrite just to satisfy this document. Convert one bounded contract at a time, run the relevant tests, then CI, and only then proceed to the next layer.

The objective is **architectural conversion with behavioral safety**, not a cosmetic refactor.
