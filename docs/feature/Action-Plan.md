# Action Plan

## 1. Main kaam
- Accepted financial path ko investor ke liye concrete, executable actions mein translate karna.
- Investor ko batana ki kya karna hai, kis goal/plan ke liye, kis amount ya timing ke saath, aur actions ka sequence kya hai — jahan yeh details decision se nikalti hain.
- Actions aur execution progress ko track karna.
- Action Plan implementation layer hai; strategy choose karne ya goal feasibility ko independently dobara solve karne wala engine nahi.

## 2. Scope: Actions kahan se aa sakte hain
Action Plan sirf Strategy Builder se generated tasks ki list nahi hai. Real-Life Decision Cases ke business concept ke mutabik accepted financial path ko execute karne ke liye actions in areas se aa sakte hain:
- Goal funding aur feasibility ke liye required changes.
- Debt repayment/restructuring aur EMI/cash-flow changes.
- Multiple goals ke beech resource allocation ke accepted changes.
- Selected strategy, variant, technique aur implementation design ke execution steps.
- Investor-adopted execution/what-if change ke baad required future-action updates.

Goal Planner / multi-goal planning required financial path aur required changes identify karta hai. Strategy Builder selected path ke liye detailed strategy/execution structure design karta hai. Action Plan in accepted decisions ko actual investor actions mein translate karta hai.

## 3. Inputs
- Investor/planning unit aur current Financial State.
- Goals, goal feasibility/funding context aur relevant constraints.
- Investor-adopted decision aur Accepted Plan.
- Selected strategy/implementation structure, where applicable.
- Accepted execution parameters and required financial changes.
- Existing active actions and completed-action history.

## 4. Process
1. Current Accepted Plan aur uske adopted decisions identify karo.
2. Determine karo ki accepted path ko execute karne ke liye kya-kya change/action required hai.
3. Actions ko relevant goal/plan aur selected strategy/implementation se link karo.
4. Jahan decision define karta hai, wahan amount, timing, priority aur sequencing specify karo.
5. Current accepted path ke applicable actions ko active Action Plan mein present karo.
6. Investor ke execution progress aur decisions record karo.
7. Execution change ya material financial-state change aaye to pehle impact assess karo; zarurat ke mutabik affected decisions revalidate karo.
8. Investor revised path adopt kare tabhi Accepted Plan aur uske relevant Action Plan ko update karo.
9. Updated actions aur preserved history ke saath current progress refresh karo.

## 5. Output
- Goal-wise aur, where relevant, plan-level action list.
- Action ka purpose aur uska Accepted Plan/goal/strategy se relationship.
- Applicable amount, timing, priority aur sequencing.
- Current action status aur implementation progress.
- Accepted execution changes ke baad revised future actions.
- Completed actions ki historical record, taaki purani execution history na kho jaaye.

## 6. Accepted Plan, proposal aur What-If ka boundary
- **Accepted Plan:** Investor ka currently adopted financial path aur execution.
- **Proposal / What-If:** Alternative path ya execution choice jo abhi test ho rahi hai.
- What-if experiment existing Accepted Plan ya active Action Plan ko apne aap overwrite nahi karta.
- System pehle alternative ke financial consequences explain karta hai; investor decision ke baad hi adopted change active plan mein aata hai.
- Better-path comparison ek proposal hai, active plan nahi, jab tak investor use adopt na kare.
- Action Plan ko sirf recommended/generated strategy se seedha active nahi maana jaana chahiye; active plan investor adoption par depend karta hai.

## 7. Execution change, Impact Analysis aur revalidation
Canonical change loop:

```text
Accepted Plan
    ↓
Execution / What-If Change
    ↓
Impact Analysis
    ↓
Targeted Revalidation
    ↓
Investor Decision
    ↓
Updated Accepted Plan
    ↓
Updated Action Plan
```

