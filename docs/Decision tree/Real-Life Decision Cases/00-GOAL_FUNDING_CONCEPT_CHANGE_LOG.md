# Case 1 — Goal Funding Concept Change Log

**Location:** `docs/Decision tree/Real-Life Decision Cases/`  
**Purpose:** Preserve the complete business discussion that started from Real-Life Case 1 and led to the clarification of Goal Funding, Goal Planner feasibility, and Strategy Builder responsibilities.  
**Status:** Business concept clarification — NOT yet implemented or frozen in code.

---

## 1. Why This Record Exists

We started the real-life validation process with a concrete financial case.

The purpose was not simply to create an example. The purpose was to look at the case, ask the financial questions that naturally arise from it, determine the correct mathematical/business answer, and use that discussion to identify what the Decision Tree should actually do.

The discussion exposed an important boundary:

> **Goal Funding / Goal Feasibility belongs to the Goal Planner, not to the Strategy Builder.**

The Strategy Builder receives the feasibility result and designs the detailed strategy and execution path.

This document preserves the case, the questions that arose from it, and the decisions reached during the discussion.

---

# 2. Real-Life Case 1

## Client Situation

A client is planning for **Retirement**.

| Item | Case 1 |
|---|---:|
| Current age | 35 years |
| Retirement age | 60 years |
| Goal horizon | 25 years |
| Current retirement corpus | ₹20 lakh |
| Required retirement corpus | ₹2 crore |
| Monthly income | ₹2,00,000 |
| Monthly expenses | ₹1,20,000 |
| Existing EMI | ₹10,000 |
| Approx. monthly surplus after expenses and EMI | ₹70,000 |
| Emergency fund | Adequate |
| Liquidity | Adequate |
| Debt burden | To be evaluated in context |
| Risk capacity | To be evaluated from actual financial data |
| Higher-priority goal conflict | None assumed for the case |
| Implementation constraint | None assumed for the case |

The case also introduced a home-loan decision context in which the loan interest rate was discussed as approximately **8%**, while investment-return scenarios could potentially be higher, depending on the assumptions used.

The purpose was **not** to assume that 12%, 13% or 16% is guaranteed. Those are scenario assumptions that must be tested mathematically.

---

# 3. First Question: What Is the Correct Financial Decision?

The initial temptation was to identify a strategy directly from the client's debt position.

For example:

> There is a home loan → debt burden must be evaluated → perhaps Debt Reduction.

But the discussion immediately exposed a problem with making that decision in isolation.

A debt metric by itself does not tell us whether repaying the debt is the best decision **for this particular retirement goal**.

The real question became:

> **What happens if the client's available financial capacity is used for debt repayment instead of retirement funding, and what happens if it is used for investment instead?**

This led to the first major conclusion.

### Decision reached

**Do not decide Debt Reduction merely from the existence or level of debt.**

The system must compare alternative financial paths in the context of the actual goal.

---

# 4. Second Question: What Does “Debt Burden” Actually Mean Here?

The discussion examined the idea of saying that debt is “manageable” or “high.”

That turned out to be insufficiently precise.

A debt burden cannot be evaluated only as an isolated DTI/EMI number because the same debt position can have different consequences depending on:

- the goal;
- goal horizon;
- available surplus;
- loan interest rate;
- remaining tenure;
- liquidity;
- investment opportunity;
- required goal funding;
- risk capacity;
- competing goals.

For example, an 8% home loan does not automatically mean:

> “Repay the loan first.”

The system must understand what the client gives up by using surplus cash to repay that loan.

### Decision reached

**Debt should be evaluated as part of the goal's financial scenario, not as an isolated decision rule.**

---

# 5. Third Question: What Is the Opportunity Cost?

This became the central question of Case 1.

Suppose the client has ₹70,000 monthly surplus.

That money can have different uses.

For example:

```
Use surplus for faster debt repayment
                vs
Use surplus for retirement investment
                vs
Change loan structure and invest the released EMI
```

Each choice produces a different future outcome.

### Debt repayment path

Potential benefits:

- interest saved;
- lower outstanding debt;
- potentially shorter loan duration;
- lower future debt obligation.

Potential cost:

- money that could otherwise have been invested for retirement is redirected toward debt.

### Investment path

Potential benefits:

- greater retirement corpus if investment returns exceed the relevant debt cost;
- increased goal funding.

Potential cost:

- loan continues;
- interest continues;
- investment outcome is uncertain;
- additional risk may be taken.

### Loan restructuring path

For example:

```
Longer loan tenure
        ↓
Lower EMI
        ↓
Higher monthly surplus
        ↓
Additional retirement investment
```

But:

```
Longer tenure
        ↓
Higher total interest
        ↓
Debt remains outstanding longer
```

Therefore both sides must be calculated.

### Decision reached

> **The system should compare opportunity cost between alternative feasible financial paths instead of applying a one-dimensional “debt is high → repay debt” rule.**

---

# 6. Fourth Question: What Should Goal Funding Actually Mean?

This question changed the original understanding of Goal Funding.

