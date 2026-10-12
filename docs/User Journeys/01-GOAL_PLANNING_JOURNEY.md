# Goal Planning Journey

**Document Type:** User Journey  
**Status:** CANONICAL DESIGN  
**Purpose:** Show exactly what the investor does, what the system does, what is calculated, what the investor sees, and how Goal Planning establishes feasibility before Strategy Decision.

---

## 1. What this journey is solving

Investor has an objective such as:

> “I want to fund my retirement in 25 years.”

Goal Planning answers:

> **What exactly is the goal, what will it require, what resources are available, what funding gap exists, and what financial path can make the goal feasible?**

This is broader than simply comparing **Required Contribution vs Available Surplus**.

Where alternative uses of the investor's financial capacity exist, Goal Planning must be able to compare the **financial consequences and opportunity cost of alternative feasible paths**.

This does **not** mean that Goal Planning selects the Strategy Builder Strategy.

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
Current financial capacity
        ↓
Alternative feasible funding paths
        ↓
Financial outcome / opportunity-cost comparison
        ↓
Goal feasibility / funding path
        ↓
Investor reviews result
        ↓
Accept / Adjust / Stop
        ↓
Defined Goal + Feasibility Evidence
        ↓
Strategy Decision
```

---

## 3. Step-by-step journey

| Step | Investor does | System does | Investor sees | Output |
|---|---|---|---|---|
| 1. Start | Chooses a goal | Maps input to canonical goal type | Goal | Canonical Goal Type |
| 2. Goal details | Enters goal details, current cost and required context | Validates required fields and normalises input | Entered goal details | Normalised Goal Input |
| 3. Target date | Enters target month/year | Calculates time remaining | Time to goal | Goal Timeline |
| 4. Future target | Confirms/adjusts permitted assumptions | Calculates future target | Future requirement | Future Target |
| 5. Asset mapping | Selects assets intended for the goal | Validates mapping | Mapped assets | Asset Mapping |
| 6. Asset projection | Reviews assumptions | Projects mapped assets to goal date | Expected asset value | Projected Asset Value |
| 7. Funding gap | Reviews result | Compares future target with projected mapped assets | Shortfall / On Track / Overfunded | Funding Gap |
| 8. Capacity | Reviews current position | Determines available financial capacity and relevant constraints | Available capacity | Financial Capacity |
| 9. Funding paths | Reviews possible ways to close the gap | Evaluates alternative financially feasible paths using actual financial data | Alternative paths | Funding / Feasibility Paths |
| 10. Opportunity cost | Reviews trade-offs | Compares mathematical consequences of alternative uses of financial capacity | Benefits, costs, trade-offs | Opportunity-Cost Analysis |
| 11. Feasibility | Reviews conclusion | Determines whether the goal can be made feasible under the analysed assumptions/path | Feasible / Constrained / Infeasible / Unknown | Goal Feasibility |
| 12. Decision | Accepts assumptions, adjusts them, or stops | Recalculates affected outputs | Updated result | Proposed Defined Goal |
| 13. Handoff | Continues | Packages goal + funding/feasibility evidence | Ready for Strategy Decision | Defined Goal |

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
**Target:** 2051  
**Duration:** 25 years

The calculated duration becomes part of the Goal Planning evidence.

---

### 4.2 Future target

```
Today's Cost
     ↓
Approved Assumption
     ↓
Time to Goal
     ↓
Future Target
```

The exact calculation uses the canonical Goal Planner calculation.

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

Only resources mapped to the goal participate in the mapped-asset projection.

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

A shortfall is **not automatically a reason to select Credit Utilisation or Debt Reduction**.

---

### 4.5 Required contribution

Where a positive funding gap remains:

```
Funding Gap
     ↓
Time Remaining
     ↓
Required Contribution
```

This establishes one funding requirement.

It is not, by itself, the complete feasibility decision.

---

## 5. Financial capacity and alternative funding paths

Case 1 established an important requirement: the system should not treat debt, surplus or any single metric as an isolated decision.

For example, where an investor has monthly surplus available:

```
Available Financial Capacity
          ↓
      Alternative Uses
          │
          ├── Additional Goal Funding / Investment
          │
          ├── Faster Debt Repayment
          │
          └── Loan / Financing Restructuring
