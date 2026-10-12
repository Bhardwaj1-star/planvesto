# Moneywheel

## 1. Main kaam
- Investor ki financial position ke key ratios/signals ko ek view mein dikhana.
- Financial health ke alag dimensions ko review karne mein madad dena.
- Current result ke saath available historical Moneywheel results dikhana.

## 2. Dimensions visible in code
- Cash Flow — Savings Rate.
- Liquidity — Liquid Asset Ratio.
- Debt & Solvency — Debt-to-Income Ratio, Leverage Ratio.
- Investment Structure — Financial Asset Ratio.
- Financial Protection — Insurance Coverage Ratio.
- Goal Readiness — Goal Funding Ratio, Future Funding Ratio.
- Required Return — goal fund karne ke liye required return.

## 3. Inputs
- Latest Financial State.
- Goal/funding-related data.
- Moneywheel calculation request.
- Historical Moneywheel results.

## 4. Process
1. Latest financial state load karo.
2. Moneywheel ratios calculate karne ke liye request bhejo.
3. Har dimension ke available ratios aur status dikhayo.
4. Unavailable inputs ko unavailable dikhana; unhe zero samajhna nahi.
5. Historical results se trend review karna.

## 5. Output
- Ratio values, units aur availability.
- Dimension-wise status.
- Moneywheel history, jahan available ho.

## 6. Important boundaries
- Moneywheel measurement/diagnostic view hai, final decision-maker nahi.
- Ratio alone se Debt Reduction, Credit Utilisation ya koi strategy automatic select nahi honi chahiye.
- Opportunity Cost ka concept Moneywheel ke ratio se alag hai: alternative financial paths ke consequences compare karne ka kaam Goal Planner/feasibility analysis mein establish hua hai.
- Required return projection/assumption hai; guaranteed investment return nahi.

## 7. Code evidence
- Frontend: `frontend/app/investor/moneywheel/page.tsx`
- API: `backend/api/moneywheel.py`
- Engine/repository: `backend/engines/moneywheel`, `backend/data/moneywheel_repository.py`

## 8. Abhi unverified
- Har ratio ka exact formula, denominator aur thresholds.
- Status bands ka business approval.
- Historical snapshots ki timing/retention.
- Missing/partial inputs ke sab combinations.
