# 08 — Stress / Resilience: Current State & Recommendation

> **Current-state audit only — not target policy:** Any Goal Funding / `strat-goal-funding` Strategy row, variant, candidate, or behavior described below records legacy runtime observed during audit. Canonical target ownership is Goal Planner / Goal Feasibility; Goal Funding is not a Strategy Builder strategy. Follow `docs/implementations/Strategy-Builder.md` and `docs/Real-Life Decision Cases/strategy-decision-tree.md` for target rules. Preserve these observations as audit evidence; do not implement them as target behavior.


## 1. Purpose

This document records the current code-verified Stress / Resilience capability and the recommended target contract for the PlanVesto Canonical Decision Engine.

This is a design/audit document only. Stress/resilience rules are not frozen and no refactor is authorized by this document.

Final business behavior will be frozen later through real-life cases.

## 2. Scope

This step answers:

> After a strategy, variant, technique set and architecture are selected, how do we test whether the decision remains workable when important conditions change?

It covers:
- current what-if capability,
- current stressed baseline scenario,
- current limitations,
- recommended stress framework,
- resilience outcomes,
- re-selection policy,
- audit requirements.

It does not freeze the final recommendation contract.

## 3. Current Stress-Related Capabilities

The current code has **scenario sensitivity/what-if functionality**, but it does not yet establish a complete canonical Stress / Resilience Decision Engine.

The main implementation is:

`backend/engines/strategy/scenario.py`

The StrategyEngine calls:

`generate_baseline_scenarios()`

and:

`generate_what_if_scenarios()`

before final strategy selection.

## 4. Current Baseline Stress Scenario

For non-Goal-Funding strategies, baseline scenario generation currently creates:

1. Recommended Baseline
2. Conservative Hedged Variant

The second scenario increases inflation by **1.5 percentage points** and recalculates the future target.

Its scenario name is:

**Conservative Hedged Variant**

and its market condition is recorded as:

**Stressed Market (+1.5% Inflation Drag)**

This is a useful stress-oriented scenario, but it is only one deterministic inflation shock.

It is not yet a general stress framework.

## 5. Current What-If Scenarios

The current engine generates exploratory what-if scenarios.

The code describes them explicitly as:

> exploratory what-ifs, not recommendations.

They change planning variables one at a time and calculate deterministic funding consequences.

Current what-if coverage includes contribution sensitivity and other funding/horizon/return/inflation-related changes implemented in `scenario.py`.

These scenarios are useful for decision sensitivity but are not currently a formal resilience assessment.

## 6. Important Distinction

The system currently has:

### What-if

Question:

> “What happens if this one input changes?”

### Stress / Resilience

Question:

> “Does the selected plan remain viable when adverse conditions occur, including combinations of adverse conditions?”

These are not the same capability.

The current code supports the first much more clearly than the second.

## 7. Current Runtime Position

The current StrategyEngine flow is approximately:

**Applicable Strategies**
→ **Baseline Scenarios**
→ **What-if Scenarios**
→ **Architecture Composition**
→ **Technique Execution**
→ **Strategy Decision**
→ **Ranking**
→ **Recommendation**

Therefore what-if scenarios are currently generated as decision-support data, but they do not form a separate resilience gate after the final architecture is selected.

## 8. Current Resilience Gaps

### Gap 1 — No canonical stress taxonomy

There is no verified central rule registry defining standard stress types such as:

- income reduction,
- expense increase,
- return reduction,
- inflation increase,
- earlier goal date,
- delayed goal date,
- asset unavailability,
- debt/EMI increase,
- liquidity reduction.

### Gap 2 — No correlated stress framework

Current what-ifs are primarily single-variable sensitivity scenarios.

There is no verified canonical mechanism for combinations such as:

**income ↓ + expenses ↑ + returns ↓**

### Gap 3 — No formal resilience classification

There is no verified canonical final status such as:

- Robust
- Conditional
- Fragile

for the selected plan.

### Gap 4 — No explicit strategy stability test

The current system does not establish a canonical rule answering:

> Does the recommendation remain the same under defined stress conditions?

### Gap 5 — No formal re-selection policy

If stress changes the preferred strategy, the current architecture does not yet define a formal:

