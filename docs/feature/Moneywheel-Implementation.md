# Moneywheel — Final Implementation Specification

**Document type:** Authoritative implementation specification  
**Scope:** Moneywheel metrics/constraints consumed by Goal Planner and Strategy Builder  
**Status:** Requirements consolidated. Existing behavior is code-verified in the Moneywheel evidence documents; the two debt metrics are required additions. Downstream wiring must be verified during implementation.  
**Audited source baseline:** d7640029310c8e58d4cdd9a033d7683b5ea10002 (not a claim about production deployment).

## 1. Purpose and ownership

Moneywheel calculates and presents an investor's financial measurements as **constraint and evidence inputs** for planning. It must not independently choose a goal funding path, strategy, variant, technique, solution, or accepted plan.

- **Moneywheel:** Calculates metrics, availability, status where a rule exists, and traceable snapshots.
- **Goal Planner / Goal Feasibility:** Uses relevant metrics to assess funding requirements, feasibility, funding gaps, and alternative financial paths.
- **Strategy Builder:** Consumes feasibility context and Moneywheel evidence for strategy eligibility and implementation design.
- **Canonical constraint/decision layer:** Owns the distinction between hard constraints, eligibility, warnings, and recommendation evidence. A Moneywheel health status is not automatically a hard block.
- **Accepted Plan / Action Plan:** A Moneywheel refresh does not accept a proposal, overwrite an Accepted Plan, or complete an action.

Moneywheel is the canonical calculation owner for these metrics. Downstream consumers must use its returned values and metadata rather than independently recalculating the same metric.

## 2. Consolidated rules and disposition

| ID | Rule | Disposition |
|---|---|---|
| MW-BR-01 | Use authoritative server-side Financial State; client-supplied snapshots must not override it. | Preserve existing API behavior. |
| MW-BR-02 | Missing input, invalid denominator, or non-finite result is unavailable, not zero and not healthy. | Preserve existing engine contract. |
| MW-BR-03 | Preserve the nine existing canonical metrics, formulas, units, and thresholds unless separately approved. | Preserve and regression-test. |
| MW-BR-04 | Add Weighted Debt Rate and Investment–Debt Spread as Moneywheel metrics. | Required addition. |
| MW-BR-05 | Debt existence, DTI, leverage, or a negative spread must not alone select Debt Reduction or another strategy. | Required business rule. |
| MW-BR-06 | Moneywheel supplies metrics/evidence; canonical decision rules determine whether a condition is a hard constraint, eligibility input, warning, or diagnostic. | Required ownership boundary. |
| MW-BR-07 | Goal Planner owns goal-level feasibility and funding-path comparison; Strategy Builder consumes that result and designs execution. | Required cross-feature boundary. |
| MW-BR-08 | An asset mapped to a goal is not automatically earmarked, locked, sold, or unavailable elsewhere. | Required business rule. |
| MW-BR-09 | A material Financial State or goal change may require recalculation/revalidation, but does not automatically replace a strategy or accepted plan. | Required lifecycle boundary. |
| MW-BR-10 | Proposed alternatives remain scenarios until investor adoption. “No acceptable path” is a valid outcome. | Required lifecycle boundary. |

### Rule-role distinction

Each downstream rule must declare its role:

- **Diagnostic:** describes a financial condition.
- **Warning:** signals attention but does not itself block planning.
- **Eligibility input:** contributes to whether a specific strategy fits.
- **Hard constraint:** blocks or materially restricts planning only under an explicitly defined condition.
- **Recommendation evidence:** helps explain or compare alternatives.

Do not turn every critical Moneywheel status into a universal hard constraint. Preserve the existing constraint evaluator's scope unless canonical rules are explicitly changed and tested.

## 3. Canonical metric inventory

After implementation, Moneywheel will return **11 canonical metrics**.

### 3.1 Existing nine — preserve current contracts

The formulas and thresholds below reflect the inspected backend/rules/moneywheel.py source. Do not move calculation authority to the UI.

