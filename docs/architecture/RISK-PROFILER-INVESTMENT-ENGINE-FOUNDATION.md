# Risk Profiler → Investment Engine Foundation

## Locked Boundary

The system separates risk assessment from investment implementation.

### Risk Profiler

Answers: what investment risk boundary is appropriate for this investor?

It combines three distinct dimensions:

1. Risk Required — financially required return/risk to meet objectives.
2. Risk Capacity — financial ability to absorb investment losses/volatility.
3. Risk Tolerance — behavioural willingness to tolerate investment risk.

These remain separately represented.

### Canonical ownership

Risk Required is not owned by Risk Profiler. It is already owned by the
canonical financial-calculation layer and is consumed by both MoneyWheel and
Risk Profiler.

Therefore:

Canonical Risk Required + Risk Capacity + Risk Tolerance → Risk Profile

Risk Profiler owns the assessment/combination, not duplicate calculation of
Risk Required.

## Investment Engine Boundary

The Investment Engine answers: how should approved investment risk be
implemented in the portfolio?

Implementation hierarchy:

Strategic Asset Allocation → Sub-Asset Allocation → Product Category
→ Product Selection → Allocation Amount

The Investment Engine consumes the Risk Profile / approved risk boundary. It
does not independently recalculate Risk Required or reinterpret raw Risk
Tolerance.

## Data vs Decision Separation

| Component | Owns | Does not own |
|---|---|---|
| Canonical Calculation | Risk Required and shared financial facts | Risk decisions |
| Risk Profiler | Capacity, Tolerance, combined Risk Profile | Product selection |
| Investment Engine | Portfolio allocation/implementation | Behavioural risk assessment |
| Product Selection | Actual products within approved constraints | Risk-profile creation |
| Strategy Builder | Goal/problem-solving strategy architecture | Generic portfolio construction |

## Current Foundation

A dedicated backend/engines/investment/ boundary now contains:

- models.py — input/output and allocation-layer contracts
- engine.py — orchestration foundation
- __init__.py — public exports

The engine validates whether all three Risk Profile dimensions are available
and creates the implementation-layer structure.

It intentionally does not define:

- risk-score thresholds
- asset-allocation percentages
- equity/debt/cash mappings
- product-category mappings
- product-selection rules
- rebalance rules

Those require explicit business decisions.

## End-to-End Architecture

Raw Financial Data
→ Canonical Financial Facts
→ Risk Profiler
→ Risk Profile / Risk Boundary
→ Investment Engine
→ Target Portfolio
→ Product Selection
→ Implementation

In parallel:

Canonical Financial Facts → MoneyWheel

Goals + Financial Context → Goal Engine / Strategy Builder

## Critical Design Rules

Risk Required ≠ Risk Capacity ≠ Risk Tolerance.

They participate in one Risk Profile decision, but their provenance,
calculation/assessment method, and downstream meaning remain distinct.

Risk Profile ≠ Investment Portfolio.

Risk Profile defines the boundary; Investment Engine defines implementation
within that boundary.

## Business Rules Still Required

Before actual allocation decisions are implemented, explicitly define:

1. Risk Required representation across multiple goals.
2. Risk Capacity assessment model and constraints.
3. Risk Tolerance assessment model.
4. How the three dimensions combine into an approved risk boundary.
5. Strategic Asset Allocation policy.
6. Sub-asset allocation policy.
7. Product-category eligibility rules.
8. Product-selection rules.
9. Current-vs-target allocation-gap methodology.
10. Allocation amount and rebalancing rules.

Until these are explicitly defined, the Investment Engine should return
requires_review rather than inventing an allocation.
