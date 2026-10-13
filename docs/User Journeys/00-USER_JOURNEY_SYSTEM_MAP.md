# Feature User Journey Map

**Document Type:** Feature User Journey Register  
**Status:** CANONICAL DESIGN  
**Purpose:** Index only those feature journeys whose corresponding implementation specification exists in `docs/implementations/`.

## Implementation-Backed Feature Journeys

| Feature | Implementation document | User Journey | Boundary |
|---|---|---|---|
| Goal Planner | [Goal-Planner.md](../implementations/Goal-Planner.md) | [01-GOAL_PLANNING_JOURNEY.md](./01-GOAL_PLANNING_JOURNEY.md) | Goal requirements, funding paths and Goal Feasibility |
| Moneywheel | [Moneywheel.md](../implementations/Moneywheel.md) | [04-MONEYWHEEL_JOURNEY.md](./04-MONEYWHEEL_JOURNEY.md) | Financial measurements and traceable evidence for downstream planning |
| Strategy Builder | [Strategy-Builder.md](../implementations/Strategy-Builder.md) | [05-STRATEGY_BUILDER_JOURNEY.md](./05-STRATEGY_BUILDER_JOURNEY.md) | Strategy selection and strategy-side implementation proposal |
| Action Plan | [Action-Plan.md](../implementations/Action-Plan.md) | [12-ACTION_PLAN_JOURNEY.md](./12-ACTION_PLAN_JOURNEY.md) | Actions derived from an Accepted Plan, execution and impact review |

Only journeys listed above are retained in this folder because each has a matching implementation specification. This does not mean every described capability is already implemented in runtime; each journey must preserve the implementation document's distinction between current behavior and required/target behavior.

## End-to-End Handoff

```
Financial State / Goal Context
          ↓
Goal Planner + Goal Feasibility
          ↓
Moneywheel Evidence (where relevant)
          ↓
Strategy Builder
          ↓
Investor Decision / Adoption
          ↓
Accepted Plan
          ↓
Action Plan → Execution
```

The diagram shows responsibilities and handoffs, not a mandatory sequence in which Moneywheel must always run after Goal Planner. Goal Planner owns goal-level requirements and feasibility; Moneywheel owns its measurements; Strategy Builder consumes planning evidence; Action Plan follows explicit investor adoption.

## Journey Writing Rule

Each retained journey must state:
- What the investor does.
- What the system does and what it presents.
- What inputs it relies on and what outputs it passes onward.
- What the investor can decide or do next.
- Which behaviors are current, planned, unknown or not yet verified.

Use the matching implementation specification as the governing reference. Do not invent steps, rules, calculations or runtime capabilities.