| Key | Metric | Formula | Current status bands |
|---|---|---|---|
| savings_rate | Savings Rate | (Income − Expenses) / Income × 100 | Excellent ≥30%; healthy from configured savings benchmark to 30%; attention 10% to benchmark; critical <10%. |
| liquid_asset_ratio | Liquid Asset Ratio | Liquid Assets / Total Assets × 100 | Excellent ≥25%; healthy 15–25%; attention 10–15%; critical <10%. |
| debt_to_income_ratio | Debt-to-Income Ratio | Monthly Debt Payments / Gross Monthly Income × 100 | Preserve exact existing policy constants and comparator semantics. |
| leverage_ratio | Leverage Ratio | Total Liabilities / Total Assets × 100 | Excellent <20%; healthy 20–30%; attention 30–50%; critical ≥50%. |
| financial_asset_ratio | Financial Asset Ratio | Financial Assets / Total Assets × 100 | Excellent ≥70%; healthy 50–70%; attention 30–50%; critical <30%. |
| insurance_coverage_ratio | Insurance Coverage Ratio | Existing Sum Assured / Required Insurance Cover × 100 | Excellent ≥80%; healthy 60–80%; attention 40–60%; critical <40%. |
| goal_funding_ratio | Goal Funding Ratio | Current Goal Funding / Goal Target Amount × 100 | Excellent ≥100%; healthy 80–100%; attention 50–80%; critical <50%. |
| future_funding_ratio | Future Funding Ratio | Projected Goal Funding / Future Goal Target × 100 | Excellent ≥100%; healthy 80–100%; attention 50–80%; critical <50%. |
| required_rate_of_return | Required Rate of Return | ((Future Goal Target / Current Goal Funding)^(1 / Goal Duration Years) − 1) × 100 | Excellent <8%; healthy 8–12%; attention 12–15%; critical ≥15%. |

For DTI, preserve the exact constants and boundary comparisons in the current rules source. The current implementation imports DTI and savings benchmarks from the canonical constraint policy; do not create a second source of truth.

If required inputs are missing, a denominator is zero, required-return inputs are invalid, or a result is non-finite, return unavailable with a reason. Aggregate status remains incomplete when any canonical metric is unavailable. Do not manufacture an overall healthy status.

### 3.2 New metric — Weighted Debt Rate

**Canonical key:** weighted_debt_rate  
**Unit:** annual percentage rate (%)

**Purpose:** Summarize annual interest rates for included outstanding debts, weighted by each debt's outstanding principal.

**Formula:**

Sum(outstanding_principalᵢ × annual_interest_rateᵢ) / Sum(outstanding_principalᵢ)

If rates are stored as decimals, convert the result to percentage for display.

**Inputs and rules**
- One record per included debt, with outstanding principal and applicable annual interest rate.
- All rates must use a comparable annual basis.
- Fully repaid debts with zero outstanding principal do not affect the weighted average.
- Missing principal/rate or incomparable rate conventions must not be silently replaced with zero.
- If there are no eligible outstanding debts, total eligible principal is zero, or required inputs are invalid/missing, return unavailable with a reason.
- Never substitute a simple arithmetic average.

**Interpretation and boundaries:** This summarizes the stated rates for included debts. It is not automatically an effective APR or total borrowing cost. Fees, penalties, tax effects, prepayment charges, floating-rate changes, and repayment schedules are excluded unless explicitly modeled through a separately defined input contract.

**Status bands:** Do not invent excellent/healthy/attention/critical bands for the initial implementation. Return the numeric value and availability. A threshold rule may be added only through explicit canonical rule registration.

### 3.3 New metric — Investment–Debt Spread

**Canonical key:** investment_debt_spread  
**Unit:** percentage points (pp)

**Purpose:** Compare a clearly identified investment-return assumption with the Weighted Debt Rate.

**Formula:**

Relevant annual investment-return assumption − Weighted Debt Rate

**Inputs and rules**
- A valid Weighted Debt Rate.
- An explicitly identified annual investment-return assumption relevant to the goal/path being evaluated.
- Comparable annual basis and percentage convention.
- Result metadata identifies the assumption and its source/context, such as the Goal Planner scenario. Do not silently use a universal default return.
- If either input is unavailable, missing, invalid, or incomparable, return unavailable with a reason.

**Interpretation:** Positive means the assumed return is above the weighted stated debt rate; negative means it is below; zero means the assumptions are equal. This is a comparison of assumptions, not guaranteed performance or a risk-adjusted profit calculation. It must not independently choose between debt repayment and investment.

