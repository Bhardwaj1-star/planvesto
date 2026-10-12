# Dashboard

## 1. Main kaam
- Investor ki current financial state ka overview dena.
- Income, expenses aur future ke liye available amount dikhana.
- Assets/liabilities aur goal progress ke relevant summaries dikhana.
- Detailed feature pages tak navigation dena.

## 2. Inputs
- Latest financial state.
- Dashboard API response.
- Goals aur goal summaries.
- Financial changes ke realtime notifications, jahan available hon.

## 3. Process
1. Dashboard data load hota hai.
2. Cash-flow aur financial summary metrics calculate/display hote hain.
3. Goal-related summaries aur visual indicators dikhte hain.
4. Financial data change hone par dashboard refresh ho sakta hai.
5. Detailed analysis ke liye investor relevant page kholta hai.

## 4. Output
- Financial overview aur cash-flow visualisation.
- Goal summaries/progress.
- Detailed financial information aur planning pages ke links.

## 5. Important boundaries
- Dashboard measurement/presentation layer hai; apne aap final financial decision-maker nahi.
- Dashboard ka ratio ya status apne aap strategy select karne ka rule nahi.
- Metric unavailable ho to use zero ya healthy status maan kar treat nahi karna.
- Dashboard data current Financial State se match karta hai ya nahi, har metric ke source ke saath verify hona chahiye.

## 6. Related pages
- Financial State/Dashboard route: `/investor/financial-state`
- Moneywheel: `/investor/moneywheel`
- Budgeting: `/investor/budgeting`
- Goal Planner: `/investor/goal-planner`

## 7. Code evidence
- Frontend: `frontend/app/investor/financial-state/page.tsx`
- API: `backend/api/dashboard.py`
- Financial state engine: `backend/engines/financial_state/engine.py`

## 8. Abhi unverified
- Har displayed metric ka exact formula and source.
- Dashboard ke har card ka refresh/freshness guarantee.
- Empty/missing data ke sab edge cases.
- Displayed summary aur decision engine ke input data ke beech consistency.
