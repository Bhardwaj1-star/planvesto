# 02 — Hard Constraints: Current State & Recommendation

## 1. Purpose

This document records the **current code-verified state** of hard constraints in PlanVesto and the recommended target structure for the Canonical Decision Engine.

This is a **design/audit document only**. No business rule is frozen here and no refactor is authorized by this document. Final rules will be frozen later using real-life cases.

## 2. Audit Scope

Source of truth for this audit: backend code.

Reviewed areas include:
- `backend/engines/constraints/policy.py`
- `backend/engines/constraints/evaluator.py`
- `backend/engines/constraints/models.py`
- `backend/engines/constraints/aggregator.py`
- `backend/engines/constraints/adapters.py`
- `backend/engines/rules/engine.py`
- `backend/rules/canonical.py`
- strategy decision/eligibility consumers of `ConstraintSet`

The question is specifically: **what can actually block or restrict planning, where is that rule owned today, and what should become the canonical Decision Engine contract?**

---

## 3. What “Hard Constraint” Means in the Current System

A hard constraint is a condition whose failure can block or materially restrict downstream planning.

The current code distinguishes hard constraints from:
- warnings,
- diagnostics,
- recommendation evidence,
- strategy eligibility,
- architecture constraints.

This distinction is important and should remain explicit.

The current constraint model defines:
- `hard` — blocks downstream processing,
- `eligibility` — determines strategy eligibility,
- other roles for ranking/recommendation/evidence.

The current canonical rule registry also defines `HARD_CONSTRAINT` as a distinct rule role.

---

## 4. Current Canonical Constraint Ownership

### 4.1 Constraint policy

Current policy ownership is centralized in:

`backend/engines/constraints/policy.py`

It currently owns:
- constraint rule IDs,
- threshold constants,
- priority semantics,
- constraint source priority,
- constraint normalization,
- conflict detection,
- constraint priority validation.

Examples of centralized thresholds include:
- Emergency reserve critical: **< 3 months**
- Emergency reserve healthy: **>= 6 months**
- DTI critical: **> 40%**
- DTI healthy: **<= 30%**
- Savings-rate healthy benchmark: **20%**

This is a strong existing foundation for canonicalization.

### 4.2 Constraint evaluation

Current financial/goal constraint evaluation is owned by:

`backend/engines/constraints/evaluator.py`

It evaluates:
1. financial ratios,
2. goal validity constraints,
3. emergency-reserve constraints,
4. debt-burden constraints,
5. savings-rate warnings.

The evaluator produces typed constraint results and separates:
- constraints,
- hard constraints,
- warnings,
- suggested priority overrides.

### 4.3 Constraint aggregation

Current aggregation flow is:

**Domain Engines → Constraint Adapters → Canonical Constraints → ConstraintSet**

The aggregator combines constraint layers into a single `ConstraintSet`.

This is the current central container consumed by the Strategy Engine and downstream planning layers.

---

## 5. Current Hard Constraints Identified in Code

| Constraint | Current condition | Current effect | Current owner | Status |
|---|---|---|---|---|
| Goal Positive Horizon | Goal duration must be > 0 | Goal validity failure | `FinancialRatioConstraintEvaluator.evaluate_goal_constraints()` | Actual hard constraint |
| Goal Positive Target | Future target must be > 0 | Goal validity failure | `FinancialRatioConstraintEvaluator.evaluate_goal_constraints()` | Actual hard constraint |
| Emergency Reserve Critical | Emergency coverage < 3 months + discretionary goal has critical/high priority | Goal priority is demoted to low; discretionary allocation is constrained | `FinancialRatioConstraintEvaluator.assess_constraints()` | Actual hard constraint |
| Debt Burden Exceeded | DTI > 40% + discretionary goal has critical/high priority | Goal priority is demoted to low; solvency/debt serviceability takes precedence | `FinancialRatioConstraintEvaluator.assess_constraints()` | Actual hard constraint |
| Discretionary Cannot Preempt Essential | Discretionary commitment cannot preempt essential/safety funding | Prevents discretionary priority from overriding essential funding | `engines.constraints.policy.can_discretionary_preempt_essential()` | Canonical policy exists |
| Constraint conflicts | Same constraint key has conflicting values from different sources | Conflict remains unresolved; hard presence is retained | `ConstraintRules.conflicts()` | Constraint-governance rule, not itself a financial threshold |

### Important observation

The Emergency Reserve and DTI rules are **not universal “block every goal” rules** in the current implementation.

They apply specifically when:
- the condition is critical, and
- the goal is discretionary, and
- the goal priority is critical/high.

The current action is priority demotion to low rather than deletion of the goal.

This behavior must not be silently changed during refactoring.

---

## 6. Current Warnings / Diagnostics — Not Hard Constraints

The current code also produces conditions that should **not** be confused with hard constraints.