Goal Planner should compare complete feasible paths, including cash flow, liquidity, goal timing, investment uncertainty, debt cost/tenure, and competing goals.

**Status bands:** Do not invent health bands in the initial implementation. Return the spread in percentage points and expose its assumptions.

## 4. Planning rules

1. **Authoritative source:** Build calculation input from server-owned Financial State and relevant server-side goal context. Preserve authentication and planning-unit ownership checks.
2. **Goal context:** Goal-dependent metrics require goal-specific funding, target, future target, projection, and duration inputs as applicable. Do not assume all metrics can be calculated from Financial State alone.
3. **Traceability:** Each result must be traceable to the Financial State/goal context used. Preserve stored snapshots, timestamps, and rule-set/version metadata.
4. **Freshness:** After a material Financial State or goal-input change, recalculate affected metrics before using them for a new feasibility or eligibility assessment. Materiality thresholds and targeted revalidation belong to the shared planning lifecycle, not an ad hoc Moneywheel threshold.
5. **Multi-goal use:** Moneywheel can supply evidence to whole-plan analysis; it does not allocate shared surplus or decide which goal loses funding.
6. **Asset mapping:** Mapped assets may inform Goal Planner funding analysis, but mapping alone does not reserve the asset. Do not silently count one resource as fully available to multiple goals; conflict resolution belongs to planning/whole-plan analysis.
7. **No plan mutation:** Calculation or status change does not accept/reject a proposal, update an Accepted Plan, or complete an Action Plan item.
8. **Scenario assumptions:** Investment-return assumptions used in Investment–Debt Spread must come from the relevant scenario and be displayed with the result. They are not guaranteed returns.

## 5. Business rules for downstream consumers

### Goal Planner / Goal Feasibility
- Consume Moneywheel values as evidence for goal feasibility and funding-gap analysis.
- Evaluate debt through alternative financial paths when relevant; debt alone does not prove Debt Reduction is best.
- Compare impacts on goal funding, monthly surplus, interest, liquidity, timing, uncertainty, and other goals when relevant.
- Goal Funding is a feasibility/funding-path responsibility, not an additional Strategy Builder strategy.
- A single ratio or feasibility result does not prove that one path is best.

### Strategy Builder
- Consume Goal Planner feasibility/funding context plus relevant Moneywheel constraints.
- Apply the canonical hard-constraint gate and strategy-specific eligibility rules as separate layers.
- Do not recreate Moneywheel formulas or thresholds downstream.
- Only an explicitly registered rule can make a metric a hard constraint.
- Keep Strategy, Variant, Technique/Method, Architecture/Solution, and implementation as distinct decision objects according to the canonical taxonomy.
- Do not accept a proposal or replace a strategy/plan solely because a Moneywheel metric changed.

### Canonical constraint/decision layer
- For each metric-derived rule, define rule ID, role, condition, severity/priority, result semantics, explanation, and owner.
- Preserve the existing emergency-reserve and DTI constraint scope; they are not universal blocks for every goal.
- Keep warnings/diagnostics separate from hard constraints.
- Resolve conflicting constraint sources through the canonical constraint mechanism rather than silently taking the latest result.

## 6. Output contract

Each metric result must include:
- canonical key and display name;
- nullable numeric value;
- unit (% or pp);
- formula/definition;
- availability state and reason when unavailable;
- status where a status rule exists;
- explanation;
- calculation timestamp and rule-set/version metadata.

The overall result must preserve completeness/status behavior, the Financial State snapshot, relevant goal/scenario context, and historical snapshots.

For Weighted Debt Rate, expose the included-debt scope and annual rate convention. For Investment–Debt Spread, expose the chosen investment-return assumption and its scenario/source label.

If the current response schema enforces exactly nine metrics, update schemas, models, tests, persistence, history responses, and frontend rendering so new calculations have eleven metrics without unexpectedly breaking old clients. Preserve compatibility for historical nine-metric snapshots; do not pretend old snapshots contain the new metrics.

## 7. API, persistence, and UI requirements

