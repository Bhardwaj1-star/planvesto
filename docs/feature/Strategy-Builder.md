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

## 8. Relationship to Accepted Plan and Action Plan
- Generated recommendation, saved scenario, investor adoption, Accepted Plan and Action Plan are separate lifecycle states.
- Canonical target lifecycle: goal feasibility/funding context → Strategy Decision → Variant → Technique/Method → Architecture → Solution → Stress/Resilience and targeted revalidation → Recommendation → Investor Decision → Accepted Plan → Action Plan → Execution.
- A What-If scenario remains isolated from the active Accepted Plan until the investor adopts the revised path.
- Execution changes do not automatically mean the canonical strategy has changed. Re-evaluate strategy only when the changed execution materially affects applicability, viability, constraints or outcomes.
- No acceptable path is a valid outcome. An investor-designed strategy may be evaluated, but it must not be activated merely because no standard candidate passed.

## 9. Taxonomy and decision boundary
- **Strategy:** high-level financial responsibility selected for the situation.
- **Variant:** structural form of the selected strategy.
- **Technique:** reusable mechanism selected because the Strategy + Variant requires it.
- **Method/Policy:** contextual rule for applying a technique.
- **Architecture:** composed structure of selected elements and dependencies.
- **Solution:** investor-specific implementation outcome; it must not merely duplicate a Variant or Technique under another label.
- **Action:** concrete step derived from the accepted implementation.
- Goal Planner owns goal funding feasibility and funding mechanisms. Action Plan owns accepted implementation actions and their execution status. History stores past versions/runs and does not prove current adoption.

## 10. Supporting routes
- Strategy comparison: `/investor/strategy-comparison`
- Strategy edit: `/investor/strategy-edit`
- Strategy history: `/investor/strategy-history`
- Strategy scenarios: `/investor/strategy-scenarios`

## 11. Code evidence
- Frontend: `frontend/app/investor/strategy-builder/page.tsx`
- API: `backend/api/strategy.py`, `backend/api/strategy_edit.py`, `backend/api/strategy_version.py`
- Strategy engine: `backend/engines/strategies` and related engine modules; exact runtime order needs audit.

## 12. Real-Life Decision Case references
- Case 1 and 2: Goal Funding ownership and Goal Planner → Strategy Builder boundary.
- Cases 3–4: feasibility, strategy/implementation design and accepted Action Plan lifecycle.
- Cases 5–8: changed financial state, changed goal intent, new goals and multi-strategy plans.
- Cases 9–11: What-If isolation, impact analysis, targeted revalidation, investor adoption and iterative plan updates.
- Case 12: no acceptable standard path and investor-designed strategy handling.
- Case 15: Asset Mapping vs Asset Earmarking boundary.
- Canonical source: `docs/Decision tree/Real-Life Decision Cases/strategy-decision-tree.md`.

## 13. Abhi unverified
- Exact strategy/variant selection rules and thresholds.
- Opportunity Cost calculation/pass-through/decision impact.
- Complete technique-to-solution mapping.
- Whether Solution has one consistent meaning in the registry/runtime across all strategies.
- Scenario persistence, acceptance and current-plan update.
- Whether all target canonical variants and techniques are active in runtime.
- Stress/resilience, materiality and multi-goal impact rules.
- Exact point at which architecture is composed relative to strategy selection in current runtime.
