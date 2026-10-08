# Goal Planning Journey

**Document Type:** Canonical Investor User Journey  
**Status:** DESIGN — CANONICAL JOURNEY, NOT IMPLEMENTATION DESCRIPTION  
**Scope:** From investor goal creation through Goal Feasibility and handoff to downstream Strategy Decisioning.

---

## 1. Purpose

This document defines the intended investor journey for planning an individual financial goal.

It describes:

- what the investor does;
- what the system asks for;
- what the system calculates;
- what the system validates;
- what the investor sees;
- where the journey branches;
- where the journey stops;
- what is handed to downstream decisioning.

This is a **future/canonical user journey**. It does not describe the current UI or current runtime sequence.

The Goal Planner is responsible for converting user-defined goal information and mapped assets into a canonical `DefinedGoal`, calculating the target-date funding requirement, and evaluating goal-level funding feasibility. It does not itself select the downstream Strategy. 

---

# 2. Journey Boundary

### Entry

Investor wants to create, review, or plan a financial goal.

### Exit

A versioned `DefinedGoal` exists with:

- canonical goal identity;
- timeline;
- future target;
- mapped assets;
- projected mapped asset value;
- funding gap;
- funding status;
- required contribution, where applicable;
- financial capacity evidence;
- goal feasibility status.

The resulting goal state can then be handed to downstream Strategy Decisioning.

### Important boundary

```
Goal Planning / Feasibility
        ↓
DefinedGoal
        ↓
Strategy Decision
```

Goal Planning does **not** silently choose Progressive De-risking, Capital Preservation, Debt Reduction, Credit Utilisation, or another Strategy.

---

# 3. High-Level Investor Journey

```
Investor
  ↓
Create / Select Goal
  ↓
Enter Goal Details
  ↓
System Validates Goal Input
  ↓
Goal Normalisation
  ↓
Timeline Calculation
  ↓
Future Target Calculation
  ↓
Map Existing Assets
  ↓
Project Mapped Assets
  ↓
Funding Gap Calculation
  ↓
Required Contribution Calculation
  ↓
Read Financial Capacity
  ↓
Goal Feasibility Assessment
  ↓
Investor sees Goal Planning Result
  ↓
Continue / Adjust / Stop
  ↓
DefinedGoal
  ↓
Strategy Decisioning
```

---

# 4. Journey Stages

## Stage 1 — Goal Creation

### Investor action

Investor chooses to create or plan a goal.

The investor provides the goal context, including where applicable:

- goal type;
- goal name;
- today's cost / target amount basis;
- target month/year;
- priority;
- flexibility;
- status;
- relevant dynamic details.

### System action

The system validates the supplied goal information and prepares it for canonical processing.

### Output

**Validated Goal Input**

---

## Stage 2 — Goal Normalisation

### System action

The system converts the raw goal type/name into the canonical goal vocabulary.

Example:

```
Raw Goal Input
      ↓
Canonical Goal Type
      ↓
Canonical Goal Name
```

### Important rule

Normalisation is a system operation. The investor should not have to understand internal canonical IDs.

### Output

Canonical goal identity.

---

# 5. Stage 3 — Goal Timeline

### Investor input

Target month/year.

### System action

The system calculates the duration from the reference date to the target date.

### Output

```
duration_years
```

### Investor-facing meaning

The investor should understand:

> "Your goal is approximately X years away."

The system may use the exact internal duration for calculations, while presenting a human-readable timeline.

---

# 6. Stage 4 — Future Target

### System action

The system calculates the future funding requirement from:

- today's cost;
- inflation assumption;
- duration;
- goal type;
- goal-specific calculation rules where applicable.

Retirement may use a specialised retirement-corpus calculation rather than the generic inflation projection.

### Output

```
future_target
```

### Investor-facing meaning

The investor should see the distinction between:

- today's estimated cost; and
- estimated amount required at the target date.

The calculation should be explainable rather than presented as an unexplained number.

---

# 7. Stage 5 — Asset Mapping

### Investor action