| Current signal | Current treatment | Why it is different |
|---|---|---|
| Emergency coverage in attention range | Warning | Indicates a recommended buffer is below target but does not hard-block planning |
| DTI in attention range | Warning | Indicates elevated debt pressure but is not a hard failure |
| Savings rate below benchmark | Warning | Indicates cash-flow pressure; currently does not hard-block a goal |
| Surplus health | Recommendation/diagnostic evidence | Used to explain planning pressure; not a universal hard gate |
| Emergency reserve health diagnostic | Diagnostic | Reports financial condition; missing data does not create a false hard failure |
| Liquidity health | Diagnostic | Health classification, separate from strategy liquidity eligibility |
| Debt pressure health | Diagnostic | Financial evidence, separate from hard debt-burden constraint |
| Leverage health | Diagnostic | Financial evidence, not currently a universal hard block |

### Key boundary

**Financial health ≠ hard constraint.**

A ratio can be unhealthy without automatically becoming a hard planning block.

---

## 7. Current Goal Validity vs Financial Hard Constraints

There are two different categories currently represented under hard constraints:

### A. Goal validity

Examples:
- positive horizon,
- positive future target.

These determine whether the goal itself is mathematically valid.

### B. Financial protection constraints

Examples:
- critical emergency reserve,
- critical DTI,
- essential-goal precedence.

These determine whether the user's available financial capacity can safely support a discretionary commitment.

These categories should remain distinguishable in the future Canonical Decision Engine even if both ultimately use the same hard-constraint gate.

---

## 8. Current Decision Roles

The current backend explicitly distinguishes:

- `HARD_CONSTRAINT`
- `ELIGIBILITY`
- `RANKING_INPUT`
- `RECOMMENDATION_ONLY`
- `ARCHITECTURE_CONSTRAINT`
- `EXPLANATORY_EVIDENCE`

This is important because not every “constraint-looking” item should block a strategy.

The current canonical registry already maps:
- `goal-positive-horizon` → HARD_CONSTRAINT
- `goal-positive-target` → HARD_CONSTRAINT
- `discretionary-cannot-preempt-essential` → HARD_CONSTRAINT

The eight strategy fit rules remain **ELIGIBILITY**, not hard constraints.

---

## 9. Current Strategy Decision Boundary

The current Strategy Engine receives a `ConstraintSet` and passes constraint context into decision/eligibility layers.

The strategy eligibility layer separately evaluates:
1. Cash-flow Fit
2. Liquidity Fit
3. Debt Fit
4. Asset Resource Fit
5. Risk Capacity Fit
6. Goal Constraint Fit
7. Multi-goal Conflict Fit
8. Implementation Fit

Therefore:

**Hard Constraint Gate ≠ 8-Fit Eligibility Gate.**

A hard constraint should answer:

> “Is this planning situation allowed to proceed?”

Eligibility should answer:

> “Can this particular strategy proceed successfully under the allowed situation?”

This distinction should remain in the target Decision Engine.

---

## 10. Current Gaps / Overlap

### Gap 1 — Hard constraints are not yet one complete business-rule registry

The policy layer is centralized, but not every current hard business behavior is represented as a first-class entry in `backend/rules/canonical.py`.

For example, emergency reserve and DTI critical behaviors have policy IDs/constants and evaluator implementations, but the canonical registry should eventually provide one authoritative identity/description/role for every hard rule.

### Gap 2 — Rule identity and rule execution are separated, but incompletely

`backend/rules/canonical.py` is currently the metadata authority.

`backend/engines/constraints/policy.py` owns policy IDs and thresholds.

`backend/engines/constraints/evaluator.py` owns execution.

This is a good separation of concerns, but the target should make the relationship explicit:

**Canonical Rule → Policy/Thresholds → Evaluator → Constraint Result**

rather than allowing new rules to appear only inside an engine.

### Gap 3 — Some financial health signals can look like constraints

Emergency reserve, DTI, savings rate, liquidity and leverage appear in several layers.

The system needs a single declared decision role for each signal:
- hard constraint,
- warning,
- diagnostic,
- eligibility input,
- recommendation evidence.

Otherwise “unhealthy” can incorrectly become “blocked.”

### Gap 4 — Constraint and eligibility can both use similar financial facts

For example, debt and liquidity appear in:
- hard constraint evaluation,
- diagnostics,
- strategy eligibility.

That is acceptable when each layer has a different decision role, but the source fact and authority must be canonical.

### Gap 5 — Missing data policy needs to remain explicit

Current canonical calculation behavior avoids silently treating missing required data as zero.

The same principle should apply to hard constraints:

**Missing evidence must not automatically become a hard failure.**

The system should distinguish:
- failed rule,
- passed rule,
- unavailable/not assessable.

This is especially important for financial planning.

---

## 11. Recommended Target Framework

The target Canonical Decision Engine should use this order:

**Goal Validity → Hard Constraint Gate → Strategy Applicability → 8-Fit Eligibility → Strategy Selection → Variant Selection → Technique → Architecture → Stress/Resilience → Recommendation**

The hard-constraint stage should have three explicit outcomes:

