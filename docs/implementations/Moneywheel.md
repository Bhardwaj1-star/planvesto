# Moneywheel — Final Implementation Specification

**Document type:** Authoritative implementation specification  
**Scope:** Moneywheel metrics/constraints consumed by Goal Planner and Strategy Builder, including portfolio-level required return  
**Status:** Feature definition aur existing-feature audit se consolidated implementation contract. Existing behavior ke liye audit evidence authoritative baseline hai; Weighted Debt Rate, Investment–Debt Spread aur Portfolio-Level Return Required ko specified additions ke roop mein treat kiya gaya hai, completed implementation ke roop mein nahi. Goal-Level Return Required ka owner Goal Planner hai. Downstream wiring aur portfolio-level calculation model abhi separately verify/finalize hone hain.  
**Audited source baseline:** d7640029310c8e58d4cdd9a033d7683b5ea10002 (not a claim about production deployment).

## 1. Design references

This specification keeps inspected code evidence separate from intended business behavior.

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

Where existing behavior differs from required behavior, preserve that distinction. The audit is not proof of production deployment or current live runtime state; business-rule references are not proof that a requirement is implemented.


## 2. Purpose and ownership

Moneywheel calculates and presents an investor's financial measurements as **constraint and evidence inputs** for planning. It must not independently choose a goal funding path, strategy, variant, technique, solution, or accepted plan.

- **Moneywheel:** Calculates metrics, availability, status where a rule exists, and traceable snapshots.
- **Goal Planner / Goal Feasibility:** Uses relevant metrics to assess funding requirements, feasibility, funding gaps, and alternative financial paths.
- **Strategy Builder:** Consumes feasibility context and Moneywheel evidence for strategy eligibility and implementation design.
- **Canonical constraint/decision layer:** Owns the distinction between hard constraints, eligibility, warnings, and recommendation evidence. A Moneywheel health status is not automatically a hard block.
- **Accepted Plan / Action Plan:** A Moneywheel refresh does not accept a proposal, overwrite an Accepted Plan, or complete an action.

Moneywheel is the canonical calculation owner for these metrics. Downstream consumers must use its returned values and metadata rather than independently recalculating the same metric.

## 3. Consolidated rules and disposition

| ID | Rule | Disposition |
|---|---|---|
| MW-BR-01 | Use authoritative server-side Financial State; client-supplied snapshots must not override it. | Preserve existing API behavior. |
| MW-BR-02 | Missing input, invalid denominator, or non-finite result is unavailable, not zero and not healthy. | Preserve existing engine contract. |
| MW-BR-03 | Preserve the current nine-metric runtime contract until an explicit compatibility change is approved. The target contract retires Moneywheel's legacy `required_rate_of_return` calculation because Goal Planner owns goal-level required return, and introduces `portfolio_level_return_required` as the portfolio-level measure. | Keep the current API/snapshot compatible during transition; explicitly migrate schema, persistence, history, frontend, tests, and old snapshots before changing the contract. |
| MW-BR-04 | Add Weighted Debt Rate, Investment–Debt Spread, and Portfolio-Level Return Required as Moneywheel measurements. | Required additions; portfolio-return calculation contract must be finalized before implementation. |
| MW-BR-05 | Debt existence, DTI, leverage, or a negative spread must not alone select Debt Reduction or another strategy. | Required business rule. |
| MW-BR-06 | Moneywheel supplies metrics/evidence; canonical decision rules determine whether a condition is a hard constraint, eligibility input, warning, or diagnostic. | Required ownership boundary. |
| MW-BR-07 | Goal Planner owns goal-level feasibility and funding-path comparison; Strategy Builder consumes that result and designs execution. | Required cross-feature boundary. |
| MW-BR-08 | An asset mapped to a goal is not automatically earmarked, locked, sold, or unavailable elsewhere. | Required business rule. |
| MW-BR-09 | A material Financial State or goal change may require recalculation/revalidation, but does not automatically replace a strategy or accepted plan. | Required lifecycle boundary. |
| MW-BR-10 | Proposed alternatives remain scenarios until investor adoption. “No acceptable path” is a valid outcome. | Required lifecycle boundary. |
| MW-BR-11 | Portfolio-Level Return Required must use Goal Planner's versioned goal-level requirements and explicit portfolio cash flows; it is not the arithmetic average of goal-level returns. | Required cross-feature measurement; define/validate calculation contract and dependencies before implementation. |

### Rule-role distinction

Each downstream rule must declare its role:

- **Diagnostic:** describes a financial condition.
- **Warning:** signals attention but does not itself block planning.
- **Eligibility input:** contributes to whether a specific strategy fits.
- **Hard constraint:** blocks or materially restricts planning only under an explicitly defined condition.
- **Recommendation evidence:** helps explain or compare alternatives.