Investor identifies assets that are intended to support the goal, where applicable.

### System action

The system records the relevant planning-unit assets and their applicable characteristics, such as:

- allocation type;
- value;
- expected return;
- return frequency;
- duration.

### Output

```
mapped_assets
```

---

# 8. Stage 6 — Asset Projection

### System action

The system projects the mapped assets toward the target date using the applicable planning assumptions.

### Output

```
projected_mapped_asset_value
```

### Investor-facing meaning

The system should explain:

> "Based on the assets currently mapped to this goal, the projected value at the target date is approximately X."

This is a planning projection, not a guarantee.

---

# 9. Stage 7 — Funding Gap

The system compares:

```
Future Target
        -
Projected Mapped Asset Value
        =
Funding Gap
```

### Funding status

| Result | Status |
|---|---|
| Positive gap | Shortfall |
| Approximately zero | On Track |
| Negative gap | Overfunded |

### Investor-facing result

The investor should immediately understand:

- required future amount;
- currently projected funding;
- surplus/shortfall;
- whether additional funding is currently indicated.

---

# 10. Stage 8 — Required Contribution

If a positive funding gap exists, the system calculates the required contribution using the applicable funding return assumption and remaining duration.

### Output

```
required_monthly_contribution
```

If no positive gap exists, a new contribution may not be required for the current planning state.

### Important boundary

This is **Goal Planner calculation**, not Strategy Selection.

Contribution Escalation, SIP step-up, and similar mechanisms should not be interpreted here as automatically selected Strategy Builder techniques.

---

# 11. Stage 9 — Financial Capacity

The system reads the current Financial State snapshot.

Primary capacity input:

```
investable_surplus_monthly
```

### Purpose

Determine whether the contribution requirement can be supported by the investor's current financial capacity.

### Important boundary

Financial capacity is evidence for feasibility. It does not by itself decide the Strategy.

---

# 12. Stage 10 — Goal Feasibility

The system compares:

```
Required Monthly Contribution
        vs
Available Monthly Surplus
```

The Goal Planner can return:

- **Feasible**
- **Constrained**
- **Infeasible**
- **Unknown** when required financial-state evidence is unavailable.

### Investor-facing interpretation

**Feasible**

> The current funding requirement appears supportable from the available monthly surplus.

**Constrained**

> The goal may be possible, but the current funding requirement puts pressure on available capacity.

**Infeasible**

> The current goal funding requirement cannot be supported by the available financial capacity under the current assumptions.

**Unknown**

> The system does not have sufficient financial-state evidence to determine feasibility.

---

# 13. Decision Branches

## Branch A — Feasible

```
Goal Feasibility = Feasible
        ↓
Investor reviews result
        ↓
Continue
        ↓
DefinedGoal
        ↓
Strategy Decisioning
```

The Strategy Decision subsystem now evaluates which Strategy is appropriate.

---

## Branch B — Constrained

```
Goal Feasibility = Constrained
        ↓
Investor sees constraint
        ↓
Possible planning adjustment
        ├─ Target date
        ├─ Goal amount / scope
        ├─ Asset mapping
        └─ Other permitted goal assumptions
        ↓
Recalculate
```

The journey can loop back to the affected planning stage.

The system must not silently change the investor's goal to make it feasible.

---

## Branch C — Infeasible

```
Goal Feasibility = Infeasible
        ↓
Investor sees funding shortfall / capacity issue
        ↓
Possible goal-planning adjustment
        ├─ Change target
        ├─ Change scope
        ├─ Review mapped assets
        └─ Review funding assumptions
        ↓
Recalculate
```

If the investor does not change the goal or planning assumptions, the system should preserve the infeasible state.

This does **not** mean that a Strategy should automatically be selected merely to force feasibility.

---

## Branch D — Unknown

```
Goal Feasibility = Unknown
        ↓
Missing financial-state evidence
        ↓
Request / obtain required evidence
        ↓
Recalculate feasibility
```

Missing information must not silently become either Feasible or Infeasible.

---

