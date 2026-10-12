# 03 — 8 Eligibility Fits: Current State & Recommendation

## 1. Purpose

This document records the **current code-verified state** of the eight Strategy Builder eligibility fits and the recommended target structure for the PlanVesto Canonical Decision Engine.

This is a **design/audit document only**. Rules are not frozen and no refactor is authorized by this document. Final business behavior will be frozen later using real-life cases.

## 2. The Eight Canonical Fits

The authoritative vocabulary is defined in `backend/rules/eligibility.py`:

1. Cash-flow Fit
2. Liquidity Fit
3. Debt Fit
4. Asset Resource Fit
5. Risk Capacity Fit
6. Goal Constraint Fit
7. Multi-goal Conflict Fit
8. Implementation Fit

The allowed result for every fit is:

- **PASS**
- **CONDITIONAL**
- **FAIL**

The aggregate assessment currently follows:
- any FAIL → overall FAIL
- otherwise any CONDITIONAL → overall CONDITIONAL
- otherwise PASS

Therefore the current aggregation is effectively:

**FAIL > CONDITIONAL > PASS**

---

## 3. Current Authority

### Definition authority

`backend/rules/eligibility.py` owns:
- fit names,
- eligibility status vocabulary.

### Business-rule execution

`backend/engines/strategy/eligibility.py` owns:
- all eight fit calculations,
- status assignment,
- reasons,
- required changes,
- eligibility aggregation,
- goal/strategy constraint checks.

### Decision consumption

`backend/engines/strategy/decision.py`:
- evaluates all eight fits,
- applies the separate eligibility gate,
- prefers PASS architectures,
- considers CONDITIONAL architectures only when no PASS exists,
- then uses decision scores to choose among the eligible pool.

This means the eight fits are currently centralized in one execution module, but their **business-policy ownership is still engine-based rather than a dedicated canonical rule registry**.

---

## 4. Current Fit-by-Fit Audit

| Fit | Current code test | PASS | CONDITIONAL | FAIL | Current role |
|---|---|---|---|---|---|
| Cash-flow Fit | Required monthly contribution vs investable surplus | Required <= surplus | Evidence incomplete OR required > surplus | Surplus <= 0 | Strategy eligibility |
| Liquidity Fit | Liquid assets vs required liquidity | Liquid >= required | Evidence incomplete OR liquidity gap | No current FAIL path | Strategy eligibility |
| Debt Fit | Mandatory debt payment and cash-flow serviceability | Surplus >= 0 | EMI evidence incomplete | Surplus < 0 | Strategy eligibility |
| Asset Resource Fit | Available strategy resource vs required resource | Available >= required | Evidence incomplete OR resource gap | No current FAIL path | Strategy eligibility |
| Risk Capacity Fit | Required strategy risk vs investor risk capacity | Required <= capacity | De-risked implementation can fit | Required risk > capacity and no de-risked path | Strategy eligibility |
| Goal Constraint Fit | Goal type, horizon, strategy constraints | All checks pass | No current conditional path | Any goal/strategy constraint fails | Strategy eligibility |
| Multi-goal Conflict Fit | Higher-priority goal conflict | No conflict | Impact not evidenced OR reallocation required | Higher-priority goal materially compromised | Strategy eligibility |
| Implementation Fit | Implementation evidence/status | Explicit pass | Evidence incomplete or conditional | Explicit failure | Strategy eligibility |

---

## 5. Fit 1 — Cash-flow Fit

### Current rule

The engine first looks for:
- strategy-required monthly contribution,
- investable monthly/annual surplus.

If these are unavailable, it returns CONDITIONAL.

If surplus is <= 0, it returns FAIL.

If required contribution <= surplus, it returns PASS.

If required contribution exceeds surplus but surplus is positive, it returns CONDITIONAL and records the funding gap.

### Current interpretation

Cash-flow Fit is not simply “income is high enough.”

It is specifically about whether the strategy's required contribution fits available investable cash-flow capacity.

### Recommendation

Keep this as a true eligibility fit.

