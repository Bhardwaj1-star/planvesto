# History

## 1. Main kaam
- Goal definitions/calculations ke purane versions dikhana.
- Strategy history ko review karne ka access dena.
- Investor ko samajhne dena ki goal ya strategy ka record time ke saath kaise badla.

## 2. Current pages
- Goal History: `/investor/goal-history`
- Strategy History: `/investor/strategy-history`
- Sidebar mein dono History section ke andar grouped hain.

## 3. Inputs
- Planning unit.
- Goal selection.
- Saved DefinedGoal versions.
- Strategy run/version history.

## 4. Process
1. Available goals load karo.
2. Investor ek goal select kare.
3. Us goal ke saved versions load karo.
4. Versions aur latest-version marker dikhayo.
5. Strategy history route par strategy runs/versions inspect kiye ja sakte hain.

## 5. Output
- Goal version history.
- Latest DefinedGoal version ka indicator.
- Strategy run/version records, relevant strategy page par.

## 6. Important boundaries
- History record dekhna aur old version restore karna alag actions hain.
- Version ka hona yeh prove nahi karta ki investor ne us version ko accept kiya tha.
- History ko current accepted plan ke saath confuse nahi karna.
- Existing version ko immutable bataya gaya hai Goal History UI mein; exact persistence/integrity guarantees backend se verify honi chahiye.

## 7. Real-Life Decision Case relationships
- **Cases 9–11:** What-If, recommendation, investor-adopted plan, and revised Accepted Plan are different states. History should not imply that a saved run/scenario was accepted unless an explicit status/link proves it.
- A changed or superseded action/plan should remain inspectable as history where supported; it should not be confused with the currently active plan.
- Completed actions remain historical records rather than being erased merely because the Accepted Plan later changes (Action Plan lifecycle rule; persistence needs verification).
- **Case 6:** a changed goal definition/calculation may create a new version; that alone does not prove downstream strategy/action plan was recalculated or accepted.

## 8. Code evidence
- Goal History: `frontend/app/investor/goal-history/page.tsx`
- Strategy History: `frontend/app/investor/strategy-history/page.tsx`
- Goal version API/repository: `backend/api/goals.py`, `backend/data/goal_repository.py`
- Strategy version API/repository: `backend/api/strategy_version.py`, `backend/data/strategy_version_repository.py`

## 9. Abhi unverified
- Old version restore/rollback behavior.
- Goal history aur strategy history ke retention rules.
- Har record ka accepted/rejected/what-if status available hai ya nahi.
- Goal version change se strategy/action plan automatically update hota hai ya nahi.
- Accepted Plan ka explicit version pointer, adoption timestamp, and relationship to strategy run/action-plan version.


## 10. Cross-feature plan and scenario lifecycle records

History should distinguish strategy runs, What-If scenarios, recommendations, investor decisions, Accepted Plan versions and Action Plan versions whenever the source data supports those distinctions. A saved version or scenario is not evidence of investor acceptance. Do not infer accepted/rejected status, adoption timestamp or active-plan pointer when the source record does not provide it.

When an Accepted Plan is revised, superseded versions and completed actions should remain historically inspectable under the final retention policy; the active plan must remain distinguishable from historical versions. A changed goal version does not by itself prove that strategy, impact analysis or Action Plan was recalculated or accepted. The authoritative plan-version link, scenario baseline, adoption timestamp, retention and rollback rules remain unverified.


## 11. Case-derived history distinctions — Cases 7–12

- **New goal scenario (Case 7):** a proposed goal and its whole-plan simulation are not the current plan. Record/label scenario status separately from adoption where source data supports it.
- **Strategy change (Case 8):** preserve the prior accepted path and its actions as history when a revised strategy is accepted; a generated recommendation or investor-proposed path alone is not adoption.
- **Execution What-If (Case 9):** increasing/reducing SIP, deploying an asset or changing debt execution creates a scenario for impact comparison; it does not by itself create an accepted plan version.
- **Strategy re-evaluation (Case 10):** an execution change may cause strategy re-evaluation, but it is not automatically a strategy replacement or a new accepted-plan version.
- **Iteration (Case 11):** retain the distinction between the accepted baseline and each experimental scenario/iteration; identify which iteration, if any, was adopted.
- **No acceptable path / investor-designed strategy (Case 12):** a rejected proposal or an investor-designed proposal remains distinct from an accepted plan. If the investor later accepts a modified path, that accepted version must be distinguishable from earlier rejected/experimental states where the underlying data supports it.
- Case 5 requires completed actions to remain historical records when Financial State changes; active/future actions may be revised after revalidation. Case 6 states that a changed goal version alone does not prove that strategy, impact analysis or Action Plan was recalculated or accepted.
- Do not invent status, adoption timestamp, active-plan pointer, version linkage, rollback behavior or retention semantics when the underlying record does not supply it.