Do not turn every critical Moneywheel status into a universal hard constraint. Preserve the existing constraint evaluator's scope unless canonical rules are explicitly changed and tested.

## 4. Canonical metric inventory

After implementation, Moneywheel will return **11 canonical metrics**: eight retained existing Moneywheel metrics, two debt metrics, and Portfolio-Level Return Required. Goal-Level Return Required is owned by Goal Planner, not Moneywheel.

### 4.1 Existing nine — preserve current contracts

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
| required_rate_of_return | Required Rate of Return (legacy) | ((Future Goal Target / Current Goal Funding)^(1 / Goal Duration Years) − 1) × 100 | Excellent <8%; healthy 8–12%; attention 12–15%; critical ≥15%. Retain only for current-runtime compatibility until migration is approved. |




**Legacy metric transition:** The current code still returns nine metrics, including `required_rate_of_return`. That existing row above documents current runtime behavior only. The intended target contract has eight retained existing metrics, two debt metrics, and `portfolio_level_return_required` (eleven total). Do not remove or rename the legacy key in code until API consumers, historical snapshots, persistence, frontend rendering, and tests have an explicit compatibility/migration plan.

For DTI, preserve the exact constants and boundary comparisons in the current rules source. The current implementation imports DTI and savings benchmarks from the canonical constraint policy; do not create a second source of truth.

If required inputs are missing, a denominator is zero, required-return inputs are invalid, or a result is non-finite, return unavailable with a reason. Aggregate status remains incomplete when any canonical metric is unavailable. Do not manufacture an overall healthy status.

### 4.2 New metric — Weighted Debt Rate

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

### 4.3 New metric — Investment–Debt Spread

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

### 4.4 New measurement — Portfolio-Level Return Required

**Canonical key:** portfolio_level_return_required  
**Unit:** annualized percentage (%)  
**Owner:** Moneywheel, using Goal Planner's versioned Goal-Level Return Required and goal funding/target-date evidence as inputs where relevant.

**Purpose:** Estimate the portfolio-level annualized return required to fund the included goals under an explicit shared portfolio funding model. This is a portfolio measurement, not a strategy recommendation and not an average of individual goal returns.

**Calculation contract:** The precise solver and output semantics must be finalized before implementation. At minimum, the model must explicitly define:
- which goals are included and their target-date cash outflows/required corpus;
- current portfolio assets included, their eligibility and allocation/availability;
- future contributions, contribution timing, and any planned withdrawals;
- goal-specific funding already ring-fenced or otherwise unavailable to other goals, where an authoritative earmarking/allocation exists;
- whether the model assumes one pooled portfolio or distinct goal-specific portfolios;
- return compounding/annualization convention and reference date;
- treatment of inflation-adjusted target amounts and any other modeled cash flows;
- how shared assets/surplus are prevented from being double-counted.

A single portfolio-level required return cannot be derived by taking a simple arithmetic mean of goal-level required returns. Different goal dates, amounts, current funding, contributions, and withdrawals make that invalid. The model must solve against the combined dated obligations and cash flows, or return unavailable/indeterminate if the defined model does not support a meaningful unique result.

**Cross-feature dependency and sequencing:** Goal Planner first calculates goal-level requirements and, where valid, Goal-Level Return Required for each goal/scenario. Moneywheel then calculates Portfolio-Level Return Required from the relevant versioned goal results and explicit portfolio-level cash-flow/resource assumptions. This dependency must be one-way for this measurement; Goal Planner must not require Portfolio-Level Return Required to calculate Goal-Level Return Required, avoiding a circular dependency. Goal Feasibility may consume the portfolio-level result as additional evidence after it is available.

**Interpretation and limitations:** This is the return mathematically required under the declared pooled-resource/cash-flow model, not an expected or guaranteed return and not proof that the portfolio can achieve it within the investor's risk limits. Compare it with an independently declared, risk-appropriate return assumption only on a comparable basis. A high required return must trigger constraint-aware feasibility/adjustment analysis, not an automatic increase in risk.

**Availability:** Return unavailable with a reason if goal data, dated cash flows, resource scope, contribution assumptions, or required version metadata are missing/invalid; if shared resources cannot be reconciled; or if the defined solver cannot produce a meaningful result. Do not substitute the average of goal returns, a universal default, zero, or an arbitrary fallback.

**Status bands:** Do not invent health/status bands in the initial implementation. Return the numeric value, assumptions, included-goal/resource scope, and availability metadata.


## 5. Planning rules

