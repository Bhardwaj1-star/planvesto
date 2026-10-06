# Retirement Goal Save Error

## Issue

Retirement goal save is failing with HTTP 500 because the retirement calculation requires `currentAge` and `lifeExpectancy` inside `dynamic_details`.

Error:

```
Retirement planning requires currentAge and lifeExpectancy in dynamic_details
```

## Current Code Flow

The failure occurs in both goal calculation and goal save:

```
POST /api/goals/calculate
    -> GoalService.calculate_preview()
    -> GoalEngine.calculate_defined_goal()

POST /api/goals
    -> GoalService.save_and_define_goal()
    -> GoalEngine.calculate_defined_goal()
```

Both service methods call `_enrich_retirement_context()`, but the current implementation is a no-op.

## Root Cause

### Backend

`backend/engines/goal/engine.py` reads:

- `currentAge` (also accepts `current_age`)
- `lifeExpectancy` (also accepts `life_expectancy`)

For retirement, the engine raises an error when the required age context is missing.

The retirement tests in the repository also pass both values explicitly, for example:

```python
dynamic_details={
    "currentAge": 30,
    "lifeExpectancy": 85,
}
```

### Frontend

`frontend/app/investor/goal-planner/page.tsx` builds the API payload from `dynamic_details`.

The retirement form sends `lifeExpectancy` and retirement expense/passive-income fields, but does not add `currentAge`.

The frontend goal type definitions in `frontend/lib/onboarding/goals/types.ts` also do not define `currentAge` in `GoalDynamicDetails`.

### Existing Investor Data

The repository already persists the investor's date of birth:

```
investors.date_of_birth
```

This is saved by `frontend/lib/onboarding/persistence.ts`.

## Impact

A retirement goal can reach the backend without the age context required by the calculation engine. As a result:

1. Retirement calculation fails.
2. Preview can return HTTP 500.
3. Saving the goal also fails because save invokes the same calculation path.

## Recommended Fix

The preferred fix is to populate retirement age context server-side before calling the goal engine.

The existing `GoalService._enrich_retirement_context()` is the intended central hook because both:

- `calculate_preview()`
- `save_and_define_goal()`

already call it.

For retirement goals, this enrichment should:

1. Resolve the investor associated with the planning unit.
2. Read the persisted `date_of_birth`.
3. Calculate the investor's current age.
4. Add `currentAge` to `dynamic_details`.
5. Preserve the existing `lifeExpectancy` value supplied by the goal form.
6. Then pass the enriched request to `GoalEngine.calculate_defined_goal()`.

This keeps the age calculation authoritative on the backend and fixes both preview and save through the same path.

## Files Involved

- `backend/engines/goal/engine.py`
- `backend/services/goal_service.py`
- `backend/schemas/goals.py`
- `backend/api/goals.py`
- `frontend/app/investor/goal-planner/page.tsx`
- `frontend/lib/onboarding/goals/types.ts`
- `frontend/lib/onboarding/persistence.ts`
- `frontend/supabase/migrations/001_initial_schema.sql`
- `backend/tests/test_goal_calculations.py`
- `backend/tests/test_goal_engine_build.py`

## Verification

After the fix, verify both endpoints for a retirement goal:

- `POST /api/goals/calculate`
- `POST /api/goals`

The retirement request should reach the engine with both:

```json
{
  "currentAge": 30,
  "lifeExpectancy": 85
}
```

and should no longer raise the missing retirement age-context error.

> This document is based on the repository code and the reported runtime error. No documentation outside the repository was used.
