# 05 — 22 Variant Selection: Current State & Recommendation

## 1. Purpose

This document records the current code-verified Strategy Variant Selection system and the recommended target contract for the PlanVesto Canonical Decision Engine.

This is a design/audit document only. Variant-selection rules are not frozen and no refactor is authorized by this document.

Final business behavior will be frozen later through real-life cases.

## 2. Scope

This step answers:

> After a strategy has been selected, how does PlanVesto choose the correct implementation variant under that strategy?

This covers:
- the canonical 22-variant registry,
- current variant ownership,
- current automated selection rules,
- fallback behavior,
- input dependencies,
- gaps and overlaps,
- recommended canonical ownership,
- real-life validation cases.

It does not freeze technique selection, architecture composition, or stress/resilience.

## 3. Current Canonical Variant Registry

The current code contains **22 active canonical variants**.

| Strategy | Active variants |
|---|---:|
| Goal Funding | 6 |
| Progressive De-risking | 4 |
| Capital Preservation | 4 |
| Debt Reduction | 4 |
| Credit Utilisation | 4 |
| **Total** | **22** |

The canonical registry is:

`backend/library/strategies/variants.py`

It defines:
- variant ID,
- name,
- parent strategy ID,
- variant type,
- description,
- required inputs,
- version,
- active status.

The registry explicitly says variants are reusable implementation paths and do not contain investor-specific calculated values.

## 4. Current 22 Variants

### Goal Funding — 6

1. Existing Assets — `existing_assets`
2. SIP — `sip`
3. Lumpsum — `lumpsum`
4. Lumpsum + SIP — `lumpsum_plus_sip`
5. Lumpsum + Step-up SIP — `lumpsum_plus_step_up_sip`
6. Step-up SIP — `step_up_sip`

### Progressive De-risking — 4

1. Goal-Date Glide Path — `goal_date_glide_path`
2. Payment-Tranche Glide Path — `payment_tranche_glide_path`
3. Recurring-Cashflow Glide Path — `recurring_cashflow_glide_path`
4. Income-Transition Glide Path — `income_transition_glide_path`

### Capital Preservation — 4

1. Full-Goal Preservation — `full_goal_preservation`
2. First-Payment Preservation — `first_payment_preservation`
3. Rolling Reserve Preservation — `rolling_reserve_preservation`
4. Protected-Core Preservation — `protected_core_preservation`

### Debt Reduction — 4

1. Goal-Gap Debt Reduction — `goal_gap_debt_reduction`
2. EMI-Relief Debt Reduction — `emi_relief_debt_reduction`
3. Residual-Gap Debt Reduction — `residual_gap_debt_reduction`
4. Goal-Linked Debt Reduction — `goal_linked_debt_reduction`

### Credit Utilisation — 4

1. Residual-Gap Bridge — `residual_gap_bridge`
2. Partial-Goal Financing — `partial_goal_financing`
3. EMI-Cap Financing — `emi_cap_financing`
4. Timing-Bridge Financing — `timing_bridge_financing`

## 5. Current Variant Selection Authority

The canonical **variant definitions** are owned by:

`backend/library/strategies/variants.py`

The actual **variant selection rules** are implemented by:

`backend/engines/strategy/variant_selector.py`

The recommendation layer invokes VariantSelector after the strategy decision:

`backend/engines/strategy/recommendation.py`

Therefore the current separation is:

**Variant Registry = definition authority**

**VariantSelector = selection behavior authority**

The selection behavior is not yet centralized in `backend/rules/`.

## 6. Current Product Behavior

The current code explicitly treats variants as:

> **100% automated system-selected**

The investor selects between system-generated candidate strategies; variants are not exposed as an interactive investor choice.

This is an important product rule and should remain explicit when the canonical contract is frozen.

## 7. Current Selection Rules — Goal Funding

The selector checks in this order:

1. If the baseline scenario already contains a valid `funding_strategy_id`, use it.
2. If mapped assets cover the future target, select `existing_assets`.
3. If investable surplus is zero/negative and there is a funding gap, select `lumpsum`.
4. Otherwise select `step_up_sip`.

### Important gap

The canonical registry contains six Goal Funding variants, but the current automatic selector directly chooses only:

- Existing Assets
- Lumpsum
- Step-up SIP

The other three variants are defined but are not directly selected by these current rules:

- SIP
- Lumpsum + SIP
- Lumpsum + Step-up SIP

A baseline scenario can still provide a valid funding variant, which can select one of them.

Therefore the current system has a **definition-vs-selection coverage gap**.

## 8. Current Selection Rules — Progressive De-risking

Current rules:

| Condition | Variant |
|---|---|
| Retirement / FIRE | Income-Transition Glide Path |
| Education or tranches/number of years | Payment-Tranche Glide Path |
| Vacation or multiple trips | Recurring-Cashflow Glide Path |
| Otherwise | Goal-Date Glide Path |

