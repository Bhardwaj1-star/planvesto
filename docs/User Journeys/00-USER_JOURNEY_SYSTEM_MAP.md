# Feature User Journey Map

**Document Type:** Feature User Journey Register  
**Status:** CANONICAL DESIGN  
**Purpose:** Keep user journeys organized by canonical product feature. Internal stages such as strategy selection, recommendation and execution belong inside the relevant feature journey or a shared cross-feature journey—not as substitutes for feature journeys.

## Canonical Feature Journeys

| Feature | Journey document | Current status |
|---|---|---|
| Onboarding | [02-ONBOARDING_JOURNEY.md](./02-ONBOARDING_JOURNEY.md) | Existing journey; needs feature-level verification |
| Financial State | [03-FINANCIAL_STATE_JOURNEY.md](./03-FINANCIAL_STATE_JOURNEY.md) | Existing journey; needs feature-level verification |
| Moneywheel | Not yet present | Journey document required |
| Goal Planner | [01-GOAL_PLANNING_JOURNEY.md](./01-GOAL_PLANNING_JOURNEY.md) | Existing journey; includes Goal Feasibility |
| Strategy Builder | [05-STRATEGY_BUILDER_JOURNEY.md](./05-STRATEGY_BUILDER_JOURNEY.md) | Consolidated feature journey |
| Budgeting | Not yet present | Journey document required |
| Financial Health | Not yet present | Journey document required |

This register records document coverage; it does not claim that a journey has been verified against runtime behavior unless that verification has been performed.

## End-to-End Product Lifecycle

```
Onboarding → Financial State → Goal Planner → Strategy Builder
→ Investor Decision / Adoption → Accepted Plan → Action Plan → Execution
```

Moneywheel, Budgeting and Financial Health remain distinct features; this lifecycle line does not merge their responsibilities into Goal Planner or Strategy Builder.

## Shared / Cross-Feature Journeys

These describe changes or plan-level situations that may affect more than one feature. They do not replace the feature journeys above.

- [14-REVALIDATION_JOURNEY.md](./14-REVALIDATION_JOURNEY.md)
- [15-GOAL_CHANGE_JOURNEY.md](./15-GOAL_CHANGE_JOURNEY.md)
- [16-FINANCIAL_STATE_CHANGE_JOURNEY.md](./16-FINANCIAL_STATE_CHANGE_JOURNEY.md)
- [17-NEW_GOAL_AGAINST_EXISTING_PLAN_JOURNEY.md](./17-NEW_GOAL_AGAINST_EXISTING_PLAN_JOURNEY.md)
- [19-MULTI_GOAL_WHOLE_PLAN_JOURNEY.md](./19-MULTI_GOAL_WHOLE_PLAN_JOURNEY.md)

## Journey Writing Rule

A feature User Journey must explain:
- What the investor does.
- What the system does.
- What the investor sees.
- What decision or next step the investor can take.
- What information enters the feature and what output it passes onward.

Use the feature's existing documentation and code-backed behavior as evidence. Mark gaps as unknown; do not invent steps, rules or functionality.
