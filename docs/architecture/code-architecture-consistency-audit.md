# Code & Architecture Consistency Audit

> Purpose: maintain a single source of truth for formula, policy, contract, taxonomy, strategy, and compatibility inconsistencies found in the Planvesto codebase.
>
> Rule: an item is listed as an **active conflict** only when current code provides concrete evidence. Legacy/compatibility items are separated so they are not mistaken for active runtime bugs.

## 1. Executive Summary

The codebase has a strong canonicalization direction, but some downstream services still reproduce calculations or translate contracts locally.

Highest-priority findings:

1. **FinancialPlanService has a conflicting DTI formula.**
   - Canonical DTI = Monthly Debt Payments / Gross Monthly Income × 100.
   - FinancialPlanService currently uses Total Liabilities / Annual Income × 100.
   - This is not the same financial metric.

2. **FinancialPlanService has a competing emergency-coverage calculation.**
   - Local formula uses `financial_assets * 0.2 / monthly_exp`.
   - Canonical emergency coverage uses Liquid Assets / Essential Monthly Expenses.

3. **DTI threshold handling has a boundary inconsistency.**
   - Canonical policy defines 40% as the critical threshold.
   - MoneyWheel classifies `>= 40%` as critical.
   - Summary Report only raises its high-DTI observation for `> 40%`.
   - ConstraintEvaluator text says `Critical > 40%`, while the policy boundary is 40%.

4. **Feasibility vocabulary is translated between layers.**
   - Strategy decision code uses `feasible` / `constrained`.
   - Multi-goal planning maps `constrained` to `conditional`.
   - This is currently an adapter, but it creates two vocabularies for the same concept and should be made explicit/canonical.

5. **Some canonical techniques are registered and executable but not attached to any canonical strategy.**
   - `tech-barbell`
   - `tech-tax-loss-harvesting`
   These are catalogued and executable, but the current strategy definitions do not reference them. This is a coverage/mapping gap, not necessarily a runtime bug.

6. **A separate legacy/dead-data audit already identifies additional contract and migration residue.**
   - See `docs/dead-legacy-data/dead-legacy-data.md`.
   - Those items should not automatically be treated as active defects; many are deliberate compatibility surfaces.

---

## 2. Severity Model

| Severity | Meaning |
|---|---|
| P0 | Wrong calculation / decision can materially change financial output |
| P1 | Cross-layer contract or policy mismatch that can produce inconsistent interpretation |
| P2 | Mapping/coverage gap, duplicated surface, or maintainability risk |
| P3 | Legacy/orphaned residue with no confirmed current runtime impact |

---

## 3. Active Conflicts / High-Value Findings

### P0 — Duplicate/conflicting DTI calculation

**Status:** Confirmed active conflict

**Canonical owner**

`backend/engines/calculation/canonical.py`

Function:

`calculate_debt_to_income_ratio(...)`

Canonical identity:

> Monthly Debt Payments / Gross Monthly Income × 100

Consumers already aligned with this calculation include MoneyWheel, ConstraintEvaluator, and Risk Profiler.

**Conflicting implementation**

`backend/services/financial_plan_service.py`

Current local calculation:

`dti_pct = (liabilities / income * 100.0)`

where `income` is taken from `annual_income`.

Therefore the service is effectively comparing:

> Total outstanding liabilities / Annual income

That is a leverage-style relationship, not DTI.

**Impact**

The Complete Financial Plan can expose a DTI-like value that disagrees with MoneyWheel, Constraints, Risk Profiler, and canonical calculations for the same financial state.

**Required direction**

FinancialPlanService must consume the canonical DTI calculation/fact. It must not independently derive DTI.

---

### P0 — Duplicate/conflicting emergency coverage calculation

**Status:** Confirmed active conflict

**Canonical owner**

`backend/engines/calculation/canonical.py`

Function:

`calculate_emergency_coverage(...)`

Canonical identity:

> Liquid Assets / Essential Monthly Expenses

**Conflicting implementation**

`backend/services/financial_plan_service.py`

Current local calculation:

`emergency_months = (financial_assets * 0.2) / monthly_exp]

This assumes 20% of financial assets are emergency resources and also uses a monthly-expense basis that is not the canonical essential-expense input.

**Impact**

The Complete Financial Plan can report an emergency-coverage figure different from MoneyWheel/canonical calculations.

**Required direction**

FinancialPlanService should consume the canonical emergency-coverage fact/result rather than deriving a local approximation.

---

### P1 — DTI critical boundary mismatch

**Status:** Confirmed

**Canonical policy**

`backend/engines/constraints/policy.py`

Current thresholds:

- Excellent: 20%
- Healthy: 30%
- Critical: 40%

**MoneyWheel**

`backend/rules/moneywheel.py`

Critical begins at:

`>= 40%`

**Summary Report**

`backend/engines/summary_report/engine.py`

Current observation condition:

`dti > 40`

Therefore exactly 40% can be:

- critical in MoneyWheel/constraints
- not flagged by the Summary Report observation rule

**ConstraintEvaluator**

`backend/engines/constraints/evaluator.py`

Benchmark text currently says:

`Critical > 40%`

while the canonical policy boundary is 40%.

**Required direction**

Use the canonical threshold constant and boundary consistently across all consumers. Do not hard-code `40` or `> 40`.

---

### P1 — Feasibility vocabulary mismatch / adapter translation

**Status:** Confirmed cross-layer translation

**Strategy decision**

`backend/engines/strategy/decision.py`

Uses:

- `feasible`
- `constrained`

**Multi-goal planning**

`backend/services/multi_goal_planning_service.py`

Maps:

`"feasible" -> "pass"`

and:

`"constrained" -> "conditional"`

This means multiple status vocabularies coexist:

- strategy decision vocabulary
- multi-goal planning vocabulary
- eligibility vocabulary (PASS / CONDITIONAL / FAIL)

**Impact**

The same underlying state can have different names depending on the layer. That is manageable only if the mapping is an explicit contract.

**Required direction**

Define one canonical semantic vocabulary and document/centralize adapters at API boundaries. Avoid ad-hoc string translation in services.

---

### P2 — Canonical technique coverage gap

**Status:** Confirmed catalog/runtime coverage gap

Canonical registry:

`backend/library/strategies/techniques_canonical.py`

contains 10 techniques.

Technique Engine:

`backend/engines/technique/engine.py`

supports all 10, including:

- `tech-barbell`
- `tech-tax-loss-harvesting`

But current canonical strategy definitions in:

`backend/library/strategies/canonical.py`

do not reference those two techniques.

Current result:

- Technique exists
- Technique is executable
- Technique has tests
- Technique is not reachable through the canonical strategy-to-technique mapping

This is not necessarily a defect: the techniques may intentionally be reserved for future strategy mappings. It should nevertheless be explicit.

**Required direction**

Either:
1. attach each technique to an appropriate canonical strategy, or
2. mark it explicitly as catalog-only/future capability.

---

## 4. Legacy / Compatibility / Orphaned Data

A broader audit already exists at:

`docs/dead-legacy-data/dead-legacy-data.md`

It currently records 30 items. Important categories include:

### Goal input residue

- `targetAge`
- `currentSavedAmount`
- goal-level `monthlyContribution`
- `inflationApplicability`
- goal-level `notes`
- `specialized_data`

These should be reviewed against the current Goal / DefinedGoal contracts.

### Legacy calculation surfaces

- FinancialPlanService duplicate DTI
- FinancialPlanService duplicate emergency coverage

These are also listed above because they have current runtime impact.

### Compatibility surfaces

- MoneyWheel legacy ratio aliases
- compatibility-only MoneyWheel ratio definitions
- legacy strategy ID `strat-cap-preservation`
- legacy architecture IDs
- legacy MoneyWheel API ratio keys
- legacy planning-unit localStorage key
- legacy retirement PDF route
- `MoneyWheelEngine` import alias
- legacy constraint model exports

These should not be removed blindly. They require consumer/deprecation analysis first.

### Contract/model residue

The legacy audit also records:

- priority-ranking definitions
- funding-status vocabulary
- feasibility-status vocabulary
- overlapping orchestration/allocation models
- goal taxonomy aliases
- duplicate migration residue
- compatibility report fields

These need to be revalidated against current code before any cleanup because some have already been partially canonicalized.

---

## 5. Canonical Ownership Rules

The following ownership rules should be enforced during future development.

### Financial calculations

**One calculation → one canonical implementation.**

Examples:

- DTI → `calculate_debt_to_income_ratio`
- Expense Coverage → `calculate_expense_coverage`
- Emergency Coverage → `calculate_emergency_coverage`
- Leverage → canonical leverage calculation
- Goal Funding Ratio → canonical goal-funding calculation

Consumers may transform presentation, but should not redefine the metric.

### Policy thresholds

**One policy → one policy owner.**

For DTI, threshold ownership belongs to:

`backend/engines/constraints/policy.py`

Consumers should import the policy constant rather than hard-code 40%.

### Strategy identity

Canonical strategy identity belongs to:

`backend/library/strategies/canonical.py`

Legacy IDs should remain compatibility aliases only.

### Technique identity

Canonical technique identity belongs to:

`backend/library/strategies/techniques_canonical.py`

Execution belongs to:

`backend/engines/technique/engine.py`

Strategy-to-technique applicability belongs to canonical strategy definitions.

### Constraint decision

Constraint policy/evaluation belongs to the Constraints layer.

A diagnostic metric such as DTI is not itself a constraint. The constraint decision is a separate policy/evaluation step.

---

## 6. Audit Checklist for Future Code Reviews

For every new calculation or rule, check:

- [ ] Does the metric already exist in canonical calculations?
- [ ] Is the formula identical to the canonical definition?
- [ ] Is the unit identical (ratio vs percentage)?
- [ ] Is the same threshold being reused?
- [ ] Are boundary operators identical (`>` vs `>=`)?
- [ ] Is the policy owned by the correct policy module?
- [ ] Is a service recalculating a value already available upstream?
- [ ] Is a frontend contract using a different vocabulary from the backend?
- [ ] Is a legacy alias clearly marked as compatibility-only?
- [ ] Is every executable strategy/technique reachable from the canonical mapping?
- [ ] If something is intentionally orphaned, is that status documented?
- [ ] Are tests checking cross-consumer consistency for the same input?

---

## 7. Recommended Remediation Order

### Phase 1 — Correct financial calculation authority

1. Remove/replace FinancialPlanService local DTI calculation.
2. Remove/replace FinancialPlanService local emergency-coverage calculation.
3. Make Complete Financial Plan consume canonical facts/results.
4. Add cross-consumer tests proving identical results.

### Phase 2 — Normalize policy boundaries

1. Replace Summary Report hard-coded `40`.
2. Use `DEBT_TO_INCOME_CRITICAL_PERCENT`.
3. Align `>= 40%` semantics everywhere.
4. Fix ConstraintEvaluator benchmark wording.

### Phase 3 — Normalize status contracts

1. Define canonical feasibility semantics.
2. Centralize translations between strategy decision, eligibility, orchestration, and API contracts.
3. Add contract tests for status conversion.

### Phase 4 — Clean strategy/technique coverage

1. Decide whether Barbell and Tax-Loss Harvesting are production strategy techniques or future catalog entries.
2. If production, map them to canonical strategies.
3. If future-only, explicitly mark/document their catalog-only status.

### Phase 5 — Legacy cleanup

Use `docs/dead-legacy-data/dead-legacy-data.md` as the backlog. Remove only after confirming there are no active consumers or compatibility requirements.

---

## 8. Definition of Done

This audit can be considered substantially resolved when:

- no downstream service recalculates canonical financial metrics independently;
- DTI has one formula and one threshold authority;
- emergency coverage has one formula authority;
- boundary semantics are consistent across MoneyWheel, Constraints, Reports, and tests;
- strategy/technique mappings are complete or explicitly marked as catalog-only;
- cross-layer status translations are centralized and documented;
- legacy compatibility surfaces have owners and deprecation decisions;
- tests verify same-input/same-result behavior across major consumers.

---

## Source Files Reviewed

Primary evidence includes:

- `backend/engines/calculation/canonical.py`
- `backend/engines/constraints/policy.py`
- `backend/engines/constraints/evaluator.py`
- `backend/engines/moneywheel/engine.py`
- `backend/rules/moneywheel.py`
- `backend/services/financial_plan_service.py`
- `backend/engines/summary_report/engine.py`
- `backend/engines/strategy/decision.py`
- `backend/services/multi_goal_planning_service.py`
- `backend/library/strategies/canonical.py`
- `backend/library/strategies/techniques_canonical.py`
- `backend/engines/technique/engine.py`
- `docs/dead-legacy-data/dead-legacy-data.md`
- `docs/architecture/FINANCIAL-PLANNING-LAYER-MAP.md`
- `docs/architecture/CANONICAL-CALCULATION-SYSTEM.md`

**Audit principle:** prefer verified code evidence over architectural assumptions. When a conflict is fixed, update this document and add a regression test so the same class of inconsistency does not return.