**Stress → Re-evaluate → Re-select Strategy → Re-select Variant → Re-compose Architecture**

cycle.

### Gap 6 — Hard constraints are not explicitly stress re-evaluated as a resilience gate

The system has centralized hard-constraint evaluation, but a dedicated stress loop that re-runs the same canonical gates under shocked inputs is not established.

## 9. Recommended Target Stress Flow

After the base decision:

**Selected Strategy**
↓
**Selected Variant**
↓
**Selected Techniques**
↓
**Final Architecture**
↓
**Stress Scenario Set**
↓
**Re-run Hard Constraints**
↓
**Re-run 8 Eligibility Fits**
↓
**Re-run Strategy Selection if required**
↓
**Re-run Variant Selection if strategy changes**
↓
**Re-compose Architecture if required**
↓
**Measure Outcome Stability**
↓
**Resilience Classification**

This should use the same canonical decision rules as the base case.

## 10. Recommended Stress Categories

The future canonical stress library should explicitly define shocks such as:

| Stress | Example |
|---|---|
| Income shock | Income -10%, -20% |
| Expense shock | Expenses +10%, +20% |
| Return shock | Expected return reduced materially |
| Inflation shock | Inflation materially higher |
| Goal-date shock | Goal date brought forward |
| Goal-delay shock | Goal date delayed |
| Asset shock | Mapped asset unavailable/reduced |
| Debt shock | EMI/debt burden increases |
| Liquidity shock | Available liquid resources reduced |

Exact percentages are **TO DECIDE**.

They should be frozen only after real-life validation.

## 11. Recommended Correlated Stress Cases

Single shocks are insufficient.

The framework should support combined scenarios such as:

### Moderate adverse case

Income ↓ + Expenses ↑

### Market adverse case

Returns ↓ + Inflation ↑

### Severe planning case

Income ↓ + Expenses ↑ + Returns ↓

### Goal-pressure case

Goal date earlier + Inflation ↑ + Asset value ↓

### Debt-pressure case

Income ↓ + EMI burden ↑ + Liquidity ↓

The exact combinations should be business-defined rather than invented by the engine.

## 12. Recommended Stress Evaluation

For every stress case, calculate:

1. Goal feasibility
2. Funding gap
3. Required contribution
4. Cash-flow resilience
5. Liquidity resilience
6. Debt/EMI safety
7. Hard-constraint status
8. Eight-fit eligibility status
9. Strategy stability
10. Variant stability
11. Architecture feasibility

The same canonical decision rules should be re-used.

Stress testing should not create a second decision system.

## 13. Recommended Resilience Classification

A future canonical classification could be:

### Robust

The selected strategy remains viable and the architecture remains feasible across defined stress cases.

### Conditional

The strategy remains viable only after defined changes, or some stresses produce conditional eligibility.

### Fragile

One or more material stress cases cause hard-constraint failure, no viable strategy, or infeasible architecture.

These are recommendations only and are **not frozen**.

## 14. Recommended Strategy Stability Measure

The system should record whether the base strategy survives each stress case.

Example:

| Stress | Base Strategy | Stress Strategy | Stable? |
|---|---|---|---|
| Income -10% | Goal Funding | Goal Funding | Yes |
| Income -20% | Goal Funding | Debt Reduction | No |
| Inflation +2% | Goal Funding | Goal Funding | Yes |

This makes resilience explainable to the investor.

## 15. Recommended Re-selection Rule

If stress causes:

- hard-constraint failure,
- eligibility failure,
- architecture infeasibility,
- or materially different strategy suitability,

the system should re-run the canonical decision pipeline.

Conceptually:

**Stress → Same Inputs + Shock → Same Decision Engine → New Decision**

Not:

**Stress → Separate ad-hoc recommendation rule**

This keeps the system canonical.

## 16. Recommended Stress Result Object

The future result should conceptually contain:

- stress scenario ID,
- shocked inputs,
- base decision,
- stress decision,
- hard-constraint results,
- eight-fit results,
- strategy before/after,
- variant before/after,
- architecture status,
- funding gap before/after,
- required contribution before/after,
- resilience classification,
- explanation.