The rules are deterministic and ordered.

### Observation

The rule uses goal type plus selected dynamic details, but does not currently express these rules as canonical decision-policy records.

## 9. Current Selection Rules — Capital Preservation

Current rules:

| Condition | Variant |
|---|---|
| Vacation or recurring interval | Rolling Reserve Preservation |
| Education or number of years | First-Payment Preservation |
| Positive surplus and positive future target | Protected-Core Preservation |
| Otherwise | Full-Goal Preservation |

Again, these are executable rules inside VariantSelector rather than a canonical rule registry.

## 10. Current Selection Rules — Debt Reduction

Current rules:

| Condition | Variant |
|---|---|
| Debt Freedom or linked liability | Goal-Linked Debt Reduction |
| EMI / income >= 40% | EMI-Relief Debt Reduction |
| Surplus <= 0 | Residual-Gap Debt Reduction |
| Otherwise | Goal-Gap Debt Reduction |

### Important observation

The 40% EMI threshold is also relevant elsewhere in the broader decision system.

Before freezing, the ownership of this threshold must be clarified:

**Is 40% a hard constraint, eligibility condition, diagnostic, or variant-selection condition?**

It should not silently exist as independent policy in multiple locations.

## 11. Current Selection Rules — Credit Utilisation

Current rules:

| Condition | Variant |
|---|---|
| Timing bridge or duration <= 1 year | Timing-Bridge Financing |
| EMI / income >= 30% | EMI-Cap Financing |
| Education or Dream Home | Partial-Goal Financing |
| Otherwise | Residual-Gap Bridge |

### Important observation

The 30% EMI threshold is variant-selection policy, while the broader decision system also contains debt/DTI rules.

This needs explicit ownership before freezing.

## 12. Current Selection Flow

The current runtime flow is effectively:

**Strategy selected**
↓
**Recommendation generated**
↓
**Recommended scenario identified**
↓
**VariantSelector.select_variant()**
↓
**Strategy-specific deterministic rule**
↓
**Canonical variant definition retrieved**
↓
**Variant returned in StrategyRecommendation**

The variant therefore currently belongs **after strategy selection**.

## 13. Current Fallback Behavior

If the selected variant ID cannot be found in the canonical registry:

1. VariantSelector tries the first available canonical variant for the strategy.
2. If no variant exists, it raises an error.

This is safe from a crash perspective for a valid strategy, but it can hide a policy/registry mismatch.

### Recommendation

For the future canonical engine:

**Invalid variant mapping should be an explicit decision error, not silently converted into the first available variant.**

Fallback may be retained only where it is intentionally part of a documented compatibility policy.

## 14. Current Input Dependencies

Variant selection currently consumes a mixture of:

### Goal inputs

- goal type
- duration
- future target
- funding gap
- projected mapped asset value
- dynamic details

### Financial context

- investable monthly surplus
- monthly surplus
- EMI burden
- monthly debt payments
- monthly income / income

### Scenario context

- baseline scenario
- funding strategy ID

This input contract is currently implicit in code.

## 15. Current Problems / Gaps

### Gap 1 — Selection rules are not canonicalized

Definitions are canonical, but executable selection policy lives in VariantSelector.

### Gap 2 — Six Goal Funding variants vs three direct selector outcomes

The registry contains six variants, while current direct rule logic selects three unless the baseline scenario supplies another funding strategy ID.

### Gap 3 — Rule order is business policy

Many rules are evaluated sequentially. Changing rule order can change the selected variant.

That order therefore needs to become an explicit canonical policy rather than remaining an implementation detail.

### Gap 4 — Threshold duplication risk

30% and 40% EMI thresholds can overlap conceptually with debt/DTI and eligibility policy.

Each threshold needs one authoritative owner.

### Gap 5 — Missing-input behavior is implicit

Current code often converts absent numeric values to zero/default values.

This can make:

**missing data**

look like:

**real zero**

For variant selection this can produce the wrong variant.

### Gap 6 — Variant selection can happen inside recommendation

Recommendation currently calls VariantSelector directly.

The future Decision Engine should ideally resolve the variant as an explicit decision stage rather than allowing recommendation generation to own business selection behavior.

### Gap 7 — Registry validation is structural, not behavioral

The canonical registry validates IDs/names/parent strategy IDs, but it does not verify that every active variant has a reachable selection rule.

## 16. Recommended Target Contract

The target flow should be:

**Strategy Selection**
↓
**Variant Candidate Set**
↓
**Variant Applicability**
↓
**Variant Decision Conditions**
↓
**Deterministic Precedence**
↓
**Selected Variant**
↓
**Variant Evidence**
↓
**Technique Selection**

The Variant Registry should remain the definition source.

A separate canonical variant-rule layer should own selection policy.

Recommended future location:

