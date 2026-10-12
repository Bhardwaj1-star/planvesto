# Goal Planner

## 1. Main kaam
- Goal define/update karna aur required amount/timeline capture karna.
- Goal ke liye existing resources aur funding gap assess karna.
- Goal feasibility aur possible funding paths samajhna.
- Result ko Strategy Builder ke strategy/execution decision se alag rakhna.

## 2. Inputs
- Goal type, current cost/target amount, target date, priority, flexibility aur status.
- Inflation assumption aur goal-specific details.
- Goal ke saath mapped assets.
- Financial State se assets/liabilities aur related amounts.
- Existing goal/financial information.

## 3. Process
1. Investor goal create ya edit kare.
2. Goal requirement aur target date capture ho.
3. Available assets aur asset mappings review hon.
4. Goal feasibility/funding view par projected requirement aur funding gap assess ho.
5. Alternative funding paths aur unke assumptions compare karne ki zaroorat identify ho.
6. Debt, liquidity, cash flow aur competing goals par relevant impact assess ho.
7. Goal-related output Strategy Builder ke liye input ban sakta hai.

## 4. Goal Funding and feasibility
- Goal Funding, Goal Planner/feasibility domain ka hissa hai; Strategy Builder ki fifth strategy nahi.
- SIP, lump sum, step-up contribution aur combinations funding mechanisms hain; ye apne aap feasibility prove nahi karte.
- Output mein feasibility, gap, assumptions aur goal ko feasible banane ke possible changes clear hone chahiye.
- Exact formulas aur complete scenario workflow abhi verified/frozen nahi.

## 5. Opportunity Cost — documented business concept
- Case 1 mein Opportunity Cost ko alternative financial paths compare karne ka central principle banaya gaya.
- Example: extra surplus ko (a) debt prepayment, (b) goal investment, ya (c) loan/EMI structure change karke invest karne mein use karna.
- Har path ke benefits aur costs compare karo: interest saved/paid, uncertain investment outcome, future goal corpus, cash flow, liquidity, risk aur debt duration.
- Sirf debt hone se Debt Reduction automatic select mat karo.
- Sirf assumed investment return debt rate se zyada hone se investing ko automatic best mat bolo.
- **Ownership:** Goal Planner / Goal Feasibility ke alternative-path analysis ka business principle.
- **Status:** Real-Life Decision Case mein documented; current runtime mein explicit Opportunity Cost calculation/decision use hona abhi verify nahi hua.
- Source: `docs/Decision tree/Real-Life Decision Cases/00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md`, sections 5, 7, 13–16.

## 6. Multiple goals
- Har goal individually feasible ho sakta hai, par combined plan infeasible ho sakta hai.
- Shared assets/surplus aur competing funding needs ka impact check karo.
- Whole-plan analysis tab relevant hai jab multiple goals ya accepted plan materially affected ho.
- Ek individual goal change par bina reason poora plan rebuild mat karo.

## 7. Asset Mapping vs Asset Earmarking
- **Asset Mapping:** asset ko planning ke liye goal se associate karna; asset automatically locked/sold/committed nahi hota.
- **Asset Earmarking:** asset ya hissa ko jaan-boojhkar goal ke liye reserve/protect karna.
- Same asset ko multiple goals ke liye fully earmark karne ka conflict hide mat karo.
- Goal cancel hone par asset Financial State se delete nahi hota.

## 8. Goal changes and existing plans
- Amount/date/corpus change ho to affected requirement/feasibility recalculate karo.
- New goal ko pehle what-if scenario ke roop mein assess karo.
- Investor acceptance se pehle existing Accepted Plan overwrite nahi hona chahiye.
- Material financial changes par affected goals/decisions revalidate karo.
- Exact materiality thresholds aur plan-version behavior abhi unverified.

## 9. Output
- Goal requirement and timeline.
- Available/mapped resources and funding gap.
- Feasibility status or missing information.
- Alternative paths and assumptions, where supported.
- Debt/cash-flow/liquidity/other-goal trade-offs.
- Strategy Builder ko dene wala goal/funding context.
- No acceptable path ho to forced recommendation ke bajay limitation clear karna.

## 10. Related pages
- Goal Planner: `/investor/goal-planner`
- Goal feasibility detail: `/investor/goal-planner/[goalId]/feasibility`
- Goal History: `/investor/goal-history`
- Goal report: `/investor/goal-report`

## 11. Code evidence
- Frontend: `frontend/app/investor/goal-planner/page.tsx`
- Feasibility UI: `frontend/components/goals/GoalFeasibility`
- Backend goal API/engine: `backend/api/goals.py`, `backend/engines/goal/engine.py`, `funding_gap.py`, `funding_strategies.py`

## 12. Abhi unverified
- Exact feasibility and opportunity-cost formulas.
- Alternative paths ka complete generation/comparison and save/accept behavior.
- Multi-goal resource allocation rule.
- Goal cancellation par earmarking release/remapping.
- Materiality thresholds and accepted-plan update behavior.
- Is document mein business intent aur code evidence alag rakhe gaye hain; documented concept ko implemented feature nahi maana gaya.
