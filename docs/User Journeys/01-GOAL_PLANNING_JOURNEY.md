# Goal Planning Journey

**Document Type:** User Journey  
**Status:** CANONICAL DESIGN  
**Scope:** Goal Setup → Goal Feasibility → Strategy Decision

---

## 1. Main Journey

```
Select / Create Goal
        ↓
Goal Details
        ↓
Target Date
        ↓
Future Target
        ↓
Map Existing Assets
        ↓
Project Mapped Assets
        ↓
Funding Gap
        ↓
Required Contribution / Return
        ↓
Financial Capacity
        ↓
Goal Feasibility
        ↓
Investor Review
        ↓
Decision
        ↓
Strategy Decision
```

---

## 2. Goal Setup

```
Canonical Goal
      +
Goal Details
      +
Target Date
      +
Mapped Assets
      ↓
Validated Goal Inputs
```

---

## 3. System Outputs

| Stage | Output |
|---|---|
| Goal Validation | Valid / Missing Inputs |
| Timeline | Time Remaining |
| Target Calculation | Future Requirement |
| Asset Projection | Projected Mapped Resources |
| Funding Gap | Gap / Surplus |
| Required Contribution | Contribution Amount |
| Goal-Level Return Required | Required Return |
| Financial Capacity | Available Capacity + Obligations |
| Goal Feasibility | Feasibility Result + Reasons |

---

## 4. Goal Feasibility

### Approach 1 — Financial Optimization

```
Current Goal Conditions
          ↓
Financial Capacity
          ↓
Compare Relevant Funding Paths
          ↓
Constraints + Opportunity Cost
          ↓
Recalculate Feasibility
          ↓
     ┌────┴─────┐
     ↓          ↓
  Feasible   Still Infeasible
     ↓          ↓
 Investor    Approach 2
   Review
```

**Compare where relevant:**
- Goal Funding
- Debt Prepayment
- Loan / EMI Changes
- Liquidity
- Competing Goals
- Opportunity Cost

### Approach 2 — Goal Adjustment

*Only if Approach 1 remains infeasible.*

```
Still Infeasible
       ↓
Calculate Required Change
       ↓
┌──────┼────────┐
↓      ↓        ↓
Lower  Later    Combined
Target Date     Change
└──────┼────────┘
       ↓
Recalculate
       ↓
Investor Review
       ↓
Accept / Reject
```

**Rule:** No automatic goal change. No forced feasibility.

### Other Results

```
Missing / Invalid Evidence
          ↓
        Unknown
          ↓
   Obtain Evidence
          ↓
      Recalculate
```

```
No Acceptable Path
        ↓
Show Shortfall + Constraints
        ↓
Preserve Current Goal
```

---

## 5. Investor Adjustment Loop

```
Input Changed
     ↓
Recalculate Affected Outputs
     ↓
Funding Gap / Contribution / Return
     ↓
Funding Paths + Feasibility
     ↓
Investor Review
```

| Changed Input | Recheck |
|---|---|
| Target Date | Timeline, Target, Funding, Feasibility |
| Target Amount / Cost | Target, Gap, Contribution / Return, Feasibility |
| Asset Mapping / Value | Projected Assets, Gap, Funding Paths |
| Income / Expenses / Surplus | Capacity, Funding Paths, Feasibility |
| Debt / EMI / Terms | Cash Flow, Debt Paths, Feasibility |
| Return / Inflation Assumptions | Affected Projections + Calculations |
| Priority / Flexibility / Constraint | Path Eligibility + Feasibility |

---

## 6. Investor Result

```
Goal + Target Date
        ↓
Future Requirement
        ↓
Projected Resources
        ↓
Funding Gap
        ↓
Required Contribution / Return
        ↓
Financial Capacity
        ↓
Feasibility + Reasons
        ↓
Funding Paths + Trade-offs
        ↓
Next Action
```

**Result labels:**
- Feasible
- Constrained
- Infeasible
- Unknown
- No Acceptable Path

---

## 7. Whole-Plan Impact

```
Material Shared-Resource / Plan Impact?
                 ↓
           ┌─────┴─────┐
           ↓           ↓
           No          Yes
           ↓           ↓
       Goal-Level   Assess Affected
         Result     Goals + Plan
```

---

## 8. Strategy Decision Handoff

```
Defined Goal
     +
Financial State
     +
Funding / Feasibility Evidence
     +
Relevant Constraints
        ↓
Strategy Decision / Strategy Builder
```

**Goal Planner:** Goal requirement + funding paths + feasibility  
**Strategy Builder:** Strategy / variant and execution design  
**Accepted Plan:** Investor adoption required

---

## 9. Example

```
Education Goal
      ↓
Target: 10 Years
      ↓
Future Education Cost
      ↓
Mapped Assets + Projection
      ↓
Funding Gap
      ↓
Required Contribution / Return
      ↓
Financial Capacity
      ↓
Goal Feasibility
      ↓
Investor Review
```

*Example inputs are illustrative, not system defaults.*

---

## 10. Core Rule

```
Goal Planning
      ↓
Define + Calculate + Test
      ↓
Goal Feasibility
      ↓
Investor Decision
      ↓
Strategy Decision
```