- Execution change ko pehle execution change ke roop mein evaluate karo; woh apne aap strategy change nahi hota.
- System goal outcome aur relevant financial effects — jaise cash flow, liquidity, debt aur other-goal feasibility — explain kare, change ke nature ke hisaab se.
- Agar impact material ho aur existing strategy ab suitable na rahe, to strategy re-evaluation trigger ho sakta hai; strategy silently replace nahi honi chahiye.
- Whole-Plan / Multi-Goal Impact tabhi invoke karo jab decision plan-level ho ya change ka material cross-goal effect ho. Har individual-goal decision ke liye ise automatic mandatory gate mat banao.
- Revalidation targeted honi chahiye: affected goals/strategies ko dobara assess karo; unrelated strategies ko tab tak intact rakho jab tak material dependency/impact na ho.
- Exact materiality threshold, dependency model aur revalidation triggers abhi frozen nahi hain.

## 8. Action Plan ko revised Accepted Plan ke saath sync karna
Investor revised path adopt karne ke baad:
- Relevant active actions jo ab applicable nahi hain, unhe revise ya deactivate karne ka rule apply ho.
- Revised path ke liye required new actions add hon.
- Unaffected actions ko bina reason change na karo.
- Completed actions historical records bane rahein; unhe naye plan ke naam par erase na karo.
- Updated Action Plan current accepted implementation ko represent kare, saath hi prior implementation history preserve kare.

Exact old-action migration, revision/deactivation mechanics aur history model **not yet frozen** hain.

## 9. Action status aur progress
- Action Plan progress ko financial outcome ya goal success ke barabar nahi maana ja sakta.
- Action complete mark hona apne aap prove nahi karta ki expected financial result achieve ho gaya.
- Status labels aur transitions ka final product-level contract is document ke conceptual rules se alag validate hona chahiye; existing UI labels ko canonical business terminology assume na karo.

## 10. Decision Tree se boundary
- Goal Planner / Goal Feasibility: goal feasibility, funding path aur required financial changes identify karta hai.
- Strategy Builder: applicable strategy aur uska detailed execution structure design karta hai.
- Investor Decision / Accepted Plan: decide karta hai ki kaunsa proposed path active hoga.
- Action Plan: adopted path ko concrete actions mein translate karta hai, unki execution track karta hai aur accepted changes ke baad future actions update karta hai.
- Execution / What-If: alternative execution choices test karta hai aur impact explain karta hai; experiment ke dauran active plan ko silently change nahi karta.
- Action Plan neither a report-only presentation layer nor a strategy-selection engine hai.

## 11. Related pages
- Strategy Builder: `/investor/strategy-builder`
- Goal Planner: `/investor/goal-planner`
- Strategy version history/edit pages exist; exact navigation/acceptance behavior separately verify hona chahiye.

## 12. Real-Life Decision Case references
- `03-CASE_3_MULTI_GOAL_FEASIBILITY_AND_ACTION_PLAN.md` — Action Plan as actual implementation layer; goal funding, debt, cash-flow, multi-goal and strategy actions.
- `04-CASE_4_BETTER_PATH_STRATEGY_AND_IMPLEMENTATION.md` — proposal vs investor adoption; selected implementation ko concrete actions mein translate karna.
- `05-CASE_5_PLAN_ADAPTATION_AFTER_FINANCIAL_STATE_CHANGE.md` — changed Financial State ke baad plan adaptation.
- `07-CASE_7_NEW_GOAL_AGAINST_EXISTING_PLAN.md` — existing plan ke against new goal aur plan-level impact.
- `08-CASE_8_INVESTOR_STRATEGY_CHANGE_AND_MULTI_STRATEGY_PLAN.md` — investor-selected strategy change aur multi-strategy plan.
- `09-CASE_9_EXECUTION_PLAN_WHAT_IF_AND_IMPACT_GUIDANCE.md` — what-if, impact analysis aur adoption ke baad Action Plan changes.
- `10-CASE_10_EXECUTION_CHANGE_TRIGGERING_STRATEGY_REEVALUATION.md` — material execution change se strategy re-evaluation.
- `11-CASE_11_ITERATIVE_STRATEGY_EXECUTION_AND_REVALIDATION.md` — accepted plan, iterative what-if, targeted revalidation, investor adoption aur Action Plan history.
- `12-CASE_12_NO_ACCEPTABLE_PATH_AND_INVESTOR_DESIGNED_STRATEGY.md` — acceptable path na milne par investor decision; Action Plan ko unaccepted proposal ko active nahi banana chahiye.

