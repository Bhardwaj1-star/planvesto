# Budgeting

## 1. Main kaam
- Income, expenses aur available surplus ka cash-flow view dena.
- Budget limits ko actual expenses ke saath compare karna.
- Need vs Want classification dikhana.
- Monthly aur annual presentation switch dena.
- Savings target aur desired surplus ko plan karne mein madad karna.

## 2. Inputs
- Financial data se aane wali income aur expense categories.
- Har category ka actual monthly amount.
- Budget limit.
- Need/Want classification.
- Savings target settings.

## 3. Process
1. Budget data load karo.
2. Income, expenses aur surplus/deficit calculate karke dikhayo.
3. Budget vs actual variance per category compare karo.
4. Need/Want totals aur percentages dikhayo.
5. Investor budget limit/classification edit kare to save karo.
6. Data change par view refresh karo.

## 4. Output
- Total income, expenses aur surplus/deficit.
- Savings target.
- Category-wise budget, actual, variance aur status.
- Need/Want breakdown.
- Monthly ya annual display.

## 5. Important boundaries
- Budget surplus ko automatically fully investable mat samjho; emergency reserve, debt, timing aur goal needs alag assessment maang sakte hain.
- Savings target ek target hai, guaranteed result nahi.
- Budgeting khud Strategy Builder strategy select nahi karta.
- Budget values aur Goal Planner ke feasibility inputs ke beech exact synchronization verify karna hoga.

## 6. Real-Life Decision Case relationships
- **Case 1 / Opportunity Cost:** surplus ke alternative uses—debt prepayment, goal contribution, ya loan/EMI structure change—ka comparative decision Budgeting akela nahi karta. Budgeting cash-flow facts deta hai; Goal Planner/feasibility path ke consequences compare karta hai.
- **Cases 3 and 7 / Competing goals:** available surplus ek shared resource ho sakta hai. Ek goal ke liye surplus dikhna combined multi-goal feasibility prove nahi karta.
- **Cases 5, 6 and 10 / Changed financial state:** income/expense ya EMI changes relevant downstream calculations ko refresh/revalidate karne ka trigger ho sakte hain. Existing Accepted Plan ko investor decision ke bina silently replace nahi karna.
- Budget status/variance ko financial recommendation ya strategy-selection rule samajhna mana hai.

## 7. Related pages
- Expenses/income onboarding: `/investor/onboarding/expenses`
- Dashboard: `/investor/financial-state`
- Goal Planner: `/investor/goal-planner`

## 8. Code evidence
- Frontend: `frontend/app/investor/budgeting/page.tsx`
- API client: `frontend/lib/api/budgeting`
- Backend financial data/state files ko alag se trace karke exact source-of-truth verify karna baaki hai.

## 9. Abhi unverified
- Budget limit save karne aur actual transactions update hone ka relationship.
- Savings-target/desired-surplus controls ka persistence aur downstream effect.
- Annual view current month ko 12 se multiply karke present karta hai; true annual actuals ka source alag verify hona chahiye.
- Variance status thresholds ka business approval.
- Budget change se Goal Planner, Strategy Builder aur Accepted Plan tak ka exact event/revalidation behavior.


## 10. Cross-feature change and debt-analysis boundary

Budgeting provides income, expenses, surplus/deficit, budget variance and cash-flow facts. It does not itself decide Strategy Applicability, Strategy Viability, debt-prepayment priority or financing suitability. Debt/EMI changes and material income/expense changes may affect Goal Planner feasibility, Debt Reduction/Credit Utilisation analysis and an existing Accepted Plan. Identify affected downstream decisions and apply targeted revalidation where warranted.

Surplus is a shared resource, not proof that the full amount is available for one goal. Competing goals, liquidity needs, debt obligations and timing may change the result. Whole-Plan Impact Analysis is conditional on material plan-level/cross-goal consequences, not a mandatory stage for every individual-goal decision. Authoritative debt calculations, change triggers, materiality thresholds and downstream revalidation events remain unverified.


## 11. Case-specific financial inputs recorded in the source cases

### Case 1 — Retirement and debt/goal opportunity cost
The source case records: current age 35; retirement age 60; 25-year horizon; current retirement corpus ₹20 lakh; required retirement corpus ₹2 crore; monthly income ₹2,00,000; monthly expenses ₹1,20,000; existing EMI ₹10,000; approximate monthly surplus after expenses and EMI ₹70,000; emergency fund and liquidity described as adequate. The home-loan interest rate was discussed at approximately 8%. These are case facts/assumptions, not general defaults.

The surplus may be compared across alternative uses: faster debt repayment, retirement investment, or changing the loan/EMI structure and investing released cash flow. Budgeting supplies the income/expense/EMI/surplus facts; it does not decide which use is best. Investment-return assumptions in the source (including 12%, 13% or 16%) are scenarios, not guarantees.

### Case 3 — Shared surplus
The case considers Education with a ₹50 lakh target over 8 years and Retirement with a ₹3 crore target over 22 years. Surplus is a shared resource; a positive surplus or individually feasible goal does not prove that both goals are jointly feasible.

### Case 5 — Financial State change example
The case example records monthly income changing from ₹3,00,000 to ₹2,40,000 while monthly expenses are ₹1,50,000. It requires reassessing resulting surplus, individual and combined goal feasibility, existing strategy suitability, implementation and future actions rather than automatically cancelling the old strategy. The example is illustrative, not a default investor profile.

### Data boundary
These values are copied from the cited case examples. They are not default values for new investors. Materiality thresholds, calculation formulas and downstream event/revalidation behavior remain as stated in the source documents: not frozen/verified.
