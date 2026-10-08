# Goal Planning Journey

**Document Type:** User Journey  
**Status:** CANONICAL DESIGN  
**Purpose:** Show exactly what the investor does, what the system does, what is calculated, what the investor sees, and what happens next.

---

## 1. What this journey is solving

Investor has an objective such as:

> “I want to fund my child's education in 10 years.”

Goal Planning answers:

> **What exactly is the goal, how much will it require in the future, what resources are already available, what funding gap remains, and is that gap supportable from current financial capacity?**

It does **not** decide the Strategy.

---

## 2. Complete investor journey

```
Investor starts a goal
        ↓
Goal details
        ↓
System validates & normalises
        ↓
Timeline
        ↓
Future target
        ↓
Existing asset mapping
        ↓
Asset projection
        ↓
Funding gap
        ↓
Required contribution
        ↓
Financial capacity
        ↓
Goal feasibility
        ↓
Investor reviews result
        ↓
Accept / Adjust / Stop
        ↓
Defined Goal
        ↓
Strategy Decision
```

---

## 3. Step-by-step journey

| Step | Investor does | System does | Investor sees | Output |
|---|---|---|---|---|
| 1. Start | Chooses **Education** | Maps input to canonical goal type | Education | `education` |
| 2. Goal details | Enters goal name, beneficiary/context, current cost and other required details | Validates values and required fields | Entered goal details | Normalised Goal Input |
| 3. Target date | Enters target month/year | Calculates time remaining | e.g. 10 years | Goal Timeline |
| 4. Future target | Confirms/adjusts assumptions where permitted | Applies documented inflation/target assumptions | Future required amount | Future Target |
| 5. Asset mapping | Selects assets intended for this goal | Validates mapping and ownership/eligibility as applicable | Mapped assets | Asset Mapping |
| 6. Asset projection | Reviews assumptions | Projects mapped asset value to goal date | Expected asset value | Projected Asset Value |
| 7. Funding gap | Reviews result | Calculates Future Target − Projected Mapped Assets | Shortfall / On Track / Overfunded | Funding Gap |
| 8. Contribution | Reviews requirement | Calculates contribution needed when a positive gap exists | Required monthly contribution | Required Contribution |
| 9. Capacity | Reviews available capacity | Reads current investable surplus / relevant capacity | Available monthly capacity | Financial Capacity |
| 10. Feasibility | Reviews result | Compares required contribution with available capacity | Feasible / Constrained / Infeasible / Unknown | Goal Feasibility |
| 11. Decision | Accepts assumptions, adjusts them, or stops | Recalculates only affected outputs | Updated result | Proposed Defined Goal |
| 12. Handoff | Continues | Packages canonical goal + evidence | Ready for next stage | Defined Goal |

---

## 4. What is actually calculated

### 4.1 Timeline

```
Today
  ↓
Target Month / Year
  ↓
Duration
```

Example:

**Today:** 2026  
**Target:** 2036  
**Duration:** 10 years

The system should store the calculated duration rather than repeatedly deriving it differently in downstream modules.

---

### 4.2 Future target

If today's goal cost is ₹20 lakh and the approved inflation assumption is used:

```
Today's Cost
     ↓
Inflation Assumption
     ↓
Time to Goal
     ↓
Future Target
```

The exact calculation must use the canonical Goal Planner calculation already defined in the architecture.

The User Journey does not create a second formula.

---

### 4.3 Asset projection

```
Mapped Asset
     ↓
Current Value
     ↓
Projection Assumptions
     ↓
Projected Value at Goal Date
```

Only assets actually mapped to the goal participate in this calculation.

---

### 4.4 Funding gap

```
Future Target
      -
Projected Mapped Asset Value
      =
Funding Gap
```

Possible results:

- **Shortfall** — positive funding gap
- **On Track** — target is supportable by mapped resources under the model
- **Overfunded** — mapped resources exceed the target

---

### 4.5 Required contribution

If a positive funding gap exists:

```
Funding Gap
     ↓
Time Remaining
     ↓
Required Contribution
```

The result is an input to feasibility, **not automatically a Strategy**.

---

### 4.6 Feasibility

```
Required Contribution
        vs
Available Financial Capacity
        ↓
Goal Feasibility
```

Result:

| Result | Meaning |
|---|---|
| **Feasible** | Current capacity supports the calculated requirement under stated assumptions |
| **Constrained** | Goal may be possible but current capacity/assumptions create a constraint |
| **Infeasible** | Current evidence does not support the requirement |
| **Unknown** | Required evidence is missing or unreliable |