Later freeze:
- whether zero surplus should always be FAIL,
- whether a positive surplus with a contribution gap should always remain CONDITIONAL,
- whether some strategy types can legitimately use assets/lumpsum to overcome a monthly cash-flow gap.

---

## 6. Fit 2 — Liquidity Fit

### Current rule

The engine compares:
- liquid assets,
- required liquidity.

If evidence is missing → CONDITIONAL.

If liquid assets cover the requirement → PASS.

If there is a liquidity gap → CONDITIONAL.

There is currently **no direct FAIL path** inside this fit.

### Important observation

Liquidity Fit can therefore report a meaningful shortfall without making the strategy itself FAIL.

This is different from a hard emergency-reserve constraint.

### Recommendation

Keep the separation:

**Hard safety constraint → protection decision**

**Liquidity Fit → strategy-specific feasibility**

Later freeze whether certain severe liquidity gaps should become FAIL for specific strategies.

---

## 7. Fit 3 — Debt Fit

### Current rule

The engine checks mandatory debt payment evidence.

If EMI evidence is missing → CONDITIONAL.

If surplus is non-negative → PASS.

If surplus is negative → FAIL.

### Important observation

The actual DTI > 40% hard constraint is handled in the constraint layer.

Debt Fit is a different question:

> Can the strategy coexist with current debt-service capacity?

### Recommendation

Do not merge Debt Fit with the DTI hard constraint.

They use related financial facts but have different decision roles.

---

## 8. Fit 4 — Asset Resource Fit

### Current rule

The engine compares:
- strategy-required asset/resource amount,
- available asset/resource amount.

Missing evidence → CONDITIONAL.

Available >= required → PASS.

Available < required → CONDITIONAL.

There is currently **no direct FAIL path**.

### Recommendation

Keep this as strategy eligibility.

Later freeze:
- what counts as a valid resource,
- whether all asset classes are equally usable,
- whether an asset gap should ever produce FAIL,
- how earmarked assets affect available resource.

---

## 9. Fit 5 — Risk Capacity Fit

### Current rule

The engine compares:
- strategy-required risk capacity,
- investor risk capacity.

If missing → CONDITIONAL.

If requirement <= capacity → PASS.

If requirement exceeds capacity but a defined de-risked implementation fits → CONDITIONAL.

Otherwise → FAIL.

### Important boundary

Risk Capacity is a financial capacity concept.

It should not be confused with behavioral Risk Tolerance.

The current repo already separates objective risk capacity from behavioral evidence.

### Recommendation

Keep this fit.

Later freeze:
- canonical scale/units,
- exact comparison semantics,
- when a de-risked implementation is a legitimate CONDITIONAL solution,
- when risk mismatch must be an absolute FAIL.

---

## 10. Fit 6 — Goal Constraint Fit

### Current rule

The engine checks:
- canonical goal type against strategy's applicable goal types,
- strategy horizon constraints,
- strategy funding-gap constraints.

Any failed check → FAIL.

All checks passing → PASS.

There is currently no explicit CONDITIONAL path.

### Important observation

This fit overlaps conceptually with **Strategy Applicability**.

That overlap should be resolved during later rule freezing.

Recommended distinction:

**Applicability**
> Should this strategy enter the candidate pool at all?

**Goal Constraint Fit**
> Once it is a candidate, does the specific goal satisfy the strategy's mandatory constraints?

This distinction avoids duplicating the same gate.

---

## 11. Fit 7 — Multi-goal Conflict Fit

### Current rule

The engine checks `higher_priority_goal_conflict`.

- missing evidence → CONDITIONAL,
- true/material conflict → FAIL,
- conditional conflict → CONDITIONAL,
- no conflict → PASS.

### Important observation

This is one of the most important boundaries between:
- hard multi-goal protection,
- strategy eligibility,
- recommendation.

A confirmed essential/higher-priority conflict can become a hard constraint in the broader Decision Engine, while strategy-specific resource conflict can remain an eligibility result.

### Recommendation

Do not collapse this fit into generic goal priority.

Later freeze:
- what constitutes “materially compromised,”
- whether the conflict is hard or conditional,
- how multiple higher-priority goals are handled.