# 14. Investor Adjustment Loop

The Goal Planning journey is iterative.

```
Goal State
   ↓
Investor Changes Relevant Input
   ↓
Recalculate Affected Outputs
   ↓
Funding Gap
   ↓
Required Contribution
   ↓
Financial Capacity / Feasibility
   ↓
Updated Goal State
```

The system should avoid forcing the investor through unrelated steps again when only one planning input changed.

Examples:

- changing target date → recalculate duration, future target, funding gap, contribution, feasibility;
- changing today's cost → recalculate future target and downstream funding calculations;
- changing mapped assets → recalculate projected mapped value, funding gap, contribution and feasibility;
- changing financial capacity → re-evaluate feasibility without unnecessarily changing the goal definition.

---

# 15. What the Investor Should See

At the end of Goal Planning, the investor should have a clear planning summary:

```
Goal
Target Date
Future Target
Mapped Assets
Projected Asset Value
Funding Gap
Funding Status
Required Contribution
Available Monthly Surplus
Goal Feasibility
```

The result should answer:

> **"Is this goal currently financially supportable, and what funding requirement does it create?"**

It should not prematurely answer:

> **"Which Strategy should I use?"**

That belongs downstream.

---

# 16. Handoff to Strategy Decision

Once the goal state is sufficiently defined:

```
DefinedGoal
   +
Current Financial State
   +
Feasibility / Funding Evidence
   +
Relevant Constraints
        ↓
Strategy Decision
```

The downstream Strategy Decision may then evaluate:

- Strategy Applicability;
- Candidate Viability / Eligibility;
- Strategy Selection;
- Variant;
- Technique;
- Method / Policy;
- Architecture / Solution;
- Stress / Resilience;
- Decision / Recommendation.

Goal Planning therefore provides **decision evidence**, not the final Strategy decision.

---

# 17. What-If Boundary

What-if is **not a mandatory Goal Planning stage**.

A what-if may be introduced when the investor or system wants to test a proposed change.

Example:

```
Current Goal State
        ↓
What if target date moves by 2 years?
        ↓
Recalculate
        ↓
Compare funding / feasibility impact
```

The scenario remains separate from the accepted goal state until the investor adopts the change.

---

# 18. Whole-Plan Boundary

Whole-Plan / Multi-Goal Impact is not required for every individual Goal Planning journey.

It becomes relevant when the goal or proposed change affects:

- competing goals;
- shared financial resources;
- an existing accepted plan;
- another material plan-level dependency.

Then:

```
Goal Feasibility
        ↓
Whole-Plan / Multi-Goal Impact
        ↓
Investor Decision
```

The existing accepted plan should not be silently overwritten by a proposed new goal or changed goal.

---

# 19. Accepted Plan Boundary

Goal Planning does not create an Accepted Plan.

The downstream sequence is:

```
Goal Planning
    ↓
Strategy Decision
    ↓
Implementation Design
    ↓
Stress / Resilience
    ↓
Decision / Recommendation
    ↓
Investor Decision / Adoption
    ↓
Accepted Plan
```

Only after investor adoption should the accepted plan become the basis for downstream Action Plan and Execution.

---

# 20. Micro Journey Example

### Investor says:

> "I want to fund my child's education in 10 years."

### System journey

```
Select Education
        ↓
Enter target information
        ↓
Enter target date
        ↓
Map existing education assets
        ↓
System calculates 10-year duration
        ↓
System calculates future target
        ↓
System projects mapped assets
        ↓
System calculates funding gap
        ↓
System calculates required contribution
        ↓
System reads monthly investable surplus
        ↓
System assesses feasibility
        ↓
Investor sees result
        ↓
Continue to Strategy Decision
```

The system should **not** jump directly from "Education" to "Progressive De-risking" simply because the goal has a 10-year horizon.

Strategy selection happens after the Goal Planner has produced the required evidence.

---

# 21. Failure / Exception Journeys

The Goal Planning journey must explicitly handle:

### Invalid goal input

```
Invalid Input
   ↓
Explain missing / invalid field
   ↓
Investor corrects input
```

