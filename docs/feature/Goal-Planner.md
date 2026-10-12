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
- Mapping is upstream feasibility evidence; earmarking is a separate commitment/protection concept and must not be treated as a synonym.

## 8. Goal changes and existing plans
- Amount/date/corpus change ho to affected requirement/feasibility recalculate karo.
- New goal ko pehle what-if scenario ke roop mein assess karo.
- Investor acceptance se pehle existing Accepted Plan overwrite nahi hona chahiye.
- Material financial changes par affected goals/decisions revalidate karo.
- Exact materiality thresholds aur plan-version behavior abhi unverified.
- No acceptable path ek valid outcome hai; investor ko constraints aur trade-offs explain karo, aur unaccepted proposal ko active plan mat banao.

## 9. Relationship to Strategy Builder and Action Plan
- Goal Planner answers **what is feasible / what funding conditions are required**; Strategy Builder designs **how to implement the feasible path**.
- Strategy Builder ko Goal Planner ka feasibility/funding context consume karna chahiye, bina us feasibility ko silently independently redefine kiye.
- A changed contribution/funding mechanism is not automatically a change to one of the four canonical Strategy Builder strategies.
- Selected strategy/implementation becomes an Accepted Plan only after investor decision; Action Plan is generated/synchronized downstream from that accepted plan.

## 10. Output
- Goal requirement and timeline.
- Available/mapped resources and funding gap.
- Feasibility status or missing information.
- Alternative paths and assumptions, where supported.
- Debt/cash-flow/liquidity/other-goal trade-offs.
- Strategy Builder ko dene wala goal/funding context.
- No acceptable path ho to forced recommendation ke bajay limitation clear karna.

## 11. Related pages
- Goal Planner: `/investor/goal-planner`
- Goal feasibility detail: `/investor/goal-planner/[goalId]/feasibility`
- Goal History: `/investor/goal-history`
- Goal report: `/investor/goal-report`

## 12. Code evidence
- Frontend: `frontend/app/investor/goal-planner/page.tsx`
- Feasibility UI: `frontend/components/goals/GoalFeasibility`
- Backend goal API/engine: `backend/api/goals.py`, `backend/engines/goal/engine.py`, `funding_gap.py`, `funding_strategies.py`

## 13. Abhi unverified
- Exact feasibility and opportunity-cost formulas.
- Alternative paths ka complete generation/comparison and save/accept behavior.
- Multi-goal resource allocation rule.
- Goal cancellation par earmarking release/remapping.
- Materiality thresholds and accepted-plan update behavior.
- Is document mein business intent aur code evidence alag rakhe gaye hain; documented concept ko implemented feature nahi maana gaya.


## 14. Cross-feature concept boundaries

### Funding feasibility and debt economics
Goal Planner owns goal-level funding requirements, funding-gap evidence and feasibility; it is not a fifth Strategy Builder strategy. Debt inputs that can affect feasibility include effective debt cost, EMI/payment burden, prepayment terms, repayment capacity, borrowing capacity and financing-cost comparison. Debt or a funding gap alone does not prove that Debt Reduction or Credit Utilisation is suitable. Shared calculation ownership across Goal Planner, Budgeting and Strategy Builder remains unverified.

### Local impact vs Whole-Plan Impact
Goal Planner assesses the affected goal's requirement, available resources, funding gap and feasibility. When a new/changed goal competes for shared resources or materially affects an Accepted Plan, Whole-Plan / Multi-Goal Impact Analysis is also needed. It is conditional, not mandatory for every individual-goal decision. Identify affected goals, resource conflicts, trade-offs and decisions requiring targeted revalidation; do not rebuild unrelated decisions without a material dependency. Materiality thresholds and dependency rules remain unfrozen.

### Asset Mapping vs Asset Earmarking
**Asset Mapping** associates a resource with a goal for planning/feasibility; it does not mean the resource is committed, protected, sold or sufficient. **Asset Earmarking** is a separate strategic/implementation choice to reserve or protect a resource for a goal/capital pool. Do not use the terms as synonyms. Mapping the same resource to multiple goals can reveal a conflict; do not silently count it as fully available to each. Cancelling a goal does not delete the underlying asset from Financial State; earmark release/remapping needs a defined lifecycle.

### Opportunity Cost and alternative paths
Compare funding alternatives using explicit assumptions: contributions, debt prepayment, loan/EMI changes, timing, liquidity and competing-goal effects. Do not call an alternative better merely because debt exists or an assumed investment return exceeds a debt rate. A proposed alternative/What-If result is not an Accepted Plan until investor adoption. Runtime calculations and acceptance workflow remain unverified.

Budgeting supplies cash-flow facts; Strategy Builder designs a strategy-side implementation; Impact Analysis evaluates cross-goal consequences where material; Action Plan converts an accepted path into actions.


## 15. Source-derived case details — goal funding and multi-goal feasibility