| Outcome | Meaning |
|---|---|
| PASS | No hard constraint prevents the decision |
| FAIL | A confirmed hard constraint blocks/restricts the decision |
| UNAVAILABLE | Required evidence is missing; do not manufacture a failure |

Where a hard constraint is a **goal-specific restriction**, its scope should be explicit rather than globally blocking every goal.

---

## 12. Recommended Canonical Hard-Constraint Categories

These categories should be documented first and frozen only after real-life validation.

### Category A — Goal validity
- positive horizon
- positive target
- any future mandatory validity rules discovered during case testing

### Category B — Financial safety/protection
- critical emergency reserve
- critical debt-service burden
- essential funding precedence

### Category C — Multi-goal protection
- discretionary goal cannot preempt essential/safety commitments
- confirmed higher-priority goal conflicts that are genuinely blocking

### Category D — Data sufficiency
Not a financial hard constraint itself.

Instead, define whether a rule is:
- assessable,
- unavailable,
- or failed.

This prevents missing data from becoming a false failure.

---

## 13. Recommended Ownership

Future ownership should be:

| Responsibility | Recommended authority |
|---|---|
| Canonical rule identity | `backend/rules/canonical.py` or dedicated canonical decision-rule registry |
| Hard-constraint policy/thresholds | `backend/rules/` canonical decision policy |
| Constraint normalization/conflict policy | `backend/engines/constraints/policy.py` during transition; later aligned to canonical rule ownership |
| Constraint calculation/evaluation | Constraint evaluator |
| Aggregation | Constraint aggregator |
| Decision execution | Canonical Decision Engine |
| Strategy eligibility | Strategy eligibility module |
| Diagnostics | Financial/MoneyWheel diagnostic layer |

The key principle:

**Engines execute canonical rules; they should not invent new hard business rules locally.**

---

## 14. Real-Life Validation Before Freezing

Before implementation, test the current behavior against real cases.

Minimum cases:

1. Goal with zero/negative horizon.
2. Goal with zero/negative target.
3. Emergency reserve below 3 months + high-priority discretionary goal.
4. Emergency reserve between 3 and 6 months.
5. DTI above 40% + high-priority discretionary goal.
6. DTI between 30% and 40%.
7. Low savings rate but healthy emergency reserve.
8. Missing emergency-reserve data.
9. Missing income/DTI data.
10. Essential goal competing with discretionary goal.
11. Multiple goals where one safety constraint should affect only selected goals.
12. Conflicting constraint evidence from different sources.

For each case, record:
- input facts,
- expected constraint,
- expected role,
- PASS/FAIL/UNAVAILABLE,
- whether the goal is blocked, priority-adjusted, or merely warned,
- downstream Strategy Builder effect.

Only after this should the rule be frozen.

---

## 15. What Should NOT Be Frozen Yet

Do not freeze these solely from the current code:

- whether every critical ratio should become a hard constraint,
- whether emergency reserve should block all discretionary goals or only demote priority,
- whether DTI should block strategy selection or only alter priority,
- whether leverage should ever become a hard constraint,
- whether savings rate should ever become a hard constraint,
- exact multi-goal precedence behavior in every scenario,
- missing-data behavior beyond the current “do not invent failure” principle,
- whether a hard constraint should block a goal, a strategy, a variant, or only a funding component.

These require real-life business cases.

---

## 16. Current vs Recommended Summary

| Area | Current state | Recommendation |
|---|---|---|
| Constraint policy | Strong central policy module exists | Preserve and align with canonical Decision Engine |
| Thresholds | Centralized in policy | Keep one owner |
| Goal validity | Centralized evaluator | Keep as hard-constraint domain |
| Emergency reserve | Hard + warning + diagnostic layers | Make decision role explicit and canonical |
| DTI | Hard + warning + diagnostic layers | Make decision role explicit and canonical |
| Savings rate | Warning/diagnostic | Do not convert to hard constraint without case validation |
| Liquidity | Diagnostic + eligibility | Keep roles separate |
| Leverage | Diagnostic | Do not promote automatically |
| Essential vs discretionary | Canonical policy exists | Preserve as multi-goal protection rule |
| Constraint aggregation | Central `ConstraintSet` exists | Preserve |
| Rule registry | Partial | Expand to every authoritative hard rule |
| Missing data | Generally protected against false zero/failure | Formalize PASS/FAIL/UNAVAILABLE |
| Strategy eligibility | Separate from hard constraints | Preserve separation |
| Decision Engine | Not yet the sole owner of business-rule execution | Make it the orchestrator of canonical rule results |

---

## 17. Decision Status

**Current status: DOCUMENTED — NOT FROZEN**

The code already provides a strong constraint foundation. The main problem is not absence of a constraint system; it is that the **full decision authority is not yet expressed as one complete canonical hard-constraint contract**.

The next step is **not refactoring**.

The next step is to validate these current rules with real-life cases, freeze the business behavior, and then move to:

**Step 3 — 8 Eligibility Fits: Current State & Recommendation.**