---

## 12. Fit 8 — Implementation Fit

### Current rule

The engine checks `implementation_status`.

- missing → CONDITIONAL,
- pass → PASS,
- conditional → CONDITIONAL,
- anything else → FAIL.

### Important observation

Implementation Fit is currently partly an evidence/status interface rather than a deeply computed financial rule.

### Recommendation

Keep it as a fit, but later define what “implementation evidence” actually means.

Possible dimensions to validate later:
- required action exists,
- required product/instrument/resource is available,
- execution can occur within timeline,
- required account/asset transition is possible.

Do not invent these rules during refactoring without business validation.

---

## 13. Current Overall Eligibility Gate

Current architecture effectively applies:

**Applicability → 8 Fits → Eligibility Gate → Decision Score**

The eight fits are evaluated together.

Current aggregation:

| Fit result combination | Overall status |
|---|---|
| Any FAIL | FAIL |
| No FAIL + any CONDITIONAL | CONDITIONAL |
| All PASS | PASS |

Then the decision layer applies an additional rule:

**PASS pool is preferred. CONDITIONAL pool is considered only when no PASS exists.**

This is currently the most important cross-fit decision policy.

---

## 14. Current Gaps / Overlap

### Gap 1 — Definition vs business policy

Fit names are canonical, but the thresholds and conditions are implemented inside the strategy engine.

Recommendation: eventually move authoritative business policy into canonical rule modules while leaving the engine responsible for execution.

### Gap 2 — Not every fit has symmetric PASS/CONDITIONAL/FAIL behavior

Examples:
- Liquidity Fit has no direct FAIL path.
- Asset Resource Fit has no direct FAIL path.
- Goal Constraint Fit has no CONDITIONAL path.

This may be intentional, but it needs business validation.

### Gap 3 — Missing evidence currently becomes CONDITIONAL

This is safer than silently treating missing data as zero.

However, the target Decision Engine should explicitly distinguish:

**FAIL = rule evaluated and failed**

**CONDITIONAL = rule can proceed only with a defined condition/change**

**UNAVAILABLE = required evidence is missing**

Whether UNAVAILABLE remains a fourth public status or maps to CONDITIONAL for product UX should be decided later.

### Gap 4 — Applicability overlap

Goal Constraint Fit partly repeats strategy applicability.

The target architecture should make the boundary explicit.

### Gap 5 — Hard constraint overlap

Debt Fit and liquidity-related fits use facts also used by the hard-constraint layer.

That is acceptable only because their roles differ.

The source facts should be canonical; the decision roles should remain separate.

### Gap 6 — Input contracts are implicit

The current engine expects context keys such as:
- `strategy_required_monthly_contribution`
- `investable_surplus_monthly`
- `liquid_assets`
- `required_liquidity`
- `strategy_required_asset_resource`
- `available_asset_resource`
- `strategy_required_risk_capacity`
- `risk_capacity`
- `de_risked_strategy_risk`
- `higher_priority_goal_conflict`
- `implementation_status`

These should eventually become explicit canonical inputs rather than loosely named context fields.

---

## 15. Recommended Target Contract

The eight fits should remain the canonical Strategy Eligibility Gate.

Recommended pipeline:

**Strategy Applicability**
↓
**Hard Constraint Gate**
↓
**8-Fit Eligibility Gate**
↓
**PASS / CONDITIONAL / FAIL**
↓
**Strategy Selection**

The key principle:

> Hard constraints decide whether planning is allowed to proceed safely.  
> Eligibility fits decide whether a particular strategy is suitable and feasible.

---

## 16. Recommended Ownership

| Responsibility | Recommended authority |
|---|---|
| Fit names/status vocabulary | `backend/rules/eligibility.py` |
| Canonical fit rule identity | Canonical Decision Rule registry |
| Fit policy/thresholds | Dedicated canonical strategy-eligibility rules |
| Fit execution | Strategy eligibility evaluator |
| Aggregation | Eligibility assessment/gate |
| Strategy selection | Decision layer |
| Hard constraints | Constraint engine |
| Diagnostics | Financial/MoneyWheel layers |