```

The actual alternatives depend on the investor's financial situation and the goal.

The system evaluates the relevant alternatives using:

- goal requirement;
- goal horizon;
- available surplus/capacity;
- existing assets;
- debt and EMI;
- debt cost;
- remaining tenure;
- liquidity/reserves;
- required goal funding;
- investment assumptions;
- repayment capacity;
- relevant constraints.

The system must not invent an alternative merely to produce a comparison.

---

## 6. Opportunity-cost analysis

**Opportunity cost is part of the feasibility/funding analysis when alternative uses of financial capacity materially change the goal or financial outcome.**

The question is:

> **What does the investor gain and give up by choosing one feasible financial path instead of another?**

### Example from the real-life case

A retirement client has approximately ₹70,000 monthly surplus and an existing home loan.

The system may need to compare:

```
Path A
Surplus → Faster Debt Repayment
       ↓
Interest Saving
       ↓
Lower Debt
       ↓
Less money deployed toward retirement during the period
```

versus:

```
Path B
Surplus → Retirement Investment
       ↓
Potentially Higher Retirement Corpus
       ↓
Loan Continues
       ↓
Interest Continues
       ↓
Investment Outcome Is Uncertain
```

A further feasible scenario may be:

```
Path C
Loan Restructuring
       ↓
Lower EMI
       ↓
Higher Monthly Investable Surplus
       ↓
Additional Retirement Investment
       ↓
But Potentially Higher Total Interest
```

The system compares the **mathematical consequences and trade-offs** of the relevant paths.

It does **not** apply:

> “Debt exists → Debt Reduction.”

It also does **not** apply:

> “Expected investment return is higher → Investment is automatically better.”

Investment returns are assumptions/scenarios and must not be represented as guaranteed outcomes.

---

## 7. What Opportunity Cost produces

Opportunity-cost analysis should make the trade-off visible rather than hide it inside a generic feasibility label.

The investor should be able to see, where relevant:

| Comparison | Path A | Path B | Path C |
|---|---|---|---|
| Use of surplus | Debt repayment | Goal investment | Restructuring + investment |
| Debt outcome | Improved | Debt continues | Changed |
| Interest outcome | Lower | Continues | May increase/decrease depending on structure |
| Goal funding outcome | Changes | Changes | Changes |
| Liquidity | Changes | Changes | Changes |
| Investment outcome | Lower deployment | Higher deployment | Higher deployment possible |
| Key risk | Goal funding trade-off | Market/return uncertainty | Higher debt cost / tenure risk |
| Opportunity cost | Foregone goal investment | Foregone interest saving | Trade-off between both |

The exact columns depend on the case.

The system should show only calculations that are actually supported by the available evidence and assumptions.

---

## 8. Feasibility result

Feasibility is therefore not merely:

```
Required Contribution vs Available Surplus
```

The relevant model is:

```
Goal Requirement
      +
Financial State
      +
Funding Gap
      +
Relevant Financial Alternatives
      +
Opportunity Cost / Trade-offs
      +
Constraints
      ↓
Goal Feasibility / Feasible Funding Path
```

Possible result:

| Result | Meaning |
|---|---|
| **Feasible** | A financially supportable path exists under the stated assumptions |
| **Constrained** | A path may exist, but important financial constraints/trade-offs remain |
| **Infeasible** | Current evidence does not identify a supportable path |
| **Unknown** | Required evidence or assumptions are insufficient to establish feasibility |

**Important:** Opportunity cost does not automatically make a goal Infeasible. It explains the economic trade-off between feasible alternatives.

---

## 9. What happens when the investor changes something?

The system should recalculate the outputs affected by the change.

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
Funding Paths
   ↓
Opportunity Cost
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
Funding Paths
   ↓
Opportunity Cost
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
Funding Paths
   ↓
Feasibility
```

### Financial capacity / debt changes

```
Financial State Change
   ↓
Available Capacity
   ↓
Debt Economics / Financing Position
   ↓
Affected Funding Paths
   ↓
Opportunity-Cost Comparison
   ↓
Feasibility
```

Not every change requires every analysis to be rebuilt.

---

## 10. Feasibility branches

### Feasible

```
Feasible Path
     ↓
Investor reviews
     ↓
Continue
     ↓
Defined Goal + Feasibility Evidence
     ↓
Strategy Decision
```

### Constrained / Infeasible

```
Constraint / Infeasibility
        ↓
Investor sees:
• what caused it
• which assumptions matter
• available alternatives
• financial trade-offs
        ↓
Investor changes goal / assumptions / funding choice?
   ├── YES → Recalculate
   └── NO  → Keep result / stop
```