## 13. Code evidence (feature register only)
- Frontend: `frontend/app/investor/action-plan/page.tsx`
- API: `backend/api/action_plan.py`
- Repository: `backend/data/action_plan_repository.py`
- Impact engine: `backend/engines/action_plan/impact_engine.py`

Real-Life Decision Cases se nikle business concepts ka document mein hona unke complete runtime implementation ka proof nahi hai.

## 14. Business concepts established by the cases
- Action Plan adopted financial path ki actual implementation layer hai, report-only output nahi.
- Action Plan actions multiple planning sources se aa sakte hain; Strategy Builder hi ekmatra source nahi.
- Proposed alternatives aur what-if scenarios adoption tak accepted plan se separate rehte hain.
- Execution change impact analysis aur, where materially necessary, targeted strategy/goal revalidation trigger kar sakta hai.
- Investor adoption ke baad relevant Action Plan update hota hai; completed actions history mein preserve hote hain.
- Whole-Plan / Multi-Goal Impact conditional hai; har individual-goal decision ka default mandatory stage nahi.

## 15. Abhi unverified / not yet frozen
- Har Goal Funding, debt, cash-flow, multi-goal aur strategy path ke liye action-generation completeness.
- Required action ke amount, timing, sequencing, dependencies aur deadlines ka exact rule.
- Investor adoption ko har path mein identify/record karne ka exact product contract.
- What-if scenario storage/history aur Accepted Plan se uska technical separation.
- Materiality thresholds aur targeted revalidation triggers.
- Strategy/goal change ke baad old active actions ko revise, deactivate ya replace karne ka exact migration rule.
- Unaffected goals/actions preserve karne ke exact dependency rules.
- Completed action undo/edit policy aur historical records ka final contract.
- Due dates, reminders aur dependencies ka exact behavior.
- Yeh document business-concept register hai; har concept ki complete code implementation ka claim nahi karta.


## 16. Investor Decision, plan lifecycle and targeted revalidation

### Investor Decision / Accepted Plan
A recommendation, proposal, What-If scenario, Investor Decision, Accepted Plan and Action Plan are distinct states/objects. Action Plan represents actions derived from the currently adopted path; it must not activate a proposal merely because a strategy run or report exists. Investor acceptance must be explicit. The final set of decision states (accept/reject/defer/request changes and any partial or conditional acceptance) remains to be defined and verified. “No Acceptable Strategy” must not be bypassed to create an active Action Plan for an unaccepted path.

### Materiality and targeted revalidation
A financial-state, goal-intent or execution change may affect only part of a plan. Assess materiality and dependencies before deciding which goals, strategies, solutions and actions need refresh. Whole-Plan / Multi-Goal Impact applies when the decision is plan-level or a material cross-goal effect exists; it is not mandatory for every individual-goal decision. Revalidate affected decisions after material changes, preserve unrelated valid actions, and preserve completed actions as history. Exact thresholds, stale-result rules and dependency mapping remain unverified.

### Implementation Design vs Action Plan
Strategy Builder/Implementation Design compares concrete alternatives and produces a proposed solution. Action Plan translates the adopted solution/Accepted Plan into executable steps, with timing, amounts, sequencing and status where defined. A What-If scenario remains separate from the active Action Plan until explicit adoption. A proposed solution is not proof of adoption, and Action Plan does not independently select a strategy or recalculate goal feasibility.

### Debt, cash-flow and multi-goal actions
Actions can arise from accepted debt repayment/restructuring, EMI/cash-flow changes, goal-funding adjustments, resource allocation between goals or selected strategy implementation. A calculated debt/financing option is not an accepted instruction until adopted. When a revised plan changes future actions, reconcile active actions without erasing completed-action history; exact replacement/migration semantics remain unverified.