This provides an auditable answer to:

> “What happens to my plan if conditions worsen?”

## 17. Current vs Recommended Ownership

| Responsibility | Current state | Recommended authority |
|---|---|---|
| Scenario generation | strategy/scenario.py | Canonical Stress Scenario rules |
| What-if calculations | scenario engine | Preserve as sensitivity layer |
| Stress definitions | Not centralized | Canonical Stress rules |
| Stress execution | Not a separate engine | Stress/Resilience Engine |
| Hard constraints under stress | Existing constraint engine | Reuse unchanged |
| Eligibility under stress | Existing eligibility engine | Reuse unchanged |
| Strategy re-selection | Not formally defined | Same Decision Engine |
| Variant re-selection | Not formally defined | Same Variant rules |
| Architecture re-composition | Not formally defined | Same Architecture rules |
| Resilience status | Not centralized | Canonical Resilience policy |
| Investor explanation | Recommendation layer | Preserve downstream role |

## 18. Recommended Architecture Principle

Stress testing must **not become a parallel decision engine**.

It should be a controlled replay of the same canonical decision pipeline under changed inputs.

This is the key architectural rule:

> **One Decision Engine, multiple input states.**

Base case and stressed cases should therefore use the same:
- applicability rules,
- hard constraints,
- eligibility fits,
- strategy selection,
- variant selection,
- technique selection,
- architecture rules.

Only the inputs/scenario state changes.

## 19. Real-Life Validation Cases Before Freezing

Validate at minimum:

1. Base plan survives mild income reduction.
2. Base plan fails under severe income reduction.
3. Expense increase causes contribution shortfall.
4. Return reduction increases funding gap.
5. Inflation increase changes required corpus.
6. Earlier goal date changes strategy.
7. Delayed goal date changes variant.
8. Existing asset becomes unavailable.
9. EMI increases.
10. Liquidity reserve falls.
11. Combined income + expense shock.
12. Combined return + inflation shock.
13. Severe multi-variable shock.
14. Stress causes eligibility PASS → CONDITIONAL.
15. Stress causes PASS → FAIL.
16. Stress changes primary strategy.
17. Stress changes variant but not strategy.
18. Stress changes architecture but not strategy.
19. Stress causes no viable strategy.
20. Recovery scenario restores original strategy.

For every case record:

**Base Inputs → Stress → Base Decision → Stress Decision → Constraint Changes → Eligibility Changes → Strategy Changes → Variant Changes → Architecture Changes → Resilience Status**

## 20. What Should NOT Be Frozen Yet

Do not freeze solely from current code:

- exact shock percentages,
- exact stress combinations,
- number of stress cases,
- resilience thresholds,
- Robust/Conditional/Fragile definitions,
- whether every stress must trigger full re-selection,
- materiality threshold for strategy change,
- recovery scenario rules,
- investor-visible stress scenarios,
- whether stress affects final recommendation automatically.

## 21. Current vs Recommended Summary

| Area | Current state | Recommendation |
|---|---|---|
| What-if | Implemented | Preserve as sensitivity layer |
| Baseline stress | Limited inflation stress | Expand carefully |
| Stress taxonomy | Not centralized | Create canonical stress rules |
| Correlated shocks | Not established | Add |
| Constraint replay | Existing engine | Reuse |
| Eligibility replay | Existing engine | Reuse |
| Strategy re-selection | Not formalized | Reuse canonical Decision Engine |
| Variant re-selection | Not formalized | Reuse canonical Variant rules |
| Architecture re-composition | Not formalized | Reuse canonical Architecture rules |
| Resilience classification | Not established | Create canonical policy |
| Auditability | Scenario data exists | Add base-vs-stress decision record |

## 22. Decision Status

**CURRENT STATUS: DOCUMENTED — NOT FROZEN**

The repository already has useful scenario and what-if infrastructure, but it does **not yet have a complete canonical Stress / Resilience Decision Engine**.

The recommended direction is not to build a second decision system. It is to replay the same canonical Decision Engine under controlled adverse input states and measure whether the strategy, variant and architecture remain viable.

**Next step: Step 9 — Final Decision & Recommendation: Current State & Recommendation.**
