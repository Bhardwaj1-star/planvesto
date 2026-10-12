# 09 — Final Decision & Recommendation: Current State & Recommendation

## 1. Purpose

This document records the current code-verified Final Decision and Recommendation layer of PlanVesto and defines the recommended target contract for the future Canonical Decision Engine.

This is a design/audit document only.

No decision rule is frozen by this document and no refactor is authorized by it.

Business rules will be frozen later through real-life validation.

## 2. Scope

This step answers:

> After all gates, eligibility fits, strategy candidates, variants, techniques, architecture and resilience evidence have been evaluated, what exactly becomes the final decision shown to the investor?

It covers:
- current decision authority,
- recommendation generation,
- alternative strategy handling,
- feasibility status,
- explanation/evidence,
- final output ownership,
- stress/resilience interaction,
- recommended final decision contract.

## 3. Current Decision Authority

The current runtime decision authority is:

`backend/engines/strategy/decision.py::evaluate_decision()`

It produces a `DecisionResult`.

The current flow is broadly:

**Applicable Strategies**
→ **Scenarios**
→ **Architecture Candidates**
→ **8-Fit Eligibility**
→ **Eligibility Gate**
→ **Decision Score**
→ **Best Architecture / Strategy**
→ **Recommendation**

The separate ranking layer is not the final authority.

## 4. Current Selection Logic

Current code establishes this precedence:

1. Evaluate candidate architectures.
2. Evaluate all eight eligibility fits.
3. A failed eligibility gate produces FAIL.
4. PASS candidates form the preferred pool.
5. CONDITIONAL candidates are considered only when no PASS exists.
6. FAIL candidates are never recommended.
7. The highest decision score wins within the selected pool.
8. One alternative architecture may be retained.

Therefore the current decision principle is:

**PASS > CONDITIONAL > FAIL**

followed by the current composite decision score.

## 5. Current Decision Score

The current decision score combines:

- Goal Fit
- Horizon Fit
- Funding Fit
- Feasibility
- Component Fit
- Technique Execution

The current feasibility values are:

| Status | Score |
|---|---:|
| PASS | 15 |
| CONDITIONAL | 8 |
| FAIL | 0 |

A failed candidate receives an infeasible decision score of **-1000**.

The current score weights and values are implementation policy, not yet a fully canonical business rule set.

## 6. Current Recommendation Layer

`backend/engines/strategy/recommendation.py` consumes `DecisionResult`.

It does **not** simply take the first ranking item.

It adds:
- funding context,
- financial-state diagnostics as explanatory evidence,
- supporting-strategy explanation,
- canonical strategy good-outcome text,
- selected variant information,
- architecture,
- alternative architecture IDs,
- feasibility,
- constraints.

This is directionally correct: recommendation is downstream of the decision.

## 7. Current Variant Placement

The current recommendation layer calls:

`VariantSelector.select_variant()`

after the strategy decision has already been made.

Therefore the runtime currently behaves approximately as:

**Strategy Decision → Recommendation → Variant Selection → Recommendation Output**

The target architecture should make variant selection an explicit decision stage before final recommendation.

## 8. Current Ranking Role

`backend/engines/strategy/ranking.py` explicitly treats `DecisionResult` as authoritative.

Its composite safety/liquidity/growth/flexibility score is descriptive evidence and does not override the decision order.

This separation should be preserved.

## 9. Current Alternative Handling

The current decision engine returns at most one alternative architecture.

The recommendation exposes its architecture IDs.

This is useful but the business question is still open:

> Should the investor receive one alternative, multiple alternatives, or only a materially different alternative?

This should be frozen through real-life examples.

## 10. Current Feasibility Meaning

The current recommendation exposes:

- `feasible`
- `conditional`
- `infeasible`

These statuses currently come from decision/architecture evaluation.

However, the exact boundary between:
- eligibility,
- feasibility,
- implementation readiness,
- stress resilience,

is not yet fully centralized.

That boundary must be clarified before the final contract is frozen.

## 11. Current Explanation Model

The current recommendation contains two explanation levels:

### Short reasons

A concise set of decision reasons, including:
- goal-specific rationale,
- funding state,
- relevant financial diagnostics,
- supporting strategy explanation,
- strategy outcome.

### Complete reasoning

The decision engine's reasoning plus critical financial-state considerations.

This is appropriate for separating:
- investor-facing explanation,
- deeper audit evidence.

## 12. Current Decision Snapshot

The strategy service persists a decision snapshot when a StrategyVersion is finalized.

