# Multi-Goal Planning Architecture

**Status:** CANONICAL  
**Scope:** Coordinating multiple defined goals into one planning-unit-level plan.

## Purpose

Multi-Goal Planning operates above individual Goal and Strategy runs. It resolves competing goals against shared financial capacity and priorities.

## Flow

**Multiple Defined Goals → Per-Goal Reports/Strategies → Financial Context → Multi-Goal Evaluation → Conflict/Allocation Resolution → Multi-Goal Plan**

## Per-Goal Inputs

For each goal the service consumes:
- goal identity/type
- client priority
- target date
- today cost
- future target
- funding gap
- required monthly contribution
- feasibility
- selected Strategy Version
- recommended strategy
- strategy funding solution evidence

## Shared Context

The service consumes the canonical current Financial State and derives normalized planning fields such as:
- income
- expenses
- monthly surplus
- assets
- liabilities
- net worth
- liquid assets
- essential expenses
- EMI burden

## Conflict Boundary

Multi-Goal Planning does not replace individual Strategy Decision. Each goal must have a selected current Strategy Version before the current multi-goal plan can be built.

The multi-goal layer then evaluates goals together, including priority and shared-resource constraints.

## Code

- `backend/services/multi_goal_planning_service.py`
- `backend/engines/orchestration/engine.py`
- `backend/rules/multi_goal.py`
- `backend/schemas/multi_goal_planning.py`
- `backend/api/orchestration.py`

## Architectural Position

**Goal Planner** answers each goal's funding requirement.  
**Strategy Engine** answers each goal's strategy.  
**Multi-Goal Planning** answers how multiple goals coexist under shared resources.

