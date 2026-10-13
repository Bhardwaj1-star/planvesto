# Moneywheel — Financial Planner Guide

## 1. What Moneywheel does

Moneywheel summarizes a client's financial position through key ratios and measurements. These measurements help the financial planner understand savings, liquidity, debt, asset structure, insurance coverage, and goal funding.

**Moneywheel provides financial evidence; it does not make the decision for the planner.**
- **Moneywheel:** Calculates and explains financial measurements.
- **Goal Planner:** Assesses whether each goal is achievable and compares funding options.
- **Strategy Builder:** Uses feasibility results and relevant constraints to design a suitable approach.
- A warning or poor ratio is not automatically a reason to reject a goal or choose a strategy.

## 2. Core measurements

The following are the existing Moneywheel measurements. Thresholds shown here should be treated as the current documented bands, not universal financial-planning standards.

| Measurement | What it tells the planner | Calculation | Current interpretation |
|---|---|---|---|
| Savings Rate | How much of income remains after expenses | (Income − Expenses) ÷ Income × 100 | Excellent: ≥30%; Healthy: configured benchmark to 30%; Attention: 10% to benchmark; Critical: <10% |
| Liquid Asset Ratio | How much of total assets is held in liquid assets | Liquid Assets ÷ Total Assets × 100 | Excellent: ≥25%; Healthy: 15–25%; Attention: 10–15%; Critical: <10% |
| Debt-to-Income Ratio (DTI) | How much gross monthly income goes toward monthly debt payments | Monthly Debt Payments ÷ Gross Monthly Income × 100 | Use the system's approved DTI policy and exact boundary rules; do not create a separate threshold |
| Leverage Ratio | How large liabilities are relative to total assets | Total Liabilities ÷ Total Assets × 100 | Excellent: <20%; Healthy: 20–30%; Attention: 30–50%; Critical: ≥50% |
| Financial Asset Ratio | How much of total assets is held in financial assets | Financial Assets ÷ Total Assets × 100 | Excellent: ≥70%; Healthy: 50–70%; Attention: 30–50%; Critical: <30% |
| Insurance Coverage Ratio | How current sum assured compares with required insurance cover | Existing Sum Assured ÷ Required Insurance Cover × 100 | Excellent: ≥80%; Healthy: 60–80%; Attention: 40–60%; Critical: <40% |
| Goal Funding Ratio | How much of a goal's target is funded today | Current Goal Funding ÷ Goal Target Amount × 100 | Excellent: ≥100%; Healthy: 80–100%; Attention: 50–80%; Critical: <50% |
| Future Funding Ratio | How projected funding compares with the future goal target | Projected Goal Funding ÷ Future Goal Target × 100 | Excellent: ≥100%; Healthy: 80–100%; Attention: 50–80%; Critical: <50% |

### How to use these measurements

- Read a ratio alongside the client's circumstances, goal dates, cash flow, liquidity needs, and risk capacity.
- Treat a status band as a signal to investigate—not as a complete financial recommendation.
- A low liquid-asset ratio may warrant a liquidity review; it does not, by itself, establish the exact emergency-fund requirement.
- DTI and leverage describe different things: DTI compares debt payments with income, while leverage compares liabilities with assets.
- Goal funding measurements depend on reliable goal targets, current funding, projections, and time horizons.

## 3. New debt-related measurements

These measurements are specified for the intended Moneywheel design. They should not be described as live/implemented until the implementation is verified.

### A. Weighted Debt Rate

**Purpose:** Shows the average stated annual interest rate across included outstanding debts, weighted by outstanding principal.

**Calculation:**