---

## 5. What happens when the investor changes something?

The system should **not recalculate everything blindly**.

### Target date changes

```
Target Date
   ↓
Timeline
   ↓
Future Target
   ↓
Asset Projection
   ↓
Funding Gap
   ↓
Contribution
   ↓
Feasibility
```

### Goal cost changes

```
Goal Cost
   ↓
Future Target
   ↓
Funding Gap
   ↓
Contribution
   ↓
Feasibility
```

### Asset mapping changes

```
Asset Mapping
   ↓
Projected Asset Value
   ↓
Funding Gap
   ↓
Contribution
   ↓
Feasibility
```

### Financial capacity changes

```
Financial Capacity
   ↓
Feasibility
```

This is important because later **targeted revalidation** depends on knowing which output is affected by which input.

---

## 6. Feasibility branches

### Feasible

```
Feasible
   ↓
Investor reviews
   ↓
Continue
   ↓
Defined Goal
   ↓
Strategy Decision
```

### Constrained / Infeasible

```
Constraint / Infeasibility
        ↓
Investor sees:
• what caused it
• which assumption matters
• what can be changed
        ↓
Investor changes assumption?
   ├── YES → Recalculate
   └── NO  → Keep result / stop
```

The system must **not silently reduce the goal, extend the date, assume extra funding, or select credit** just to produce a feasible result.

### Unknown

```
Missing / unreliable evidence
        ↓
Feasibility = Unknown
        ↓
Obtain / correct evidence
        ↓
Recalculate
```

Unknown is not Feasible and not Infeasible.

---

## 7. What the investor should see at the end

A useful Goal Planning result should show:

**Goal**
- Goal type/name
- Target date
- Priority/flexibility where applicable

**Funding**
- Today's cost
- Future target
- Mapped assets
- Projected mapped asset value
- Funding gap
- Required contribution

**Capacity**
- Available financial capacity
- Goal feasibility
- Key assumptions
- Data limitations, if any

The investor should be able to answer:

> **“What do I need, what do I already have, what is the gap, and can my current financial position support it?”**

---

## 8. What happens next

Goal Planning produces a **Defined Goal**.

Conceptually:

```
Defined Goal
      +
Financial State
      +
Feasibility / Funding Evidence
      +
Relevant Constraints
      ↓
Strategy Decision
```

The Strategy Decision may later consider:

- Progressive De-risking
- Capital Preservation
- Debt Reduction
- Credit Utilisation
- No acceptable Strategy

Goal Planning itself does **not** select any of them.

---

## 9. Important boundaries

### Goal Funding

Goal Funding is part of Goal Planner / Goal Feasibility.

It is **not** a peer Strategy Builder Strategy.

### Whole-Plan Impact

Not required for every goal.

It becomes relevant when a new/changed goal materially competes with existing goals or resources.

### What-If

Optional scenario analysis. A scenario does not automatically modify the accepted plan.

### Accepted Plan

Not created here. Investor adoption happens downstream.

---

## 10. Example

Investor says:

> “Education goal: ₹20 lakh today's cost, target in 10 years.”

System:

```
Education
   ↓
10-year timeline
   ↓
Future education target
   ↓
Map existing education assets
   ↓
Project mapped assets
   ↓
Calculate funding gap
   ↓
Calculate required contribution
   ↓
Read available monthly capacity
   ↓
Feasibility
```

Investor then sees something like:

```
Future Target:              ₹X
Mapped Asset Projection:    ₹Y
Funding Gap:                ₹Z
Required Contribution:      ₹A/month
Available Capacity:         ₹B/month
Feasibility:                Feasible / Constrained / Infeasible / Unknown
```

Only after this does the system hand the Defined Goal to Strategy Decision.

It does **not** say:

> “Education + 10 years = Progressive De-risking.”

That is a downstream decision.

---

## 11. Core rule

**Goal Planning defines the goal and establishes its funding/feasibility evidence.**

**Strategy Decision decides how the goal should be approached.**

**Investor remains the owner of goal intent and the final decision.**

---

## References

- `docs/architecture/goal-planner.md`
- `docs/Decision tree/00-DECISION_ENGINE_DESIGN_SUMMARY.md`
- `docs/User Journeys/04-GOAL_FEASIBILITY_JOURNEY.md`
- `docs/Decision tree/Real-Life Decision Cases/03-CASE_3_MULTI_GOAL_FEASIBILITY_AND_ACTION_PLAN.md`
