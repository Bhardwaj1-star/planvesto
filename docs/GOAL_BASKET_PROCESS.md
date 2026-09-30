# Goal Basket — Process & Implementation

## 1. Purpose

A **Goal Basket** is a logical grouping of multiple client goals that should be viewed and planned together.

Example:

- Family Security Basket
  - Emergency Fund
  - Child Education
  - Insurance Reserve

The basket is a planning-level grouping. It does not replace individual goals.

## 2. Current Goal Architecture

Planvesto currently calculates and evaluates goals individually through the DefinedGoal layer. A DefinedGoal contains the calculated target, time horizon, priority, flexibility, funding status, funding gap and required monthly contribution.

The Strategy Builder can then evaluate a goal against available strategies and eligibility rules.

## 3. Goal Basket Concept

The basket sits **above individual goals**:

```text
Investor
  ↓
Planning Unit
  ↓
Goal Basket(s)
  ↓
Individual Goals
  ↓
Defined Goals
  ↓
Strategy / Eligibility
  ↓
Multi-Goal Orchestration
  ↓
Resource Allocation
  ↓
Financial Plan
```

A goal may belong to a basket while retaining its own goal identity, target, timeline, priority and strategy.

## 4. What a Basket Represents

A basket should represent a client's planning intent, not merely a UI folder.

It can provide:

- A name and description
- A set of member goals
- Basket-level planning context
- Aggregated target/funding information
- A basis for collective resource planning
- A way to reason about trade-offs among related goals

## 5. What a Basket Does NOT Do

A basket must not:

- Merge individual goals into one goal
- Destroy individual goal calculations
- Automatically change goal priorities
- Automatically select investment products
- Replace the Strategy Builder
- Override eligibility rules

Individual goals remain independently calculable and auditable.

## 6. Example

Suppose a client has:

| Goal | Target | Timeline | Priority |
|---|---:|---:|---|
| Emergency Fund | ₹3L | 1 year | Critical |
| Child Education | ₹40L | 10 years | High |
| Retirement | ₹2Cr | 25 years | High |

The client may create:

**Family Security Basket**

containing all three goals.

The system can then see both levels:

```text
Family Security Basket
├── Emergency Fund
├── Child Education
└── Retirement
```

Each goal still receives its own DefinedGoal calculation and strategy evaluation.

## 7. Planning Logic

Basket-level planning should eventually follow this sequence:

1. Load all active goals belonging to the basket.
2. Load each goal's DefinedGoal state.
3. Evaluate individual goal feasibility and strategy eligibility.
4. Aggregate required funding and funding gaps.
5. Compare combined requirements with the investor's available resources.
6. Apply goal priorities and constraints.
7. Resolve resource conflicts/trade-offs.
8. Send the resulting goal set into Multi-Goal Orchestration.
9. Produce a consolidated financial plan.

## 8. Important Distinction

There are three separate concepts:

**Goal** — what the client wants to achieve.

**Goal Basket** — which goals the client wants to consider together.

**Strategy** — how a particular goal should be funded/achieved given the investor's financial state and constraints.

Therefore:

```text
Basket ≠ Goal
Basket ≠ Strategy
Basket = Planning Group
```

## 9. Implementation Status

The current backend work establishes the conceptual/data-model layer for goal grouping without changing the Supabase schema.

The next implementation stages are:

### Stage A — Basket persistence

Add durable basket storage and goal-to-basket membership.

### Stage B — Basket APIs

Add create, read, update and membership-management endpoints.

### Stage C — Basket calculations

Calculate aggregate funding requirements, gaps and resource demand without losing individual-goal calculations.

### Stage D — Orchestration integration

Feed basket membership into the existing Multi-Goal Orchestrator so related goals can participate in collective resource allocation.

### Stage E — Financial Plan output

Expose basket-level summaries, trade-offs and allocation decisions in the consolidated Financial Plan.

## 10. QA Rules

The implementation must preserve these invariants:

1. A basket cannot change the identity of a goal.
2. Removing a goal from a basket must not delete the goal.
3. Deleting a basket must not delete its member goals.
4. Individual goal calculations must remain reproducible.
5. Basket totals must equal the aggregation of its current active members.
6. Basket-level planning must respect individual goal constraints.
7. Resource allocation must not silently exceed available investor resources.
8. Existing single-goal strategy flows must continue to work when a goal has no basket.

## 11. Target End State

The final system should allow a client/advisor to organize goals into meaningful planning baskets while Planvesto continues to make decisions at the correct level:

```text
Client Intent
    ↓
Goal Basket
    ↓
Goals
    ↓
Defined Goals
    ↓
Eligibility
    ↓
Individual Strategies
    ↓
Multi-Goal Orchestration
    ↓
Resource Allocation & Trade-offs
    ↓
Complete Financial Plan
```

The basket is therefore a **planning abstraction above goals**, designed to make multi-goal financial planning more understandable and operational without compromising the existing goal-level decision architecture.