The earlier working interpretation treated Goal Funding largely as predefined funding variants:

- Existing Assets
- SIP
- Lump Sum
- Lump Sum + SIP
- Lump Sum + Step-up SIP
- Step-up SIP

The discussion established that these are **funding mechanisms**, not the complete Goal Funding decision.

A SIP by itself does not answer:

> “How can this client's retirement goal be made feasible?”

The system first needs to understand the client's actual financial situation.

### Decision reached

> **Goal Funding should determine how the client's goal can be made financially feasible using the client's actual financial data and alternative financial scenarios.**

---

# 7. Fifth Question: What Should Goal Funding Do?

The resulting conceptual process is:

```
Client Financial Data
        ↓
Goal Definition
        ↓
Understand Current Financial Situation
        ↓
Identify Goal Funding Gap
        ↓
Create Alternative Financial Scenarios
        ↓
Calculate Financial Outcome of Each Scenario
        ↓
Compare Feasibility / Opportunity Cost / Trade-offs
        ↓
Produce Goal Funding / Feasibility Paths
        ↓
Explain How the Goal Can Become Feasible
```

The scenarios can potentially consider:

- existing assets;
- existing monthly surplus;
- expenses;
- debt and EMI;
- loan interest;
- remaining loan tenure;
- liquidity/reserves;
- additional contribution capacity;
- goal horizon;
- current goal funding;
- required return;
- alternative debt structures;
- alternative contribution structures;
- changes in goal timing;
- combinations of multiple actions.

The exact calculation rules are **not yet frozen**.

---

# 8. Sixth Question: Is Goal Funding a Strategy Builder Strategy?

This was the next important clarification.

The answer is:

> **No.**

Goal Funding is **not a Strategy Builder strategy**.

Goal Funding belongs to the **Goal Planner / Goal Feasibility function**.

Its responsibility is to answer:

> **Can this goal be made feasible, and what financial conditions/path make it feasible?**

The result of that analysis becomes an **input to the Strategy Builder**.

---

# 9. Correct Boundary Between Goal Planner and Strategy Builder

The correct architecture established by this discussion is:

```
CLIENT FINANCIAL DATA
        ↓
    GOAL PLANNER
        ↓
GOAL FEASIBILITY / GOAL FUNDING
        ↓
Feasible Financial Path
        ↓
========================
THIS BECOMES INPUT
========================
        ↓
  STRATEGY BUILDER
        ↓
Strategy Selection
        ↓
Variant
        ↓
Techniques
        ↓
Architecture
        ↓
Detailed Execution Steps
```

### Goal Planner / Goal Funding

Answers:

> **WHAT IS FEASIBLE?**

It determines the financial conditions and path required to make the goal feasible.

### Strategy Builder

Answers:

> **HOW DO WE EXECUTE THAT FEASIBLE PLAN?**

It takes the feasibility output and creates the detailed financial strategy.

For example, if Goal Planner determines that a retirement goal is feasible with a particular funding requirement, horizon, risk/return condition and asset structure, Strategy Builder can then determine the appropriate strategy and implementation structure.

A **Bucket Strategy** can therefore make sense at the Strategy Builder level because it is an actual strategy/architecture for executing the already-established feasibility.

---

# 10. Seventh Question: What Happens to SIP, Lump Sum and Similar Variants?

They should **not automatically be treated as the definition of Goal Funding**.

They are possible mechanisms that may appear inside a generated feasibility/funding path.

For example, Goal Planner might determine:

```
Goal Funding Requirement
        ↓
Existing Asset + Monthly Contribution
        ↓
Monthly Contribution implemented through SIP
```

Here:

- **Goal Funding** = the feasibility solution;
- **SIP** = one mechanism used to execute part of that solution.

Therefore:

> **SIP is not the Goal Funding strategy by itself.**

The final role of the currently defined Goal Funding variants remains **TO BE VALIDATED**.

---

# 11. Eighth Question: Does Strategy Builder Decide How the Goal Becomes Feasible?

Again, the answer is:

> **No.**

Strategy Builder should not independently recreate the Goal Planner's feasibility analysis.

It should consume the feasibility result.

The intended relationship is:

```
Goal Planner
    ↓
Goal Feasibility
    ↓
Goal Funding Path
    ↓
Strategy Builder
    ↓
Detailed Strategy
    ↓
Detailed Implementation
```

This prevents the two systems from independently making conflicting decisions about whether the goal is feasible.

---

# 12. What Strategy Builder Is Actually For

The Strategy Builder is a **detailed strategy and execution design layer**.

Once feasibility is established, it should answer questions such as:

- Which strategy should execute the feasible plan?
- Which variant fits?
- Which techniques should be used?
- How should the strategy be structured?
- Which components should be used?
- How should the execution be organized?
- What detailed steps should the investor follow?

For example:

> Goal Planner says the retirement goal is feasible under a defined funding path.

Then Strategy Builder can determine:

> Use a particular strategy, apply a Bucket Strategy, select appropriate techniques/components, and produce the detailed execution structure.

This is fundamentally different from Goal Planner asking:

> “Can the retirement goal be achieved at all, and what financial changes make it feasible?”

---

# 13. Ninth Question: What Is the Correct Overall Decision Flow?

The discussion therefore produced this separation:

```
1. CLIENT FINANCIAL DATA
          ↓
2. GOAL
          ↓
3. GOAL PLANNER
          ↓
4. GOAL FEASIBILITY
          ↓
5. GOAL FUNDING / FEASIBLE FINANCIAL PATH
          ↓
6. OPPORTUNITY-COST / SCENARIO ANALYSIS
          ↓
7. STRATEGY BUILDER INPUT
          ↓
8. STRATEGY SELECTION
          ↓
9. VARIANT
          ↓
10. TECHNIQUES
          ↓
11. ARCHITECTURE
          ↓
12. DETAILED EXECUTION PLAN
```

The exact internal ordering and rule ownership of the Strategy Builder remains subject to the separate Decision Tree validation process.

---

# 14. What Case 1 Actually Taught Us

Case 1 did not merely teach us how to handle a retirement goal.

It exposed a system-level distinction:

### Goal Planner

**Feasibility engine**

> Can the goal be achieved, and what financial path makes it achievable?

### Strategy Builder

**Strategy/execution engine**

> Given the feasible goal path, how should that path actually be implemented?

### Opportunity Cost

**Decision principle used when comparing alternative financial paths during feasibility analysis.**

This distinction should be preserved going forward.

---

# 15. What Was Explicitly Rejected

The following interpretations are rejected as the sole design:

### Rejected 1

> Debt exists → choose Debt Reduction.

### Rejected 2

> DTI is high → automatically stop investing and repay debt.

### Rejected 3

> Goal Funding = SIP/Lump Sum/Step-up SIP.

### Rejected 4

> Goal Funding is one of the Strategy Builder's investment strategies.

### Rejected 5

> Strategy Builder should independently determine whether the goal is feasible.

The correct model is goal-centric, scenario-based and mathematically comparative.

---

# 16. What Was Established

| Question | Decision |
|---|---|
| Should debt be evaluated in isolation? | **No** |
| Is DTI alone enough to decide Debt Reduction? | **No** |
| What is central to the decision? | **Opportunity cost and goal outcome** |
| Should alternative financial scenarios be compared? | **Yes** |
| Is Goal Funding just SIP/Lump Sum/etc.? | **No** |
| Where does Goal Funding belong? | **Goal Planner / Goal Feasibility** |
| What does Goal Funding produce? | **A feasible financial path / funding solution** |
| What does Strategy Builder consume? | **Goal feasibility/funding output** |
| What does Strategy Builder produce? | **Detailed strategy and execution structure** |
| Can Bucket Strategy be a Strategy Builder strategy? | **Yes, where appropriate to the feasible goal path** |
| Are exact Goal Funding rules frozen? | **No** |
| Are existing Goal Funding variants' final roles frozen? | **No** |

---

# 17. What Must Happen Before Implementation

The next real-life cases should follow the same method:

```
CASE
  ↓
QUESTIONS CREATED BY THE CASE
  ↓
INDEPENDENT FINANCIAL / MATHEMATICAL ANALYSIS
  ↓
DECISION REACHED
  ↓
WHAT THIS MEANS FOR THE SYSTEM
  ↓
CANONICAL RULE TO FREEZE LATER
```

For each case we should explicitly record:

1. **The client case**
2. **The financial question**
3. **Why the question matters**
4. **Alternative scenarios**
5. **Mathematical comparison**
6. **Opportunity cost**
7. **Expected financial decision**
8. **Which system layer owns that decision**
9. **Current code decision**
10. **Difference, if any**
11. **Rule that should eventually be frozen**

---

# 18. Final Business Principle from Case 1

> **Goal Funding is a Goal Planner / Goal Feasibility function. It uses the client's financial data to understand the goal, identify the funding gap, create alternative financial scenarios, compare their mathematical consequences and determine how the goal can be made feasible.**

> **The resulting feasibility/funding path is an input to the Strategy Builder. The Strategy Builder then determines the detailed strategy, techniques, architecture and execution steps required to implement that feasible plan.**

> **Financial decisions should be driven by the mathematical consequences and opportunity cost of alternative feasible paths, rather than by isolated rules or metrics.**

---

## Change Status

| Item | Status |
|---|---|
| Case 1 documented | **Complete** |
| Original Goal Funding interpretation | **Superseded** |
| Goal Funding = funding mechanisms only | **Rejected** |
| Goal Funding = Goal Planner feasibility function | **Business direction established** |
| Opportunity-cost comparison | **Core principle established** |
| Goal Planner → Strategy Builder boundary | **Clarified** |
| Strategy Builder as detailed execution layer | **Business direction established** |
| Existing Goal Funding variants' final role | **Not yet frozen** |
| Strategy Builder implementation changes | **Not made** |
| Goal Funding implementation changes | **Not made** |
| Canonical V1 rules | **Not frozen** |
| Next phase | **Real-life case validation** |