Target principle:

**One business rule → one canonical owner → many consumers.**

---

## 17. Real-Life Validation Cases Before Freezing

At minimum validate:

1. Required SIP exactly equals surplus.
2. Required SIP is slightly above surplus.
3. Surplus is zero.
4. Surplus is negative.
5. Liquid assets exactly equal required liquidity.
6. Liquidity is below requirement.
7. EMI evidence is missing.
8. Negative surplus with debt obligations.
9. Required asset resource equals available resource.
10. Asset resource gap.
11. Strategy risk equals risk capacity.
12. Strategy risk exceeds capacity but de-risked version fits.
13. Strategy risk exceeds capacity with no de-risked solution.
14. Goal type not supported by strategy.
15. Goal horizon violates strategy constraint.
16. Higher-priority goal is materially compromised.
17. Higher-priority conflict is unknown.
18. Implementation evidence missing.
19. Implementation explicitly conditional.
20. Implementation explicitly failed.
21. All eight PASS.
22. One FAIL + several PASS.
23. No FAIL + one CONDITIONAL.
24. Multiple CONDITIONAL fits.

For each case record:
- input facts,
- fit result,
- reason,
- required change,
- aggregate status,
- whether strategy enters the selection pool,
- expected final recommendation behavior.

---

## 18. What Should NOT Be Frozen Yet

Do not freeze solely from current code:

- exact thresholds for every fit,
- whether liquidity/resource gaps should become FAIL,
- whether missing evidence should remain CONDITIONAL or become UNAVAILABLE,
- exact definition of “materially compromised,”
- exact risk-capacity scale,
- whether implementation failure is always a strategy FAIL,
- how applicability and Goal Constraint Fit divide responsibility,
- whether every fit must have all three PASS/CONDITIONAL/FAIL outcomes,
- whether one FAIL should always eliminate a strategy in every future decision domain.

---

## 19. Current vs Recommended Summary

| Area | Current state | Recommendation |
|---|---|---|
| Eight fit vocabulary | Centralized | Preserve |
| Status vocabulary | PASS/CONDITIONAL/FAIL | Preserve for now |
| Fit execution | Centralized in strategy eligibility engine | Preserve behavior, later move policy ownership |
| Aggregation | FAIL > CONDITIONAL > PASS | Validate and then freeze |
| Missing evidence | Mostly CONDITIONAL | Make explicit data-sufficiency policy |
| Hard constraints | Separate constraint layer | Preserve separation |
| Applicability overlap | Exists | Define boundary clearly |
| Input contract | Context-key based | Formalize canonical inputs |
| Decision selection | Decision layer is authoritative | Preserve |
| Rule registry | Partial | Add eight fit rule identities/policies |
| Real-life validation | Not yet frozen | Required before refactor |

---

## 20. Decision Status

**CURRENT STATUS: DOCUMENTED — NOT FROZEN**

The repository already has a clear eight-fit structure and a single execution module. The main remaining design work is to establish the exact business meaning, input contract, and boundary of each fit before moving its policy into the Canonical Decision Engine.

**Next step:** Step 4 — Strategy Selection: Current State & Recommendation.


---

## 20. Verification Correction — Double Evaluation in Current Decision Path

The full code verification confirms that the current decision path performs **two related eligibility checks**:

1. `evaluate_eligibility_fits()` calculates the eight fit results.
2. `evaluate_eligibility()` separately applies the goal/constraint eligibility gate.

`backend/engines/strategy/decision.py` currently calls both and then combines their outcomes. This is an actual overlap in decision authority, not merely two presentation helpers.

For V1, the business meaning of these two checks must be explicitly separated or consolidated. Until that is decided, the documentation should not imply that the eight-fit evaluator is the only eligibility authority.

The previously documented asymmetry remains confirmed:
- Liquidity Fit has no direct FAIL branch.
- Asset Resource Fit has no direct FAIL branch.
- Goal Constraint Fit has no CONDITIONAL branch.