The snapshot includes:
- selected scenario,
- applicable strategies,
- scenarios,
- what-if scenarios,
- investor priorities,
- comparison matrix,
- rankings,
- recommendation,
- technique outputs.

This is important because final decisions need an auditable historical record.

## 13. Important Current Mismatch

The code contains a policy module:

`backend/rules/strategy_decision.py`

which is described as an authoritative decision/scoring policy surface.

However, some of its strategy IDs are stale and do not match the current canonical five strategies.

Current canonical strategy IDs are:

1. `strat-goal-funding`
2. `strat-progressive-de-risking`
3. `strat-capital-preservation`
4. `strat-debt-reduction`
5. `strat-credit-utilisation`

The policy module still contains older IDs such as:
- `strat-dynamic-accumulation`
- `strat-calibrated-growth`
- `strat-high-liquidity-flex`
- `strat-cap-preservation`

Therefore this file cannot currently be treated as the complete canonical final-decision rulebook.

## 14. Recommended Final Decision Contract

The future Canonical Decision Engine should produce one authoritative final decision object containing:

### Decision Identity
- decision/run ID,
- goal ID,
- defined-goal version,
- decision-engine version.

### Selected Path
- primary strategy,
- selected variant,
- selected techniques,
- final architecture.

### Decision Evidence
- applicability result,
- hard-constraint result,
- eight-fit results,
- strategy comparison,
- selection rationale,
- alternative path(s).

### Feasibility
- implementation feasibility,
- constraints,
- required changes.

### Resilience
- stress-test result,
- strategy stability,
- variant stability,
- architecture stability,
- resilience classification.

### Investor Explanation
- recommendation,
- why it was selected,
- what must be done,
- key trade-offs,
- what could change the recommendation.

## 15. Recommended Final Decision Flow

The target canonical pipeline should be:

**Goal**
↓
**Goal Classification**
↓
**Hard Constraint Gate**
↓
**Strategy Applicability**
↓
**8-Fit Eligibility**
↓
**Strategy Selection**
↓
**Variant Selection**
↓
**Technique Selection**
↓
**Architecture Composition**
↓
**Stress / Resilience**
↓
**Re-selection if required**
↓
**Final Decision**
↓
**Investor Recommendation**

The key point is that **Recommendation is the final presentation of a decision, not the place where new decision rules are invented.**

## 16. Stress / Resilience Interaction

Stress testing should not independently create a recommendation.

Instead:

**Base Decision**
→ **Stress**
→ **same Decision Engine**
→ **compare result**
→ **reselect only when defined policy requires it**
→ **Final Decision**

This preserves one decision authority.

## 17. Recommended Decision Outcomes

The final engine should conceptually return one of:

### Recommended

A strategy/variant/architecture is viable and satisfies the frozen decision policy.

### Recommended with Conditions

A viable path exists, but specified changes are required.

### No Viable Recommendation

All candidates fail the applicable decision gates.

Exact labels are **TO DECIDE**.

## 18. Recommended Alternative Policy

Alternatives should be generated only from materially different viable paths.

An alternative should answer:

> “If the investor does not follow the primary recommendation, what is the next viable path and what trade-off does it introduce?”

Do not expose alternatives merely because another architecture received a score.

The exact number and materiality threshold are **TO DECIDE**.

## 19. Recommended Decision Evidence Hierarchy

The future system should distinguish:

1. **Hard constraints** — can block/downgrade according to policy.
2. **Eligibility fits** — determine suitability.
3. **Decision factors** — distinguish viable candidates.
4. **Stress evidence** — tests stability.
5. **Diagnostics** — explain financial condition.
6. **Investor preferences** — influence permitted ranking/choice.
7. **Narrative evidence** — explains the result.

This prevents diagnostic information from accidentally becoming a decision rule.

## 20. Recommended Ownership

| Responsibility | Current authority | Recommended authority |
|---|---|---|
| Goal classification | `rules/goals.py` | Canonical Goal rules |
| Hard constraints | Constraints engine | Canonical Constraint policy |
| Applicability | StrategyRuleEngine + library metadata | Canonical Applicability rules |
| 8 fits | Strategy eligibility engine | Canonical Eligibility policy |
| Strategy selection | `engines/strategy/decision.py` | Canonical Strategy Selection policy |
| Variant selection | VariantSelector | Canonical Variant rules |
| Technique selection | Architecture/library + TechniqueEngine | Canonical Technique rules |
| Architecture | Composition engine | Canonical Architecture rules |
| Stress | Scenario engine / what-if | Canonical Stress/Resilience rules |
| Final decision | DecisionResult | Canonical Decision Engine |
| Recommendation | Recommendation engine | Presentation/explanation layer |
| Audit snapshot | Strategy service | Immutable decision snapshot |

