# Goal Funding — Concept Change Log

**Location:** `docs/Decision tree/Real-Life Decision Cases/`
**Purpose:** Preserve the business discussion and reasoning that changed the definition of Goal Funding before real-life decision cases are created.
**Status:** Business concept clarification — NOT yet implemented or frozen in code.

---

## 1. Why This Record Exists

Before implementing or freezing Strategy Builder decision rules, we are validating the decision tree through real-life financial cases.

During the first case discussion, an important conceptual clarification was reached about **Goal Funding**. This document preserves that reasoning so the original intent is not lost when the system is later changed.

This is a **historical business decision record**, not a technical implementation specification.

## 2. Original Working Interpretation

The existing Strategy Builder model treated Goal Funding largely through funding variants such as:

- Existing Assets
- SIP
- Lump Sum
- Lump Sum + SIP
- Lump Sum + Step-up SIP
- Step-up SIP

These are useful funding mechanisms, but the discussion established that they are **not sufficient to define Goal Funding as a complete financial decision process**.

> SIP, Lump Sum, Step-up SIP and similar mechanisms are ways of implementing funding. They should not by themselves define the Goal Funding decision.

## 3. New Business Understanding of Goal Funding

**Goal Funding should determine how a client's goal can be made financially feasible from the client's actual financial situation.**

The system should first understand the client's financial data and the goal, then create and compare scenarios before producing a goal-funding strategy.

Conceptual flow:

```
Client Financial Data
        ↓
Goal Definition
        ↓
Understand Current Financial Situation
        ↓
Identify Goal Funding Gap
        ↓
Create Alternative Scenarios
        ↓
Calculate Financial Outcome of Each Scenario
        ↓
Compare Feasibility / Opportunity Cost / Trade-offs
        ↓
Produce Goal Funding Strategy or Strategies
        ↓
Explain How the Goal Becomes Feasible
```

The important change is that **Goal Funding becomes a financial feasibility and scenario-generation process**, rather than a predefined list of contribution methods.

## 4. What the System Should Consider

Goal Funding should use the client's relevant financial data rather than assuming that a new SIP is always the answer.

Depending on the case, scenarios may consider:

- existing investable assets;
- current monthly surplus;
- current expenses;
- debt and EMI structure;
- loan interest and remaining tenure;
- liquidity/reserve position;
- existing assets that may be earmarked for the goal;
- additional contribution capacity;
- goal horizon;
- goal amount and current funding;
- required return / investment assumptions;
- changes to debt structure;
- changes to contribution pattern;
- changes to goal timing where appropriate;
- combinations of multiple actions.

The exact input set and decision rules remain to be validated through real-life cases.

## 5. Goal Funding Is Not the Same as a Funding Mechanism

| Layer | Meaning |
|---|---|
| **Goal Funding** | Determine how the goal can become financially feasible given the client's situation. |
| **Funding Strategy** | A scenario/path that makes the goal feasible. |
| **Funding Mechanism / Variant** | The concrete way money is deployed, such as SIP, Lump Sum, Step-up SIP, or use of existing assets. |
| **Financial Decision** | The broader decision about which path produces the best feasible outcome after constraints, risk and trade-offs are considered. |

## 6. Opportunity Cost Is Central

The first real-life case also clarified that the system is fundamentally trying to identify **opportunity cost**.

When a client has a home loan and investable surplus, the system should not automatically conclude:

> Debt exists → repay debt.

Instead, it should compare alternative uses of the available financial capacity.

For example:

```
Current Loan Structure
        vs
Faster Debt Repayment
        vs
Longer Tenure + Lower EMI + Investment of Released Cash Flow
```

For each scenario, the system should examine the mathematical consequences for the actual goal.

Conceptually:

```
Scenario
  ↓
Debt Cost
+ Investment Outcome
+ Cash-flow Change
+ Goal Funding Outcome
+ Liquidity / Risk Consequences
  ↓
Opportunity Cost / Trade-off
  ↓
Feasibility Decision
```

The system should therefore evaluate **alternative financial paths**, rather than applying isolated rules such as “high DTI means repay debt.”

## 7. Example from Case 1

The first case involved a retirement goal and a home loan.

The discussion considered the possibility that:

- the home loan interest rate is around 8%;
- the client may have investment opportunities with higher expected returns under some scenarios;
- the existing EMI reduces monthly investable surplus;
- extending the loan tenure could reduce EMI;
- the released monthly cash flow could potentially be directed toward the retirement goal;
- extending tenure also increases total interest and keeps the debt outstanding longer.

Therefore, the correct question is not simply:

> “Should the client repay the debt?”

The correct question is:

> **“Which feasible financial structure produces the best overall outcome for the client's retirement goal after considering debt cost, investment outcome, cash flow, liquidity and risk?”**

No final numerical answer was frozen from this discussion. The case must be fully calculated before any business rule is adopted.

## 8. Consequence for the Strategy Builder

This clarification changes how Goal Funding should be viewed inside the Strategy Builder.

**Goal Funding should not be treated as merely one more predefined investment strategy.**

Its role is to determine the feasibility of achieving the goal and generate the possible funding paths required to achieve it.

The broader strategy decision can then use that information when determining the appropriate financial approach.

Conceptually:

```
Goal
  ↓
Client Financial Situation
  ↓
Goal Funding Analysis
  ↓
Alternative Feasible Funding Paths
  ↓
Opportunity-Cost / Trade-off Analysis
  ↓
Strategy Decision
  ↓
Implementation Mechanism / Variant
```

The exact placement in the final canonical Decision Tree is **not yet frozen**. It must be validated through real-life cases.

## 9. What This Means for Existing Variants

The existing Goal Funding variants should **not automatically be deleted** merely because the concept has changed.

They should instead be treated as candidate implementation mechanisms until real-life validation determines their correct role.

Current examples:

- Existing Assets
- SIP
- Lump Sum
- Lump Sum + SIP
- Lump Sum + Step-up SIP
- Step-up SIP

Their final status is therefore **TO BE VALIDATED**.

## 10. What Is Now Explicitly Rejected as the Sole Definition

The following interpretation is rejected as an adequate definition of Goal Funding:

> **Goal Funding = choosing between SIP, Lump Sum, Step-up SIP and similar contribution variants.**

Those mechanisms can be part of the solution, but they do not answer the larger question:

> **How can this particular client's goal actually be made feasible?**

## 11. What Must Be Validated Next

Real-life cases should test Goal Funding across:

1. sufficient existing surplus;
2. insufficient monthly surplus;
3. existing assets that can fund part of the goal;
4. debt restructuring;
5. different loan interest rates;
6. different investment return assumptions;
7. different goal horizons;
8. combinations of debt, assets and contributions;
9. competing goals;
10. liquidity constraints;
11. risk-capacity constraints;
12. situations where multiple funding paths are feasible.

For each case, record:

```
Client Inputs
→ Goal
→ Current Funding Gap
→ Candidate Scenarios
→ Mathematical Outcome
→ Opportunity Cost / Trade-off
→ Goal Feasibility
→ Expected Business Decision
→ Current Code Decision
→ Difference
→ Rule Responsible
```

This evidence should determine the final Goal Funding rules.

## 12. Business Principle Preserved from This Discussion

> **Goal Funding is not simply a choice of SIP, Lump Sum or another contribution method. It is the process of using the client's financial data to understand the funding gap, create alternative financial scenarios, compare their mathematical consequences and determine how the goal can be made feasible.**

And, more broadly:

> **A financial decision should be driven by the opportunity cost and consequences of alternative feasible paths, subject to the relevant constraints and risk—not by an isolated financial metric or rule of thumb.**

## 13. Change Status

| Item | Status |
|---|---|
| Original Goal Funding interpretation | Superseded |
| Goal Funding as scenario/feasibility process | **Business direction established** |
| SIP/Lump Sum/etc. as complete Goal Funding strategies | Rejected as sole definition |
| Existing variants' final role | **Not yet frozen** |
| Opportunity-cost comparison | **Core decision principle identified** |
| Goal Funding implementation | **Not changed yet** |
| Canonical V1 rule | **Not frozen** |
| Real-life validation | **Next step** |

## 14. Important Boundary

This document records the business reasoning at the time of the change.

It does **not** authorize immediate code changes.

The next step is to use real-life financial cases to validate the concept, determine exact rules, and only then modify the canonical implementation.