- Preserve authenticated calculate/latest/history behavior and planning-unit ownership enforcement.
- Keep server-side Financial State authoritative; client snapshot fields must not override it.
- Extend the canonical key registry, typed result model, engine, API schemas, and availability handling.
- Persist both new metrics and their metadata in append-only snapshots.
- Render the new metrics in a consistent Debt & Solvency grouping; do not present them as automatic recommendations.
- Display unavailable values as unavailable with an explanation, never as zero fallback.
- Verify production migration/RLS independently; source migration files do not prove production state.

## 8. Acceptance criteria

1. Existing nine metrics retain their formulas, units, thresholds, and boundary behavior unless separately approved.
2. New calculations contain exactly eleven canonical metrics.
3. Weighted Debt Rate is principal-weighted, never a simple average.
4. Investment–Debt Spread uses the explicitly supplied annual return assumption minus Weighted Debt Rate, expressed in percentage points.
5. Missing, invalid, zero-denominator, incomparable, and non-finite inputs return unavailable with a reason.
6. No invented health bands or hidden default return assumption for the new metrics.
7. API continues to ignore client-supplied Financial State as calculation authority and enforces planning-unit ownership.
8. Persistence, latest/history, frontend, and schema validation support the new metrics.
9. Moneywheel refresh does not choose a strategy, change goal priority, earmark assets, or mutate Accepted Plan/Action Plan state.
10. Goal Planner and Strategy Builder consume a typed canonical output rather than duplicate formulas.
11. Tests prove that diagnostic, warning, eligibility, and hard constraint are distinct.
12. Tests cover threshold boundaries, partial availability, weighted-rate arithmetic, spread sign/units, historical compatibility, and cross-feature non-mutation.
13. Existing Moneywheel tests are run and results recorded; locating tests is not proof that they pass.
14. Deployment/database/RLS claims are made only after target-environment verification.

## 9. Coding-agent sequence

1. Read this specification and the existing Moneywheel evidence documents before editing.
2. Inspect current schemas/models and all consumers of the nine-metric contract.
3. Trace debt records and the relevant return assumption to authoritative sources; do not invent fields or defaults.
4. Extend registry, models, calculations, availability handling, API schemas, persistence, history, and UI for both new metrics.
5. Version the contract compatibly and preserve reading of old snapshots.
6. Wire Goal Planner and Strategy Builder to consume canonical Moneywheel output; do not duplicate formulas.
7. Confirm each downstream rule's role in the canonical constraint registry. Do not promote diagnostics to hard constraints without explicit ownership.
8. Add unit, API-contract, adapter, service, persistence/history, frontend, and integration tests.
9. Run tests and record actual outcomes, including tests not run.
10. Report changed files, source-data gaps, migrations, test results, and deployment verification separately.

## 10. Source documents and authority

### Existing-code evidence — baseline for current behavior
- docs/existing features/Moneywheel/00-BACKEND-INDEX.md
- docs/existing features/Moneywheel/01-API-AND-CALCULATION-FLOW.md
- docs/existing features/Moneywheel/02-RATIO-CONTRACTS-AND-RULES.md
- docs/existing features/Moneywheel/03-PERSISTENCE-UI-AND-INTEGRATIONS.md
- docs/existing features/Moneywheel/04-TESTS-AND-EVIDENCE-GAPS.md
- backend/rules/moneywheel.py

### Business-rule evidence — intended boundaries, not proof of implementation
- docs/Real-Life Decision Cases/00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md — debt economics, opportunity cost, and the two new debt metrics.
- Cases 3–4 — multi-goal feasibility, better-path comparison, and proposals before adoption.
- Cases 5–6 — recalculation/revalidation without automatic plan replacement.
- Cases 7–12 — new-goal scenarios, strategy/implementation changes, investor adoption, and no-acceptable-path behavior.
- Case 15 — asset mapping is distinct from earmarking.
- docs/Real-Life Decision Cases/16-CONCEPTS_OUTSIDE_EXISTING_FEATURES_REGISTER.md and FULL_AUDIT_REPORT.md — shared constraint ownership and taxonomy gaps.

## 11. Explicit non-goals

This specification does not authorize redesigning all existing ratios/thresholds, automatic Debt Reduction/Investment selection from a single metric, unapproved status bands, a separate hard-constraint engine inside Moneywheel, automatic changes to goal priority/strategy/Accepted Plan/asset earmarking/Action Plan, or claims that tests/deployments/production RLS are verified without evidence.