## 21. Real-Life Validation Cases Before Freezing

At minimum validate:

1. One clearly viable strategy.
2. Two viable strategies with different trade-offs.
3. One PASS and one CONDITIONAL.
4. Only CONDITIONAL strategies available.
5. All strategies FAIL.
6. Hard constraint blocks a candidate.
7. Eligibility fit blocks a candidate.
8. Same strategy, different variant.
9. Same strategy/variant, different techniques.
10. Same strategy but different architecture.
11. Stress keeps recommendation unchanged.
12. Stress changes variant.
13. Stress changes strategy.
14. Stress makes all strategies infeasible.
15. Financial diagnostics are critical but should not become a hidden selection rule.
16. Investor priorities change ranking without violating hard gates.
17. One alternative is materially useful.
18. No alternative is materially different.
19. Defined Goal version changes and decision is recalculated.
20. Finalized StrategyVersion preserves the exact decision snapshot.

## 22. What Should NOT Be Frozen Yet

Do not freeze solely from current code:

- exact score weights,
- exact decision-score formula,
- technique execution contribution,
- PASS vs CONDITIONAL policy,
- number of alternatives,
- alternative materiality threshold,
- investor-priority influence,
- feasibility definitions,
- stress-triggered reselection threshold,
- resilience thresholds,
- final investor-facing status labels,
- exact explanation content,
- final Decision object schema.

## 23. Overall Canonical Decision Engine Sequence

The nine documented decision domains now form one coherent target sequence:

**01 Strategy Applicability**
→ **02 Hard Constraints**
→ **03 8 Eligibility Fits**
→ **04 Strategy Selection**
→ **05 22 Variant Selection**
→ **06 Technique Selection**
→ **07 Architecture Composition**
→ **08 Stress / Resilience**
→ **09 Final Decision & Recommendation**

This is the documentation/design sequence.

It is not yet the implementation sequence.

## 24. Implementation Principle

The next phase should not begin by rewriting every engine.

First freeze the business policy through real-life cases.

Then refactor each existing implementation toward the frozen canonical ownership, with behavior-preserving tests.

The desired end state is:

**Canonical Rules define the decision.**

**Decision Engine executes the decision.**

**Library defines available strategies/variants/techniques.**

**Engines calculate/execute.**

**Recommendation explains the decision.**

**Decision Snapshot records exactly what happened.**

## 25. Definition of Done for the Decision Engine

The Decision Engine should be considered complete only when:

- every decision stage has one canonical owner,
- no stale strategy IDs remain in decision policy,
- applicability is separate from eligibility,
- hard constraints are separate from diagnostics,
- all eight fits have explicit policy,
- strategy selection has one authority,
- all 22 variants have deterministic canonical selection,
- technique selection has explicit ownership,
- architecture composition is downstream of technique selection,
- stress/resilience reuses the same decision logic,
- final recommendation cannot silently create a new decision,
- alternatives follow a defined policy,
- every decision is auditable from an immutable snapshot,
- real-life validation cases pass,
- frontend and backend consume the same canonical decision output.

## 26. Final Status

**DOCUMENTED — NOT FROZEN**

The current code already contains a substantial decision pipeline, but decision authority is distributed across policy modules, engines, library metadata, recommendation logic and legacy compatibility surfaces.

The target is not a larger Strategy Builder.

The target is a **PlanVesto Canonical Decision Engine** in which the Strategy Builder becomes one decision domain and the final recommendation is simply the explainable output of that canonical decision.

**Documentation phase complete: Steps 1–9. Next phase: Business Rule Freeze through real-life cases, followed by controlled refactor.**


---

## 27. Verification Corrections — Final Decision Boundary

The full code verification confirms the following current-state corrections:

1. `DecisionResult` remains the authoritative decision contract, but its upstream inputs are not yet fully canonical because legacy scoring IDs remain active.
2. `InvestorPriorities` is persisted in the decision snapshot and passed into the decision function, but it currently has no effect inside `evaluate_decision()`; its current scoring effect is downstream in ranking.
3. Variant selection currently occurs inside recommendation after strategy decision, so recommendation is not purely explanatory in the strict architectural sense yet.
4. Architecture and technique execution already occur before `evaluate_decision()` in the current runtime, so the target flow in this document is a future design sequence, not a current execution trace.
5. The final decision layer should therefore distinguish **current runtime authority** (`DecisionResult`) from **future canonical decision order**.

These are documentation corrections to current-state description. They do not freeze the future business policy.

