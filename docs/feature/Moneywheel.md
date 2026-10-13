# Moneywheel — Financial Measurements & Health Assessment

**Canonical feature decision:** Financial Health is part of Moneywheel, not a separate top-level feature. Financial State remains the source of underlying financial records.

## 1. Main kaam
- Investor ki financial position ke key ratios/signals ko ek view mein dikhana.
- Financial measurements ko interpret karke financial-health assessment ek hi Moneywheel feature ke andar dena.
- Current result ke saath available historical Moneywheel results dikhana.

## 2. Dimensions visible in code
- Cash Flow — Savings Rate.
- Liquidity — Liquid Asset Ratio.
- Debt & Solvency — Debt-to-Income Ratio, Leverage Ratio.
- Investment Structure — Financial Asset Ratio.
- Financial Protection — Insurance Coverage Ratio.
- Goal Readiness — Goal Funding Ratio, Future Funding Ratio.
- Required Return — goal fund karne ke liye required return.

## 3. Candidate debt measurements from real-life cases
The following two concepts are documented in `docs/Decision tree/Real-Life Decision Cases/00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md`. They belong to Moneywheel as measurements/diagnostics, not as automatic strategy-selection rules.

### 3.1 Weighted Debt Rate
- **Purpose:** Multiple outstanding debts ko ek principal-weighted interest-rate measurement mein summarize karna.
- **Formula:** `Sum(Outstanding Principal_i × Interest Rate_i) / Sum(Outstanding Principal_i)`.
- **Interpretation:** Each debt's interest rate is weighted by its share of total outstanding loan principal. This is not a simple average of loan rates.
- **Input requirements:** Outstanding principal and applicable interest rate for each included debt. If required inputs are missing or incomparable, show the metric as unavailable rather than inventing a value.

### 3.2 Investment–Debt Spread
- **Purpose:** Relevant investment-return assumption ko weighted debt rate ke against compare karna.
- **Formula:** `Relevant Investment Return Assumption − Weighted Debt Rate`.
- **Interpretation:** A positive spread means the assumed investment return is above the weighted debt rate; a negative spread means it is below. It is a comparison of assumptions/rates, not proof of a guaranteed or risk-adjusted profit.
- **Input requirements:** A clearly identified relevant investment-return assumption and a valid Weighted Debt Rate. If either is unavailable, the spread is unavailable.

### 3.3 Boundaries and status
- These are **candidate canonical measurements documented in decision-case material**; their implementation in code, final formula conventions, included debt types, return-assumption selection, and any status bands are not yet verified/finalized.
- Do not apply generic hard thresholds or automatically recommend Debt Reduction, investment, or another strategy from either metric alone.
- Moneywheel measures and presents evidence. Goal Planner/feasibility analysis contextualizes funding and alternatives; Strategy Builder designs an execution strategy.
- The example in the decision-case source (investment return assumption 12%, Weighted Debt Rate 9.23%, spread +2.77 percentage points) is illustrative, not a default assumption or threshold.

## 4. Inputs
- Latest Financial State.
- Goal/funding-related data.
- Moneywheel calculation request.
- Historical Moneywheel results.
- For the candidate debt measurements: per-debt outstanding principal and interest rate; and, for Investment–Debt Spread, the relevant investment-return assumption.

## 5. Process
1. Latest financial state load karo.
2. Moneywheel ratios calculate karne ke liye request bhejo.
3. Har dimension ke available ratios aur status dikhayo.
4. Unavailable inputs ko unavailable dikhana; unhe zero samajhna nahi.
5. Historical results se trend review karna.
6. Candidate debt measurements ko tabhi calculate/display karna jab required inputs and approved calculation conventions available hon; otherwise unavailable/not implemented status clearly show karna.

## 6. Output
- Ratio values, units aur availability.
- Dimension-wise status.
- Moneywheel history, jahan available ho.
- If implemented and inputs are sufficient: Weighted Debt Rate and Investment–Debt Spread, with their assumptions and units made clear.

## 7. Important boundaries
- Moneywheel measurement/diagnostic view hai, final decision-maker nahi.
- Ratio alone se Debt Reduction, Credit Utilisation ya koi strategy automatic select nahi honi chahiye.
- Opportunity Cost ka concept Moneywheel ke ratio se alag hai: alternative financial paths ke consequences compare karne ka kaam Goal Planner/feasibility analysis mein establish hua hai.
- Required return projection/assumption hai; guaranteed investment return nahi.

## 8. Real-Life Decision Case relationships
- **Cases 1–2:** DTI, leverage, liquidity and required-return measurements are evidence for analysis, not stand-alone strategy-selection rules. Debt existence or one ratio threshold does not automatically mean Debt Reduction.
- **Case 2 / Goal Funding Concept Change Log, sections 22–25:** Moneywheel measures; Goal Planner contextualizes feasibility/funding; Strategy Builder designs execution. Weighted Debt Rate and Investment–Debt Spread are proposed debt-related measurements, not independent decisions.
- **Cases 5–6:** changed financial data or goal intent can make prior metrics stale and may require recalculation. A refreshed ratio alone does not revalidate or replace the Accepted Plan.
- **Case 15:** asset mapping and asset earmarking are distinct. A mapped asset is not necessarily locked, reserved, or unavailable for other uses; Moneywheel ratios must not silently treat mapping as earmarking.
- Opportunity-cost comparison belongs to alternative-path analysis, not to a single Moneywheel ratio.

## 9. Code evidence
- Frontend: `frontend/app/investor/moneywheel/page.tsx`
- API: `backend/api/moneywheel.py`
- Engine/repository: `backend/engines/moneywheel`, `backend/data/moneywheel_repository.py`

## 10. Abhi unverified
- Har existing ratio ka exact formula, denominator aur thresholds.
- Weighted Debt Rate / Investment–Debt Spread code implementation and final calculation conventions.
- Which debts/rates are included, treatment of variable rates/fees, and selection of the relevant investment-return assumption.
- Status bands ka business approval.
- Historical snapshots ki timing/retention.
- Missing/partial inputs ke sab combinations.
- Whether metric changes trigger downstream targeted revalidation, and whether displayed results are tied to a dated Financial State snapshot.
