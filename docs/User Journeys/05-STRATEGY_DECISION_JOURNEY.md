# Strategy Decision Journey

**Document Type:** User Journey  
**Status:** CANONICAL DESIGN

## Entry Point

Goal Feasibility is handled in [04-GOAL_FEASIBILITY_JOURNEY.md](04-GOAL_FEASIBILITY_JOURNEY.md). Strategy Decision receives the reviewed goal-feasibility/funding evidence; it does not repeat the Goal Planner's feasibility calculation.

## Journey

```
Reviewed Goal Feasibility + Financial State + Applicable Constraints
→ Constraint / Safety Evaluation
→ Strategy Applicability
→ Candidate Viability
→ Strategy Selection
   ├─ Acceptable strategy found → Selected Strategy
   └─ No acceptable strategy → Explain why no path qualifies
→ Implementation Design Journey
```

## System Does

- Uses the goal and financial evidence supplied by the upstream journeys.
- Evaluates applicable constraints and safety conditions.
- Checks which of the four canonical strategies apply to the situation.
- Checks whether applicable candidates can work under the actual financial conditions.
- Selects a strategy only from candidates that pass the relevant checks.
- Preserves **No Acceptable Strategy** as a valid result; it does not force a strategy to produce an answer.

## Investor Experience

- Sees the strategy outcome and the reasons it fits the financial situation.
- Can understand relevant constraints, trade-offs, and why a candidate was not selected.
- If no acceptable strategy is found, sees that result rather than a forced recommendation.

## Strategy Choices

- Progressive De-risking
- Capital Preservation
- Debt Reduction
- Credit Utilisation
- No acceptable Strategy, where applicable

## Handoff

```
Selected Strategy → Implementation Design Journey
```

Variant selection, technique and method/policy composition, architecture/solution design, stress/resilience, recommendation, and investor adoption are covered by their separate User Journey documents. Strategy Decision does not repeat those journeys.

## Core Rule

The system must not jump directly from goal type or time horizon to a Strategy. It must use the reviewed evidence and applicable constraints, distinguish applicability from viability, and allow **No acceptable Strategy** when no candidate qualifies.
