# Financial State Architecture

**Status:** CANONICAL  
**Scope:** Canonical investor financial context consumed by planning engines.

## Purpose

Financial State is the current normalized financial context for a planning unit. It provides the common financial facts required by Goal, Constraint, Strategy, Multi-Goal and Investment workflows.

## Flow

**Financial Inputs → Financial State Service → Canonical Financial State → Derived Facts / Engines**

## Main Data

Current service/repository architecture exposes concepts including:
- annual income
- annual expenses
- investable monthly surplus
- total assets
- financial assets
- liquid assets
- total liabilities
- net worth
- essential monthly expenses
- monthly debt payments / EMI burden

## Ownership

| Layer | Responsibility |
|---|---|
| Financial State API | Request boundary |
| Financial State Service | Current-state orchestration |
| Financial State Repository | Persistence |
| Financial State Engine | Financial-state computation/normalisation |
| Calculation System | Canonical derived calculations |
| Downstream Engines | Consume facts; do not redefine source-of-truth facts |

## Consumers

Financial State is consumed by:
- Goal Planner
- Constraints
- Strategy Eligibility/Decision
- Multi-Goal Planning
- Action Plan generation
- Investment planning

## Snapshot Principle

Planning decisions should retain the financial context required to reproduce the decision. Current Financial State remains the live source for subsequent workflows; historical decision records retain their own decision snapshots where applicable.

## Code

- `backend/api/financial_state.py`
- `backend/services/financial_state_service.py`
- `backend/data/financial_state_repository.py`
- `backend/engines/financial_state/engine.py`
- `backend/engines/moneywheel/financial_state_adapter.py`