Sum of (each debt's outstanding principal × its annual interest rate) ÷ total included outstanding principal.

**Planner interpretation**
- Use comparable annual interest-rate figures and current outstanding balances.
- A debt with a larger outstanding principal has a greater influence on the result.
- Do not use a simple average of the interest rates.
- This is not necessarily the client's full borrowing cost: fees, penalties, tax effects, prepayment charges, and future floating-rate changes are excluded unless separately modeled.
- If the necessary debt data is missing or invalid, the result should be shown as unavailable—not zero.

### B. Investment–Debt Spread

**Purpose:** Compares an explicitly stated annual investment-return assumption with the Weighted Debt Rate.

**Calculation:** Relevant annual investment-return assumption − Weighted Debt Rate.

The result is expressed in **percentage points (pp)**.

**Planner interpretation**
- Positive spread: the assumed investment return is higher than the stated weighted debt rate.
- Negative spread: the assumed investment return is lower.
- Zero spread: both assumptions are equal.
- This is a comparison of assumptions, not a promise of investment performance or a risk-adjusted profit calculation.
- Do not choose investing or debt repayment from this spread alone. Compare realistic alternatives, including liquidity, monthly cash flow, goal deadlines, debt terms, taxes/charges where relevant, and investment uncertainty.
- The return assumption and its source/scenario must be clear. Do not silently insert a default return.

No health bands are defined for these two new measurements. Do not invent them.

## 4. Portfolio-Level Return Required

**Purpose:** Estimates the annualized return required from the combined portfolio to meet the included goals under an explicitly defined model of assets, contributions, withdrawals, and goal dates.

This is different from a goal's individual required return:
- **Goal-Level Return Required belongs to Goal Planner.**
- **Portfolio-Level Return Required belongs to Moneywheel**, using the relevant, versioned Goal Planner results and portfolio cash-flow assumptions.

**Important:** The portfolio-level return must not be calculated as a simple average of the individual goal returns. Goals can have different target amounts, dates, current funding, contributions, and withdrawals.

Before this measurement can be relied on, its calculation method must clearly define:
- Which goals and target dates are included.
- Which current assets and future contributions are available, and when.
- Planned withdrawals and any genuinely earmarked funds.
- Whether goals share one pooled portfolio or use separate portfolios.
- How inflation-adjusted targets, compounding, and annualization are handled.
- How the same asset or surplus is prevented from being counted toward multiple goals.

**Planner interpretation**
- This is the return required under stated assumptions—not the expected or guaranteed return.
- Compare it with a separately chosen, risk-appropriate return assumption.
- If the required return appears too high, review feasibility, goal timing, contributions, spending, and priorities. Do not automatically increase investment risk.
- If the inputs are incomplete or the model cannot produce a meaningful result, show the measure as unavailable with a reason.

**Implementation status:** The repository specification describes this as a required addition, but the calculation model and downstream integration still need verification. Do not present it as a confirmed live calculation without that evidence.

## 5. Missing or unreliable information

When a required input is missing, invalid, or cannot support a valid calculation:
- Show the measurement as **Unavailable** and explain why.
- Do not substitute zero or label the client healthy.
- If one or more measurements are unavailable, make the overall result's incomplete status clear.
- Review whether the source financial information or goal assumptions need correction before using the result.

Calculations should use the authoritative financial information and relevant goal data held by the system, not an unverified value entered only in a screen.

## 6. How Moneywheel fits into the planning process

1. Review the client's financial measurements and any unavailable values.
2. Identify the financial condition that needs attention; distinguish a warning from a genuine planning constraint.
3. Use Goal Planner to test goal funding, feasibility, and alternative funding paths.
4. Use Strategy Builder to assess suitable strategies and their implementation.
5. Explain the assumptions, trade-offs, and consequences to the client.
6. Treat alternatives as proposals until the client adopts one. A recalculation does not automatically change an accepted plan, goal priority, or asset allocation.

### Important planning boundaries

- Debt, a high DTI, leverage, or a negative Investment–Debt Spread does not automatically mean that debt repayment is the best strategy.
- A critical Moneywheel status is not automatically a hard block for every goal. Only an explicitly defined planning rule can impose that restriction.
- Mapping an asset to a goal does not, by itself, mean the asset is reserved, locked, or unavailable for other goals.
- Shared assets and surplus must not be counted in full for multiple goals. Resolve competing claims during whole-plan feasibility analysis.
- Recalculate affected measurements when important financial information or goal assumptions change, but do not automatically replace the client's accepted plan.

## 7. Ownership summary

| Area | Responsible feature |
|---|---|
| Financial ratios and Moneywheel measurements | Moneywheel |
| Individual goal's required return | Goal Planner |
| Goal feasibility and funding-path comparison | Goal Planner |
| Strategy, variant, technique, and implementation design | Strategy Builder |
| Decision on whether a condition is a warning, eligibility factor, or hard constraint | Canonical constraint/decision rules |
| Accepting a proposed plan or changing an accepted plan | Explicit client/planning workflow—not a Moneywheel refresh |

## 8. Scope and limitations

- Existing measurement formulas and current documented bands should not be changed without an approved review.
- The exact DTI thresholds must follow the system's canonical policy.
- Weighted Debt Rate, Investment–Debt Spread, and Portfolio-Level Return Required are specified additions; their live status must be checked before relying on them.
- No new health bands or automatic investment/debt recommendations are implied.
- Results are calculations based on the supplied data and assumptions; they are not guarantees of future outcomes.