### Missing financial capacity

```
Financial Capacity Unavailable
   ↓
Feasibility = Unknown
   ↓
Obtain required evidence
   ↓
Recalculate
```

### Funding shortfall

```
Funding Gap
   ↓
Required Contribution
   ↓
Capacity Comparison
   ↓
Constrained / Infeasible
```

### Goal change after planning

```
Existing Goal State
   ↓
Investor changes goal
   ↓
Recalculate affected planning outputs
   ↓
Targeted downstream revalidation
```

### New goal against an existing plan

This becomes a plan-level journey and can invoke Whole-Plan / Multi-Goal Impact before adoption.

---

# 22. System Responsibilities vs Investor Responsibilities

| Step | Investor | System |
|---|---|---|
| Goal definition | Provides intent and goal information | Validates and normalises |
| Timeline | Provides target date | Calculates duration |
| Target | Provides cost/goal context | Calculates future target |
| Asset mapping | Identifies intended assets | Projects mapped assets |
| Funding gap | Reviews result | Calculates gap/status |
| Contribution | Reviews requirement | Calculates requirement |
| Capacity | Provides/maintains financial data | Reads current financial capacity |
| Feasibility | Reviews implication | Calculates feasibility |
| Adjustment | Decides whether to change goal assumptions | Recalculates affected outputs |
| Strategy | Investor proceeds to strategy decision | Downstream system evaluates strategies |

---

# 23. Canonical Rules for This Journey

1. Goal Planning owns **goal definition, target calculation, funding-gap calculation and goal-level funding feasibility**.
2. Goal Planning does not own final Strategy Selection.
3. Funding Status and Goal Feasibility are distinct outputs.
4. Financial capacity is evidence for feasibility, not a Strategy by itself.
5. Missing financial-state evidence produces **Unknown**, not an invented feasibility result.
6. Investor goal inputs must not be silently changed by the system.
7. Proposed changes remain proposed until the investor adopts them.
8. Whole-Plan / Multi-Goal Impact is conditional, not mandatory for every goal.
9. What-if is an optional scenario mechanism, not a mandatory Goal Planning stage.
10. A feasible goal does not imply a particular Strategy.
11. An infeasible goal does not justify automatically selecting Credit Utilisation or Debt Reduction.
12. The canonical `DefinedGoal` is the handoff object to downstream decisioning.
13. The journey must support recalculation when relevant inputs change.
14. Goal Planning should not create an Accepted Plan; investor adoption occurs downstream.

---

# 24. Journey Summary

```
INVESTOR INTENT
      ↓
GOAL INPUT
      ↓
VALIDATION / NORMALISATION
      ↓
TIMELINE
      ↓
FUTURE TARGET
      ↓
ASSET MAPPING / PROJECTION
      ↓
FUNDING GAP
      ↓
REQUIRED CONTRIBUTION
      ↓
FINANCIAL CAPACITY
      ↓
GOAL FEASIBILITY
      ↓
┌───────────────┬────────────────┬────────────────┐
│   FEASIBLE    │   CONSTRAINED  │  INFEASIBLE    │
│       ↓       │       ↓        │       ↓        │
│    REVIEW     │    ADJUST      │    ADJUST      │
│       ↓       │       ↓        │       ↓        │
└───────┬───────┴────────┬───────┴────────┬───────┘
        │                │                │
        └────────────── RECALCULATE ─────┘
                         ↓
                   DEFINED GOAL
                         ↓
                STRATEGY DECISION
```

---

## Reference Basis

This journey is derived from the canonical Goal Planner architecture and the canonical product/decision architecture. Current implementation details are treated as audit evidence, not as authority for the target journey.

**Primary reference:** `docs/architecture/goal-planner.md`

**Related reference areas:**
- Decision Engine / Strategy Decision architecture
- Strategy applicability and eligibility
- Strategy → Variant → Technique → Architecture
- Real-Life Decision Cases
- Product lifecycle / investor adoption / accepted-plan flow
