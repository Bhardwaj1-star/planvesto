# Onboarding to MoneyWheel Architecture

**Status:** CANONICAL INITIAL PLANNING FOUNDATION

This document defines the initial financial-planning architecture from investor onboarding through MoneyWheel. The scope intentionally ends at MoneyWheel diagnostic output. Goal planning, constraints, strategy eligibility, recommendation, product selection, and action planning are downstream layers and are not defined as part of this initial phase.

## 1. Architecture Boundary

The initial phase has four logical layers:

1. **Onboarding / Financial Inputs** — collect and persist the investor's source information.
2. **Financial State** — normalize those source records into the authoritative current financial position.
3. **Canonical Financial Calculations** — calculate shared financial measures from the current Financial State.
4. **MoneyWheel** — classify those measures into financial-condition signals and return diagnostic explanations.

Flow:

**Investor → Onboarding → Source Records → Financial State → Canonical Calculations → MoneyWheel → Financial Diagnostic**

MoneyWheel does not become the source of truth for raw financial data. It consumes the current Financial State and canonical calculations.

## 2. Onboarding

Onboarding is the source-input layer. It captures the financial picture required to establish the planning context.

Current onboarding steps:

| Step | Domain | Primary Input |
|---|---|---|
| 1 | Personal Information | Name, DOB, marital status, contact/location, occupation |
| 2 | Family & Dependents | Family/dependent members |
| 3 | Income | Income sources |
| 4 | Expenses | Expense records |
| 5 | Assets | Asset records |
| 6 | Insurance | Insurance policies |
| 7 | Liabilities | Liability records |
| 8 | Goals | Goal records |

The onboarding state is scoped to a **planning unit** and may also carry an **investor ID** for individual scope.

The onboarding layer owns collection and persistence of source records. It does not calculate the final MoneyWheel ratios.

### Onboarding Data Ownership

| Data | Owner | Downstream Role |
|---|---|---|
| Personal Information | Onboarding persistence | Investor/planning context |
| Family & Dependents | Onboarding persistence | Household context |
| Income | Onboarding persistence | Financial State income inputs |
| Expenses | Onboarding persistence | Financial State expense inputs |
| Assets | Onboarding persistence | Financial State asset inputs |
| Liabilities | Onboarding persistence | Financial State liability inputs |
| Insurance | Onboarding persistence | Insurance coverage inputs |
| Goals | Onboarding persistence | Goal context and later planning |

## 3. Financial State

Financial State is the authoritative current-state aggregate built from persisted financial source records.

Flow:

**Onboarding Source Records → Financial State Engine → FinancialState → Snapshot**

The Financial State service reads the persisted financial inputs and builds a normalized state containing the current financial position.

Core state used by downstream calculations includes:

- annual income
- annual expenses
- investable monthly surplus
- total assets
- financial assets
- liquid assets
- total liabilities
- net worth
- essential monthly expenses
- EMI / debt-payment context
- planning unit
- scope
- investor context where applicable

### Snapshot Authority

Financial State snapshots are bound to the revision of the underlying raw inputs.

The service:

1. reads current persisted inputs,
2. creates a deterministic input revision,
3. checks the latest snapshot,
4. reuses it only when the snapshot is still bound to the same input revision and planning context,
5. otherwise rebuilds Financial State and saves a new snapshot.

This prevents MoneyWheel and other downstream consumers from silently reading stale financial state.

### Financial State Rule

**Raw onboarding records remain source data. Financial State is the authoritative normalized current-state representation consumed by calculations and diagnostics.**

## 4. Canonical Financial Calculations

MoneyWheel does not independently own the core financial formulas.

The canonical calculation layer provides shared calculation functions consumed by MoneyWheel and other financial engines.

Examples include:

| Measure | Canonical Calculation |
|---|---|
| Savings Rate | Monthly surplus relative to gross monthly income |
| Liquid Asset Ratio | Liquid assets relative to total assets |
| Debt-to-Income Ratio | Monthly debt payments relative to gross monthly income |
| Leverage Ratio | Total liabilities relative to total assets |
| Financial Asset Ratio | Financial assets relative to total assets |
| Insurance Coverage Ratio | Existing sum assured relative to required insurance cover |
| Goal Funding Ratio | Current goal funding relative to goal target |
| Future Funding Ratio | Projected goal funding relative to future goal target |
| Required Rate of Return | Required return from current funding, future target and duration |
| Emergency Coverage | Liquid assets relative to essential monthly expenses |
| Expense Coverage | Liquid assets relative to monthly expenses |

The canonical calculation layer answers:

**“What is the financial measure?”**

MoneyWheel answers:

**“What does that measure indicate under the MoneyWheel rule set?”**

## 5. MoneyWheel

MoneyWheel is the diagnostic framework at the end of this initial phase.

It receives a MoneywheelInput derived from the current financial context and produces a MoneywheelResult.

Current canonical MoneyWheel ratio set:

| Ratio | What It Measures |
|---|---|
| Savings Rate | Savings capacity relative to income |
| Liquid Asset Ratio | Liquid assets relative to total assets |
| Debt-to-Income Ratio | Debt-payment burden relative to income |
| Leverage Ratio | Liabilities relative to assets |
| Financial Asset Ratio | Financial assets relative to total assets |
| Insurance Coverage Ratio | Existing insurance cover relative to required cover |
| Goal Funding Ratio | Current goal funding relative to target |
| Future Funding Ratio | Projected funding relative to future target |
| Required Rate of Return | Return required to reach the future target |

MoneyWheel also returns separate coverage rules:

| Rule | What It Measures |
|---|---|
| Expense Coverage | Liquid assets in months of total monthly expenses |
| Emergency Coverage | Liquid assets in months of essential monthly expenses |

## 6. MoneyWheel Classification

MoneyWheel uses a versioned rule set to classify available ratios.

Current classification statuses:

**Excellent → Healthy → Attention → Critical**

Classification is ratio-specific. The same status names do not imply one universal threshold across all metrics.

Examples from the current rule set:

| Metric | Classification Basis |
|---|---|
| Savings Rate | Percentage of income retained as savings |
| Debt-to-Income Ratio | Percentage of gross income consumed by debt payments |
| Leverage Ratio | Percentage of assets represented by liabilities |
| Emergency Coverage | Months of essential expenses covered by liquid assets |
| Required Rate of Return | Return required to bridge current funding to future target |

The classification function is owned by the MoneyWheel rule layer and uses the canonical rule definitions and thresholds.

## 7. MoneyWheel Output

MoneyWheel returns diagnostic information rather than making a strategy decision.

A ratio result contains, where available:

- metric key
- display name
- calculated value
- unit
- classification status
- formula
- explanation
- availability

A coverage-rule result contains:

- rule key
- display name
- calculated value
- unit
- formula
- explanation
- availability

The overall result also carries the MoneyWheel rule-set version and calculation timestamp.

### Missing Data Behavior

If required inputs are missing, the corresponding ratio/rule is marked unavailable rather than inventing a value.

Examples:

- missing numerator/denominator → unavailable
- zero denominator → unavailable
- undefined required return → unavailable
- non-finite calculated value → unavailable

This preserves diagnostic integrity and makes data gaps explicit.

## 8. MoneyWheel vs Constraints

MoneyWheel and Constraints consume overlapping financial measures, but they have different responsibilities.

| Layer | Question | Output | Decision Authority |
|---|---|---|---|
| Canonical Calculations | What is the financial measure? | Standardized ratio/measure | Calculation authority |
| MoneyWheel | What condition does the measure indicate? | Excellent / Healthy / Attention / Critical + explanation | Diagnostic authority |
| Constraints | Does a financial/goal condition impose a planning restriction? | Hard constraint / Warning / Override / Evidence | Constraint authority |
| Strategy Eligibility | Can a specific strategy proceed? | Pass / Conditional / Fail | Strategy eligibility authority |

Therefore:

**MoneyWheel classification is not itself a strategy rejection.**

A MoneyWheel metric can provide evidence used by downstream constraint assessment, but the constraint layer owns the policy decision about whether that evidence becomes a warning, hard constraint, or suggested override.

## 9. End-to-End Decision Boundary

The complete initial-phase flow is:

**Onboarding**

↓

**Persisted Source Records**

↓

**Financial State Service**

↓

**Authoritative Financial State Snapshot**

↓

**Canonical Financial Calculations**

↓

**MoneyWheel Rule Classification**

↓

**MoneyWheel Diagnostic Output**

**Initial phase ends here.**

Downstream architecture begins after this boundary:

**MoneyWheel / Financial State → Constraints → Goal Planner → Strategy Applicability → 8-Fit Eligibility → Decision / Ranking → Strategy Version → Actions**

Those downstream layers are intentionally outside this document.

## 10. Data Ownership Matrix

| Layer | Source of Truth | Owns | Does Not Own |
|---|---|---|---|
| Onboarding | Persisted source records | Investor-entered financial inputs | Derived financial ratios |
| Financial State | FinancialStateService + current snapshot | Normalized current financial position and snapshot lineage | MoneyWheel classifications |
| Canonical Calculations | backend/engines/calculation/canonical.py | Shared financial formulas | Planning policy |
| MoneyWheel Rules | backend/rules/moneywheel.py | MoneyWheel thresholds, metric definitions and classification | Raw financial data; strategy eligibility |
| MoneyWheel Engine | backend/engines/moneywheel/engine.py | Assemble ratios/rules into MoneyWheel result | Constraint hard-gating |
| Constraints | Constraint policy/evaluator | Planning restrictions and warnings | MoneyWheel's diagnostic presentation |
| Strategy Decision | backend/engines/strategy/decision.py | Candidate selection and ranking | Raw onboarding collection |

## 11. Code Ownership

| Responsibility | Current Code Path |
|---|---|
| Onboarding orchestration/state | frontend/components/onboarding/OnboardingProvider.tsx |
| Onboarding entry | frontend/app/investor/onboarding/page.tsx |
| Financial State service | backend/services/financial_state_service.py |
| Financial State engine | backend/engines/financial_state/engine.py |
| Canonical calculations | backend/engines/calculation/canonical.py |
| MoneyWheel engine | backend/engines/moneywheel/engine.py |
| MoneyWheel rules/classification | backend/rules/moneywheel.py |
| MoneyWheel UI | frontend/app/investor/moneywheel/page.tsx |

## 12. Architecture Principles

1. **Onboarding collects facts; it does not become the financial calculation engine.**
2. **Financial State normalizes and snapshots the current financial position.**
3. **Canonical calculations own shared formulas.**
4. **MoneyWheel owns diagnostic classification and explanation.**
5. **MoneyWheel does not directly select a strategy.**
6. **A MoneyWheel “Critical” status is diagnostic evidence, not automatically a strategy Fail.**
7. **Constraints own the policy decision when a financial condition becomes a planning restriction.**
8. **Missing data remains explicitly unavailable; no synthetic financial value is invented.**
9. **Rule versions must remain identifiable so MoneyWheel results are reproducible.**
10. **The initial architecture phase ends at MoneyWheel diagnostic output.**
