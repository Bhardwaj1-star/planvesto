# Action Plan & Implementation Architecture

**Status:** CANONICAL  
**Scope:** Conversion of an approved Strategy Version into executable planning actions.

## Flow

**Recommended Strategy → Strategy Version → Approval → Action Generation → Action Plan → Investor Execution**

## Gate

Actions are generated only when:
- the Strategy Version is approved;
- the version exists and belongs to the planning unit;
- finalized Goal and architecture context are present;
- the version is the current selected version for the goal;
- the referenced strategy exists in the active Strategy Library.

## Action Generation

`backend/services/strategy_action_generator.py`:
1. validates approval;
2. loads the selected Strategy Version;
3. loads primary and supporting strategies from the architecture;
4. resolves architecture techniques;
5. loads current Financial State;
6. builds deterministic action specifications;
7. prevents duplicate generation using generation keys;
8. persists ActionPlanItems.

## Action Specification

Action rules are owned by `backend/rules/action_plan.py`.

Actions contain implementation-oriented information such as:
- title
- description
- priority
- planned impact / generation key
- strategy-version context

## Data Ownership

| Data | Owner |
|---|---|
| Selected architecture | Strategy Version |
| Strategy/technique definitions | Strategy Library |
| Current financial context | Financial State |
| Action rules | Action Plan Rules |
| Persisted actions | Action Plan Repository |

## Boundary

Action Plan does not re-select the strategy. It materializes an already approved Strategy Version.

## Frontend/API

Primary integration paths:
- `backend/api/action_plan.py`
- `backend/services/action_plan_service.py`
- `backend/models/action_plan.py`
- `frontend/app/investor/action-plan/page.tsx`

## Lifecycle

**Draft Strategy → Approved Strategy Version → Generated Actions → Investor execution/tracking**