### Case 1–2: goal funding boundary
- Goal Funding/Goal Feasibility belongs to Goal Planner, not to the Strategy Builder strategy set.
- Goal Planner determines whether a goal can be made feasible, identifies the funding gap, compares alternative financial scenarios and produces feasibility/funding paths.
- SIP, lump sum, step-up SIP and combinations of assets/contributions are funding mechanisms/options; they are not by themselves proof of feasibility or independent Strategy Builder strategies.
- Strategy Builder consumes the feasibility/funding result and designs execution. It does not independently recreate Goal Planner feasibility.
- Debt existence, DTI or another isolated metric does not by itself determine Debt Reduction. The Case 1 alternatives include faster debt repayment, retirement investment and changing loan structure/EMI then investing released cash flow. Each path has different interest, corpus, cash-flow, liquidity, risk and debt-duration consequences.
- The Case 1 example uses a retirement goal with age 35 now, retirement age 60, ₹20 lakh current corpus, ₹2 crore target corpus, ₹2,00,000 monthly income, ₹1,20,000 expenses, ₹10,000 EMI, approximately ₹70,000 surplus, adequate emergency fund/liquidity, and a home-loan rate discussed at approximately 8%. Return rates such as 12%, 13% or 16% are scenario assumptions, not guaranteed outcomes.

### Case 3: multi-goal feasibility
- The case includes Education at ₹50 lakh over 8 years and Retirement at ₹3 crore over 22 years.
- Individual-goal feasibility does not establish combined-plan feasibility where goals compete for shared surplus/assets.
- Goal Planner / Goal Feasibility identifies what must change for goals to become feasible, including relevant funding gaps, debt/cash-flow constraints, shared resources and alternative paths.
- Possible accepted actions recorded in Case 3 include prepaying/closing high-cost debt, increasing a specified monthly contribution, deploying a required lump sum, reallocating contributions between goals, restructuring a loan and redirecting released cash flow, using a financing path to preserve existing assets, executing strategy-specific actions, and sequencing multiple actions with timing/amount.
- Whole-Plan / Multi-Goal Impact is conditional on a plan-level decision or material cross-goal effect; it is not an automatic mandatory stage for every individual-goal decision.

### Case 4: already-feasible goal and alternative implementation
- Strategy Builder may compare the current/appropriate path with a better-path alternative even when a goal is already feasible.
- The case comparison includes initial asset, return assumption, goal target, estimated goal date, difference in years, required contribution, liquidity, risk and other-goal impact.
- The case's illustrative comparison uses ₹20 lakh initial asset, a 6% return assumption on the current path and a 10% assumption on the alternative path for a ₹50 lakh goal. These are case assumptions, not guaranteed returns.
- The investor can inspect what happens if the selected strategy is actually implemented using their own financial numbers. A proposed better path is not adopted merely because it is generated.

### Case 6: goal intent change and cancellation
- Recalculate affected funding requirement and feasibility when target amount, timeline, target date, existing goal corpus, funding assumptions or other relevant goal inputs change.
- A goal change does not automatically invalidate the whole plan or existing strategy; recalculate first, then update only affected decisions as required.
- Cancelling a goal removes that goal's funding requirement, not the underlying assets. Identify assets mapped to the cancelled goal, retain them in Financial State, determine their destination, remap to remaining goals where applicable, and recalculate affected feasibility.
- Case 6 records the directional relationships: higher target generally increases funding need; longer timeline generally lowers periodic contribution need all else equal; earlier target date generally increases funding intensity; larger existing corpus generally lowers future funding need. Actual outcomes must be recalculated from complete inputs.

### Case 7: new goal against existing plan
- Treat a proposed new goal initially as a separate scenario against the existing financial plan, not as an automatically adopted goal.
- Show incremental impact on the existing plan, including trade-offs and affected goals/resources. Investor decision precedes plan adoption.
- Case 7 distinguishes goal/strategy implementation for a particular goal from whole-plan impact simulation after adding a goal or changing the financial situation.
- If rejected, the existing Accepted Plan remains; if accepted, the plan and related actions are updated through the adoption workflow.

## 16. Asset Mapping and Asset Earmarking — Case 15

- **Asset Mapping** answers which existing resources are associated with a goal for planning/feasibility. It is a planning association and can exist before strategy selection.
- **Asset Earmarking** answers which resources are intentionally reserved/protected for a goal as part of a selected strategy/technique/implementation. It is a strategic allocation/protection decision.
- A mapped asset is not automatically locked, sold, committed, protected or unavailable for other uses. Mapping is not proof of feasibility or a product recommendation.
- The same asset may be mapped to multiple goals for planning consideration; the system must not silently count it as fully available to each goal. Earmarking creates an intentional commitment and competing earmarks require conflict handling.
- Earmarking usually requires strategy/implementation context; mapping belongs to Goal Planner. The projected contribution of mapped resources belongs to goal planning/asset projection; funding gap belongs to Goal Funding/feasibility; earmarking amount belongs to strategy/method/policy; concrete execution belongs to Architecture/Solution/Action; accepted action depends on Investor Decision/Accepted Plan.
- Cancelling a goal does not delete the underlying asset. Goal-linked mapping and any earmark must be treated as distinct relationships; exact release/remapping lifecycle is not frozen.
- Case 15 is marked **canonical business decision document — not yet implemented in code**.

## 17. Source status and unresolved definitions
- Case 1–2 states that exact Goal Funding rules and the final roles of existing funding variants are not frozen.
- Case 3–4 states that optimization/comparison rules remain unfrozen.
- Case 5 leaves materiality thresholds, adaptation algorithm and action-plan versioning rules to be validated.
- Case 6 leaves exact feasibility formulas, goal-input dependency rules, asset reassignment and strategy-update mechanics to validation.
- Case 15 is not yet implemented in code.
- These source statuses are retained as recorded; this feature document does not declare implementation or business rules finalized.
