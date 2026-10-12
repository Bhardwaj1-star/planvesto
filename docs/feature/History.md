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

## 7. Code evidence
- Goal History: `frontend/app/investor/goal-history/page.tsx`
- Strategy History: `frontend/app/investor/strategy-history/page.tsx`
- Goal version API/repository: `backend/api/goals.py`, `backend/data/goal_repository.py`
- Strategy version API/repository: `backend/api/strategy_version.py`, `backend/data/strategy_version_repository.py`

## 8. Abhi unverified
- Old version restore/rollback behavior.
- Goal history aur strategy history ke retention rules.
- Har record ka accepted/rejected/what-if status available hai ya nahi.
- Goal version change se strategy/action plan automatically update hota hai ya nahi.
