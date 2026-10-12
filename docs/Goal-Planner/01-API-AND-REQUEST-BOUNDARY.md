# Goal Planner — API and Request Boundary

**Source revision:** `5a3b060e1b27915ede226f5173364e23dca1263e`

## 1. Router registration and prefix

- Source: [backend/api/goals.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/api/goals.py#L1-L57`)
- Router declaration: lines 6–7.
- Application registration: [backend/main.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/main.py#L1-L34`), Goal router imported at line 4 and registered at line 28.
- Prefix: `/api/goals`.
- Tag: `Goal Planner & DefinedGoal`.

## 2. Endpoints found in source

| Method | Route | Handler | Response model | Source lines |
|---|---|---|---|---|
| GET | `/api/goals?planning_unit_id=...` | `list_goals` | `list[GoalSummary]` | [18–22](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/api/goals.py#L18-L22`) |
| POST | `/api/goals/calculate` | `calculate_goal_preview` | `DefinedGoal` | [24–29](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/api/goals.py#L24-L29`) |
| POST | `/api/goals` | `save_and_define_goal` | `DefinedGoal` | [31–36](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/api/goals.py#L31-L36`) |
| GET | `/api/goals/{goal_id}/defined/latest?planning_unit_id=...` | `get_latest_defined_goal` | `DefinedGoal` | [38–43](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/api/goals.py#L38-L43`) |
| GET | `/api/goals/{goal_id}/defined/versions?planning_unit_id=...` | `get_defined_goal_versions` | `list[DefinedGoalVersionSummary]` | [45–50](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/api/goals.py#L45-L50`) |
| GET | `/api/goals/{goal_id}/defined/versions/{version}?planning_unit_id=...` | `get_defined_goal_version` | `DefinedGoal` | [52–57](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/api/goals.py#L52-L57`) |

## 3. Authentication and ownership validation

Every listed handler calls `authenticate_user(authorization)`.

- List endpoint: checks planning-unit ownership before listing.
- Preview and save endpoints: call `_validate_goal_request`.
- Defined-goal read/version endpoints: call `verify_goal_ownership(planning_unit_id, goal_id, user_id)`.

`_validate_goal_request` at lines 10–15 checks:
1. `verify_planning_unit_ownership(request.planning_unit_id, user_id)`;
2. investor ownership when `request.investor_id` is supplied;
3. ownership of every asset ID in `request.asset_mappings`.

Auth and ownership helpers are imported from `api.auth`. Their internal implementations were not included in this component document; no additional claims about their query semantics are made.

## 4. Handler behavior

### List goals — lines 17–22

Calls `GoalService().repository.list_goals(planning_unit_id)` after planning-unit ownership validation.

### Preview — lines 24–29

Validates the request and calls `GoalService().calculate_preview(request)`. The route does not call the save handler.

### Save/define — lines 31–36

Validates the request and calls `GoalService().save_and_define_goal(request)`.

### Latest snapshot and version reads — lines 38–57

The route verifies goal ownership before asking GoalService for latest snapshot, version list or a specific version.

## 5. Adjacent Goal Basket API — separate boundary

- Source: [backend/api/goal_basket.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/api/goal_basket.py#L1-L37`)
- Router prefix: `/api/goal-baskets`, tag `Goal Baskets`, lines 7–8.
- Endpoint: `POST /api/goal-baskets/preview`, lines 11–37.
- It authenticates and checks planning-unit ownership, constructs a `GoalBasket`, and calls `GoalBasketService.build_basket_summary`.
- The basket endpoint is a separate API surface; it is not part of `/api/goals` and does not create or save a DefinedGoal in the inspected handler.

## 6. Request validation handoff

Request contracts and field validators are defined in [02 — Taxonomy and data contracts](02-TAXONOMY-AND-DATA-CONTRACTS.md). The API route delegates calculation, feasibility and persistence to services; calculation formulas are documented separately.
