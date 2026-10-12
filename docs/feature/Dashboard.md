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

## 6. Real-Life Decision Case relationships
- **Cases 1–2:** ratios aur summary metrics context dete hain; debt, goal funding ya credit use ka final decision sirf dashboard threshold se nahi nikalna.
- **Cases 5–6:** financial-state ya goal-intent change ke baad dashboard summary refresh aur planning revalidation alag concerns hain. Refresh hone ka matlab Accepted Plan automatically update hona nahi.
- **Cases 7–8:** single-goal status ko full multi-goal plan health samajhna nahi; shared resources aur other goals ka impact alag assess hota hai.
- **Cases 9–11:** What-If/proposal, current Accepted Plan aur execution progress ko UI mein available data ke hisaab se distinguish karna chahiye; dashboard card ko adoption ka proof nahi maana ja sakta.

## 7. Related pages
- Financial State/Dashboard route: `/investor/financial-state`
- Moneywheel: `/investor/moneywheel`
- Budgeting: `/investor/budgeting`
- Goal Planner: `/investor/goal-planner`

## 8. Code evidence
- Frontend: `frontend/app/investor/financial-state/page.tsx`
- API: `backend/api/dashboard.py`
- Financial state engine: `backend/engines/financial_state/engine.py`

## 9. Abhi unverified
- Har displayed metric ka exact formula and source.
- Dashboard ke har card ka refresh/freshness guarantee.
- Empty/missing data ke sab edge cases.
- Displayed summary aur decision engine ke input data ke beech consistency.
- Current financial-state snapshot, proposed scenario aur Accepted Plan ka explicit version/status display.
