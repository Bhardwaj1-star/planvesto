# Goal Planning Journey

**Document Type:** User Journey  
**Status:** CANONICAL DESIGN  
**Scope:** Investor creates/plans a goal → Goal Planning result → handoff to Strategy Decision.

---

## 1. Journey

```
Investor wants a goal
        ↓
Create / Select Goal
        ↓
Enter Goal Details
        ↓
System validates & normalises
        ↓
Target Date / Timeline
        ↓
Future Target
        ↓
Map Existing Assets
        ↓
Project Assets
        ↓
Funding Gap
        ↓
Required Contribution
        ↓
Financial Capacity
        ↓
Goal Feasibility
        ↓
Investor reviews result
        ↓
Continue / Adjust
        ↓
Defined Goal
        ↓
Strategy Decision
```

---

## 2. What the Investor Does

1. Selects/creates a goal.
2. Enters goal details and target date.
3. Identifies assets intended for the goal.
4. Reviews the projected funding position.
5. Reviews feasibility.
6. Decides whether to continue or change the goal assumptions.

The investor owns the **goal intent and final choice**.

---

## 3. What the System Does

| Stage | System action | Investor sees |
|---|---|---|
| Goal input | Validate and normalise | Goal |
| Timeline | Calculate duration | Time remaining |
| Future target | Calculate target amount | Future requirement |
| Asset mapping | Project mapped assets | Expected funding |
| Funding gap | Compare target vs assets | Shortfall / On Track / Overfunded |
| Contribution | Calculate required contribution | Monthly requirement |
| Capacity | Read financial capacity | Available capacity |
| Feasibility | Assess funding supportability | Feasible / Constrained / Infeasible / Unknown |

---

## 4. Feasibility Branch

### Feasible

```
Feasible
   ↓
Review
   ↓
Continue
   ↓
Strategy Decision
```

### Constrained / Infeasible

```
Result
   ↓
Investor reviews issue
   ↓
Change permitted goal assumptions?
   ├─ Yes → Recalculate
   └─ No  → Preserve current result
```

The system must **not silently change the investor's goal** to make it feasible.

### Unknown

```
Missing financial evidence
        ↓
Feasibility = Unknown
        ↓
Obtain required evidence
        ↓
Recalculate
```

Missing data must not be treated as Feasible or Infeasible.

---

## 5. Investor Adjustment Loop

If the investor changes an input:

```
Changed Input
    ↓
Recalculate affected outputs
    ↓
Updated Funding Gap
    ↓
Updated Contribution
    ↓
Updated Feasibility
    ↓
Investor reviews again
```

Examples:

- Target date changes → timeline and downstream funding calculations update.
- Goal cost changes → future target and funding calculations update.
- Asset mapping changes → projected assets and funding gap update.
- Financial capacity changes → feasibility is re-evaluated.

---

## 6. What the Investor Should Get

At the end of Goal Planning:

```
Goal
Target Date
Future Target
Mapped Assets
Projected Asset Value
Funding Gap
Required Contribution
Financial Capacity
Goal Feasibility
```

The core question answered is:

> **"Is this goal financially supportable under the current assumptions?"**

---

## 7. Handoff

Goal Planning produces a canonical **Defined Goal**.

```
Defined Goal
     +
Financial State
     +
Funding / Feasibility Evidence
     +
Relevant Constraints
        ↓
Strategy Decision
```

Goal Planning does **not** decide:

- Progressive De-risking
- Capital Preservation
- Debt Reduction
- Credit Utilisation
- Variant
- Technique
- Solution

Those belong downstream.

---

## 8. Boundaries

**What-if:** optional. It can test a proposed change but does not automatically change the accepted state.

**Whole-Plan Impact:** conditional. It is used when the goal affects competing goals, shared resources, or an existing plan.

**Accepted Plan:** not created here. Investor adoption happens downstream.

---

## 9. Simple Example

Investor:

> "I want to fund education in 10 years."

Journey:

```
Education Goal
    ↓
10-year timeline
    ↓
Future education cost
    ↓
Existing education assets
    ↓
Projected asset value
    ↓
Funding gap
    ↓
Required contribution
    ↓
Available surplus
    ↓
Feasibility
    ↓
Continue to Strategy Decision
```

The system does **not** automatically say:

> "10 years = Progressive De-risking."

Strategy selection happens after Goal Planning.

---

## 10. Core Rule

**Goal Planning defines and tests the goal.  
Strategy Decision decides how the goal should be approached.**