1. **Authoritative source:** Build calculation input from server-owned Financial State and relevant server-side goal context. Preserve authentication and planning-unit ownership checks.
2. **Goal context:** Goal-dependent metrics require goal-specific funding, target, future target, projection, and duration inputs as applicable. Do not assume all metrics can be calculated from Financial State alone.
3. **Traceability:** Each result must be traceable to the Financial State/goal context used. Preserve stored snapshots, timestamps, and rule-set/version metadata.
4. **Freshness:** After a material Financial State or goal-input change, recalculate affected metrics before using them for a new feasibility or eligibility assessment. Materiality thresholds and targeted revalidation belong to the shared planning lifecycle, not an ad hoc Moneywheel threshold.
5. **Multi-goal use:** Moneywheel can supply evidence to whole-plan analysis; it does not allocate shared surplus or decide which goal loses funding.
6. **Asset mapping:** Mapped assets may inform Goal Planner funding analysis, but mapping alone does not reserve the asset. Do not silently count one resource as fully available to multiple goals; conflict resolution belongs to planning/whole-plan analysis.
7. **No plan mutation:** Calculation or status change does not accept/reject a proposal, update an Accepted Plan, or complete an Action Plan item.
8. **Scenario assumptions:** Investment-return assumptions used in Investment–Debt Spread must come from the relevant scenario and be displayed with the result. They are not guaranteed returns.

## 6. Business rules for downstream consumers

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
- Keep Strategy, Variant, Technique/Method, Solution, and implementation as distinct concepts according to the canonical taxonomy.
- Do not accept a proposal or replace a strategy/plan solely because a Moneywheel metric changed.

### Canonical constraint/decision layer
- For each metric-derived rule, define rule ID, role, condition, severity/priority, result semantics, explanation, and owner.
- Preserve the existing emergency-reserve and DTI constraint scope; they are not universal blocks for every goal.
- Keep warnings/diagnostics separate from hard constraints.
- Resolve conflicting constraint sources through the canonical constraint mechanism rather than silently taking the latest result.

## 7. Output contract

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

## 8. API, persistence, and UI requirements

- Preserve authenticated calculate/latest/history behavior and planning-unit ownership enforcement.
- Keep server-side Financial State authoritative; client snapshot fields must not override it.
- Extend the canonical key registry, typed result model, engine, API schemas, and availability handling.
- Persist both new metrics and their metadata in append-only snapshots.
- Render the new metrics in a consistent Debt & Solvency grouping; do not present them as automatic recommendations.
- Display unavailable values as unavailable with an explanation, never as zero fallback.
- Verify production migration/RLS independently; source migration files do not prove production state.

## 9. Acceptance criteria

1. The current runtime's nine metrics retain their formulas, units, thresholds, and boundary behavior until a compatibility change is approved. The target contract retains eight existing metrics, retires Moneywheel's legacy `required_rate_of_return` ownership, and adds the two debt metrics plus `portfolio_level_return_required`; Goal Planner owns goal-level required return.
2. The intended Moneywheel output contains eleven canonical metrics after the ownership change: eight retained existing metrics, two debt metrics, and Portfolio-Level Return Required. Goal-Level Return Required is calculated by Goal Planner. Legacy snapshot compatibility is explicit.
3. Weighted Debt Rate is principal-weighted, never a simple average.
4. Investment–Debt Spread uses the explicitly supplied annual return assumption minus Weighted Debt Rate, expressed in percentage points.
4a. Portfolio-Level Return Required uses explicit dated portfolio obligations/resources and versioned Goal Planner outputs; it is never a simple average of goal-level returns.
4b. Goal-Level Return Required has one calculation owner (Goal Planner); Moneywheel does not retain a competing formula.
5. Missing, invalid, zero-denominator, incomparable, and non-finite inputs return unavailable with a reason.
6. No invented health bands or hidden default return assumption for the new metrics.
7. API continues to ignore client-supplied Financial State as calculation authority and enforces planning-unit ownership.
8. Persistence, latest/history, frontend, and schema validation support the new metrics.
9. Moneywheel refresh does not choose a strategy, change goal priority, earmark assets, or mutate Accepted Plan/Action Plan state.
10. Goal Planner and Strategy Builder consume a typed canonical output rather than duplicate formulas.
11. Tests prove that diagnostic, warning, eligibility, and hard constraint are distinct.
12. Tests cover threshold boundaries, partial availability, weighted-rate arithmetic, spread sign/units, portfolio-level cash-flow solving/availability, goal-return ownership, historical compatibility, and cross-feature non-mutation.
13. Existing Moneywheel tests are run and results recorded; locating tests is not proof that they pass.
14. Deployment/database/RLS claims are made only after target-environment verification.

## 10. Explicit non-goals

This specification does not authorize redesigning all existing ratios/thresholds, automatic Debt Reduction/Investment selection from a single metric, unapproved status bands, a separate hard-constraint engine inside Moneywheel, automatic changes to goal priority/strategy/Accepted Plan/asset earmarking/Action Plan, or claims that tests/deployments/production RLS are verified without evidence. It also does not authorize implementing Portfolio-Level Return Required until its cash-flow solver, goal inclusion/allocation rules, and legacy `required_rate_of_return` migration/compatibility are explicitly reviewed.
