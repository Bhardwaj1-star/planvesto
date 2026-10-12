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
