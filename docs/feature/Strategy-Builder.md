# Strategy Builder

## 1. Main kaam
- Goal aur financial context ke basis par strategy run karna.
- Available strategy candidates, recommendation aur relevant architecture/scenario inspect karna.
- Strategy runs/history aur comparison/edit/scenario pages se related workflow support karna.
- Recommendation ko investor decision se alag rakhna.

## 2. Inputs
- Defined goal ya selected planning basket.
- Financial state aur goal context.
- Strategy run request.
- Strategy/scenario/architecture selection.
- Existing strategy run history.

## 3. Canonical business model
- Target decision tree mein chaar canonical strategies hain:
  - Progressive De-risking.
  - Capital Preservation.
  - Debt Reduction.
  - Credit Utilisation.
- Goal Funding fifth Strategy Builder strategy nahi; Goal Planner/feasibility layer ka hissa hai.
- Applicability (relevant hai?) aur viability (actual numbers mein kaam kar sakti hai?) alag checks hain.
- Koi acceptable strategy na ho to force karke select nahi karna.

## 4. Variants and techniques
- Target variant set aur technique mapping source decision-tree document mein listed hain.
- Technique reusable method hai; Solution investor-specific concrete path hai.
- SIP/contribution escalation ko automatically Strategy Builder strategy ya core technique nahi samajhna.
- Target business tree mein listed har variant/technique current code mein implemented hai, aisa assume nahi karna.

## 5. Opportunity Cost se relationship
- Goal Planner/feasibility mein alternative funding paths aur unka opportunity cost assess karne ka business concept documented hai.
- Strategy Builder ko Goal Planner ka feasibility/funding context consume karna chahiye; usi feasibility ko silently independently redefine nahi karna chahiye.
- Strategy Builder meaningful execution alternatives compare kar sakta hai: goal result, contribution, timing, liquidity, debt cost, risk aur competing-goal impact.
- Evidence ke bina kisi alternative ko “better” mat declare karo.
- Current runtime mein Opportunity Cost evidence explicitly pass hota hai ya calculations strategy selection ko affect karti hain, abhi verify nahi.

## 6. Process visible in UI
1. Goal/basket load aur select karo.
2. Strategy run/recommendation load ya generate karo.
3. Available strategy/architecture/scenario details inspect karo.
4. Strategy ya scenario select karke related comparison/edit/history workflows use karo.
5. Result aur trade-offs review karo.
6. Investor acceptance/active-plan update ka exact behavior verify karna baaki hai.

## 7. Output
- Strategy run/recommendation.
- Strategy candidates and relevant rationale/metrics.
- Architecture/scenario data where available.
- Strategy run history.
- Comparison/edit/scenario views via supporting routes.

## 8. Supporting routes
- Strategy comparison: `/investor/strategy-comparison`
- Strategy edit: `/investor/strategy-edit`
- Strategy history: `/investor/strategy-history`
- Strategy scenarios: `/investor/strategy-scenarios`

## 9. Decision boundary
- Goal Planner: goal feasibility/funding requirement and possible paths.
- Strategy Builder: strategy/execution approach for the relevant goal context.
- Action Plan: actions and execution status.
- History: stored versions/runs; not the same as current accepted plan.
- Investor acceptance must not be inferred merely from a generated recommendation or saved scenario.

## 10. Code evidence
- Frontend: `frontend/app/investor/strategy-builder/page.tsx`
- API: `backend/api/strategy.py`, `backend/api/strategy_edit.py`, `backend/api/strategy_version.py`
- Strategy engine: `backend/engines/strategies` and related engine modules; exact runtime order needs audit.

## 11. Abhi unverified
- Exact strategy/variant selection rules and thresholds.
- Opportunity Cost calculation/pass-through/decision impact.
- Complete technique-to-solution mapping.
- Scenario persistence, acceptance and current-plan update.
- Whether all target canonical variants and techniques are active in runtime.
- Stress/resilience and multi-goal impact rules.