The system must **not silently reduce the goal, extend the date, assume extra funding, or select credit** merely to produce a feasible result.

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

## 11. What the investor should see at the end

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

**Financial Capacity**
- Available capacity
- Relevant debt/EMI information where applicable
- Relevant liquidity information

**Feasibility / Funding Analysis**
- Available feasible path(s)
- Important assumptions
- Opportunity-cost / trade-off analysis where material
- Key risks and limitations
- Goal feasibility

The investor should be able to answer:

> **“What do I need, what do I already have, what is the gap, what feasible paths are available, and what am I giving up by choosing one path over another?”**

---

## 12. What happens next

Goal Planning produces:

```
Defined Goal
      +
Financial State
      +
Funding / Feasibility Evidence
      +
Relevant Constraints
      +
Material Trade-offs
      ↓
Strategy Decision
```

Strategy Decision may later consider:

- Progressive De-risking
- Capital Preservation
- Debt Reduction
- Credit Utilisation
- No acceptable Strategy

Goal Planning does **not** select the Strategy Builder Strategy.

---

## 13. Important boundaries

### Goal Funding

Goal Funding is part of the **Goal Planner / Goal Feasibility function**.

It determines the financial path/options by which the goal can become feasible.

It is **not** a peer Strategy Builder Strategy.

### Opportunity Cost

Opportunity Cost is a **decision principle within feasibility/funding analysis when alternative financial paths are being compared**.

It is not itself a Strategy, Variant, Technique or Solution.

### Whole-Plan Impact

Whole-Plan Impact is not required for every goal.

It becomes relevant when a new/changed goal materially competes with existing goals/resources or otherwise creates a plan-level decision.

Opportunity-cost analysis can occur at Goal Planning level without requiring a Whole-Plan decision.

### What-If

Optional scenario analysis. A scenario does not automatically modify the accepted plan.

### Accepted Plan

Not created here. Investor adoption happens downstream.

---

## 14. Real-life case connection

The retirement case that established this requirement had:

- 25-year retirement horizon;
- ₹20 lakh current corpus;
- ₹2 crore required corpus;
- ₹2 lakh monthly income;
- ₹1.2 lakh monthly expenses;
- ₹10,000 EMI;
- approximately ₹70,000 monthly surplus;
- approximately 8% home-loan interest assumption.

The key question was not:

> “Does the client have debt?”

It was:

> **“What happens if the available financial capacity is used for debt repayment instead of retirement funding, or if the loan is restructured and the released EMI is invested?”**

That comparison is what exposed **Opportunity Cost as a core feasibility/funding consideration**.

The case established that the system should compare alternative feasible financial paths rather than apply a one-dimensional debt rule.

---

## 15. Example

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
Read financial capacity
   ↓
Identify relevant funding paths
   ↓
Compare financial consequences where alternatives matter
   ↓
Feasibility
```

Investor sees:

```
Future Target:              ₹X
Mapped Asset Projection:    ₹Y
Funding Gap:                ₹Z
Required Contribution:      ₹A/month
Available Capacity:         ₹B/month

Feasible Path(s):           ...
Trade-off / Opportunity
Cost (if material):         ...
Feasibility:                ...
```

Only after this does the system hand the Defined Goal and feasibility evidence to Strategy Decision.

It does **not** say:

> “Education + 10 years = Progressive De-risking.”

That is a downstream decision.

---

## 16. Core rule

**Goal Planning defines the goal, establishes the funding requirement, evaluates relevant feasible financial paths, and compares their mathematical consequences and material opportunity costs.**

**Strategy Decision decides how an established feasible path should be implemented through Strategy → Variant → Technique → Method/Policy → Architecture/Solution.**

**Investor remains the owner of goal intent and the final decision.**

---

## References

- `docs/architecture/goal-planner.md`
- `docs/Decision tree/Real-Life Decision Cases/00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md`
- `docs/Decision tree/Real-Life Decision Cases/03-CASE_3_MULTI_GOAL_FEASIBILITY_AND_ACTION_PLAN.md`
- `docs/existing features/Strategy-Builder/00-DECISION_ENGINE_DESIGN_SUMMARY.md`
- `docs/User Journeys/04-GOAL_FEASIBILITY_JOURNEY.md`
