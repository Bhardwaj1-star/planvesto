# Action Plan

## 1. Main kaam
- Accepted strategy ko actionable tasks mein dikhana.
- Investor ko batana ki kya karna hai aur kis goal/strategy version ke liye.
- Actions ko track karna: pending, confirmed, completed, skipped.
- Action Plan execution layer hai; strategy choose karne wala engine nahi.

## 2. Inputs
- Investor/planning unit.
- Goals aur selected strategy version.
- Strategy se generated actions.
- Existing action statuses.

## 3. Process
1. Goals load karo.
2. Har goal ka selected strategy version check karo.
3. Us version ke actions load karo.
4. Goal ke hisaab se actions aur progress dikhayo.
5. Investor action complete kare to status update karo.
6. Latest status aur counts refresh karo.

## 4. Output
- Goal-wise action list.
- Selected strategy version ka reference.
- Total, completed, pending aur skipped actions.
- Action status aur progress.

## 5. Decision Tree se boundary
- Strategy Builder approach/solution banata hai.
- Investor ka accepted/selected strategy version execution ke liye reference hota hai.
- Action Plan us path ke actions track karta hai.
- Action complete hona financial outcome ya goal success ka proof nahi.

## 6. Related pages
- Strategy Builder: `/investor/strategy-builder`
- Goal Planner: `/investor/goal-planner`
- Strategy version history/edit pages exist; exact navigation/acceptance behavior separately verify hona chahiye.

## 7. Code evidence
- Frontend: `frontend/app/investor/action-plan/page.tsx`
- API: `backend/api/action_plan.py`
- Repository: `backend/data/action_plan_repository.py`
- Impact engine: `backend/engines/action_plan/impact_engine.py`

## 8. Abhi unverified
- Har strategy/solution ke liye actions ki completeness.
- Due dates, reminders aur dependencies ka exact behavior.
- Strategy change ke baad old/future actions ka final migration rule.
- Completed action undo/edit policy.
- Yeh document feature surface ka register hai; har business rule implementation mein complete hone ka proof nahi.