`backend/rules/strategy_variants.py`

The engine should execute those rules rather than define them.

## 17. Recommended Variant Rule Structure

Each strategy should have an explicit rule table containing:

| Field | Purpose |
|---|---|
| Strategy ID | Parent strategy |
| Variant ID | Candidate variant |
| Applicability condition | When it can be considered |
| Selection condition | When it should win |
| Precedence | Order if multiple conditions match |
| Required inputs | Evidence required |
| Missing-data policy | What happens when evidence is unavailable |
| Exclusion condition | When variant cannot be used |
| Rationale | Why the variant is selected |

This makes variant selection auditable.

## 18. Recommended Decision Principle

Variant selection should not be:

**first if-condition that happens to match.**

It should be:

**Candidate Variants → Eligibility/Applicability → Explicit Conditions → Precedence → Selected Variant**

The exact conditions and precedence should be frozen only after real-life cases.

## 19. Real-Life Validation Cases Before Freezing

At minimum validate:

### Goal Funding
1. Existing assets fully cover target.
2. No surplus and funding gap.
3. Positive surplus with gap.
4. Level SIP is sufficient.
5. Step-up SIP is required.
6. Lumpsum + SIP is optimal.
7. Lumpsum + Step-up SIP is optimal.
8. Baseline scenario explicitly specifies each supported funding variant.

### Progressive De-risking
9. Retirement.
10. FIRE/passive income.
11. Education with tranches.
12. Vacation with recurring withdrawals.
13. Generic fixed-date goal.

### Capital Preservation
14. Vacation/repeating goal.
15. Education with staged payments.
16. Positive surplus with target.
17. Default preservation case.

### Debt Reduction
18. Debt Freedom / linked liability.
19. EMI burden >= 40%.
20. No surplus.
21. Normal surplus.

### Credit Utilisation
22. Timing bridge / <=1 year.
23. EMI burden >= 30%.
24. Education / Dream Home.
25. Generic financing gap.

### Data-quality cases
26. Missing surplus.
27. Missing income.
28. Missing EMI.
29. Missing dynamic details.
30. Conflicting signals where multiple variant conditions match.

For every case record:

**Inputs → Candidate Variants → Conditions Matched → Precedence → Selected Variant → Reason**

## 20. What Should NOT Be Frozen Yet

Do not freeze solely from current code:

- exact variant conditions,
- condition precedence,
- 30% EMI threshold,
- 40% EMI threshold,
- treatment of missing data,
- whether Goal Funding should directly expose all six variants to the selector,
- baseline-scenario authority vs selector authority,
- whether a variant can be CONDITIONAL,
- whether variants can be excluded by hard constraints,
- fallback behavior,
- investor visibility of variants,
- final variant-to-technique mapping.

## 21. Current vs Recommended Summary

| Area | Current state | Recommendation |
|---|---|---|
| Variant registry | 22 canonical active variants | Preserve |
| Variant definition authority | library/strategies/variants.py | Preserve |
| Selection authority | engines/strategy/variant_selector.py | Move policy to canonical rules |
| Investor selection | Automated | Preserve unless product decision changes |
| Goal Funding coverage | 6 defined, 3 directly selected + scenario override | Explicitly validate all six |
| Rule order | Embedded in methods | Make precedence explicit |
| Threshold ownership | Partly distributed | One canonical owner per threshold |
| Missing data | Implicit defaults | Explicit missing-data policy |
| Fallback | First available variant | Prefer explicit error/compatibility policy |
| Recommendation layer | Calls VariantSelector | Keep recommendation downstream of decision |
| Auditability | Limited | Return conditions/evidence/decision version |

## 22. Decision Status

**CURRENT STATUS: DOCUMENTED — NOT FROZEN**

The repository has a clean canonical definition registry for all 22 active variants and a deterministic runtime selector. The main issue is that **variant definitions are centralized but variant-selection business rules are still embedded in executable engine code**.

The next step is to validate these rules with real-life cases before freezing them.

**Next step: Step 6 — Technique Selection: Current State & Recommendation.**


---

## 23. Verification Correction — Goal Funding Reachability

The full code verification confirms that the **22 variants are defined**, but definition does not mean every variant is independently reachable through the current selector.

For Goal Funding, the fallback selector directly chooses only:

- `existing_assets`
- `lumpsum`
- `step_up_sip`

when no `baseline_scenario` is already bound to a variant.

The remaining Goal Funding variants:

- `sip`
- `lumpsum_plus_sip`
- `lumpsum_plus_step_up_sip`

are reachable only when an existing scenario already supplies the corresponding `funding_strategy_id`.

Therefore **22 active definitions ≠ 22 independently deterministic selector outcomes** in the current runtime.

This is a current implementation finding. The correct business precedence for making all 22 variants directly reachable must be decided through real-life cases before refactoring.

