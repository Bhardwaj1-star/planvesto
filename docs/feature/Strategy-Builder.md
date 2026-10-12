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


## 14. Cross-feature concepts within Strategy Builder

### Implementation Design
Strategy Builder owns the strategy-side design from selected Strategy/Variant through Technique, Method/Policy, Architecture and a concrete Solution proposal. The proposal may compare resource use, contributions, timing, liquidity, debt effects and competing-goal consequences where relevant data exists. A Technique is not a Solution, and a Solution proposal is not an Action Plan. Active plan state changes only after explicit investor adoption.

### What-If / Scenario
A What-If scenario is an alternative evaluated against a known baseline. It must remain separate from the active Accepted Plan while being explored. Record baseline, changed inputs/assumptions, projected outcomes and validation status where supported. A saved scenario or report does not prove investor acceptance. The existing scenario route does not by itself prove runtime isolation or persistence.

### Constraint / Safety Evaluation
Constraints define the allowed/restricted decision space before strategy evaluation. Distinguish hard constraints from preferences, blockers from warnings, and failed checks from insufficient inputs. Applicability asks whether a strategy fits; viability asks whether it can work under actual conditions. Exact runtime gates remain to be audited.

### Stress / Resilience Evaluation
The canonical decision tree includes Stress / Resilience before final decision output. It tests whether the proposed path remains acceptable under defined adverse/changed assumptions, including relevant funding, liquidity, debt/EMI and goal-timing effects. It is distinct from applicability, viability and impact analysis. Stress cases, thresholds, warnings versus hard failures, and missing-input behavior remain unverified.

### Investor-designed strategy path
If all standard strategies fail, “No Acceptable Strategy” remains valid; do not force a standard recommendation. Where policy permits, an investor-designed path can be captured as a separate proposal and evaluated against constraints, feasibility, impact and resilience. It is not automatically safe, viable or accepted, and must not be relabelled as one of the four canonical strategies. It becomes active only through the explicit Investor Decision / Accepted Plan lifecycle.

### Technique policy and hierarchy
Technique policy statuses are **Required**, **Conditional**, **Optional**, **Not Applicable** and **Insufficient Inputs**; the last two are not equivalent. Preserve **Strategy → Variant → Technique → Method/Policy → Architecture → Solution → Action**. Goal Funding and Contribution Escalation remain Goal Planner responsibilities; Duration/Horizon Matching is a method, not a separate core technique.

### Impact analysis and debt economics
Whole-Plan / Multi-Goal Impact is conditional when a new goal, existing Accepted Plan, shared-resource conflict or material cross-goal effect makes it relevant; it is not a mandatory gate for every individual-goal strategy decision. Material changes may require targeted revalidation of affected decisions. Debt Reduction/Credit Utilisation analysis may require effective debt cost, repayment terms, EMI capacity, borrowing capacity, financing cost and a credible repayment path. Calculation ownership, materiality thresholds and invalidation rules remain unverified.

Canonical lifecycle: Goal Planner feasibility/funding → Strategy/Variant/Technique/Method → Architecture/Solution proposal → relevant impact and resilience checks → recommendation → explicit Investor Decision → Accepted Plan → Action Plan → execution. This is a business contract, not proof of runtime implementation.
