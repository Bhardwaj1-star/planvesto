# History — Surfaces and Data Families

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## Goal History

UI: `frontend/app/investor/goal-history/page.tsx`. It loads goal data and lets the investor select a goal, then displays saved DefinedGoal versions through goal-history APIs. The page describes versions as immutable and latest version as explicitly marked by the backend; actual persistence behavior must be read from GoalRepository and its service, not inferred from the UI description alone.

Relevant sources: `backend/api/goals.py`, `backend/data/goal_repository.py`, `backend/services/goal_service.py`, Goal Planner docs `06-PERSISTENCE-AND-VERSIONING.md`.

## Strategy History

UI: `frontend/app/investor/strategy-history/page.tsx`. It loads goals, reads optional `goalId` from the URL, requests strategy run history and the selected Strategy Version, then loads version history for the selected strategy. The first returned run is assigned as the displayed run; correctness therefore depends on the API's ordering contract.

Relevant sources: `backend/api/strategy.py`, `backend/api/strategy_version.py`, `backend/data/strategy_repository.py`, `backend/data/strategy_version_repository.py`.

## Other persisted history-like families

- Financial State snapshots through `backend/api/financial_state.py` and snapshot repository.
- Moneywheel snapshots through `backend/api/moneywheel.py` and `backend/data/moneywheel_repository.py`.
- Action Plan decisions through `backend/api/action_plan.py` and `backend/data/action_plan_repository.py`.
- Diary financial decision records through `backend/api/diary.py` and `backend/data/diary_repository.py`.

These are adjacent history sources, not proof of a unified History module.
