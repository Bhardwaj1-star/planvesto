# Case 1 — Goal Funding Concept Change Log

**Location:** `docs/Decision tree/Real-Life Decision Cases/`  
**Purpose:** Preserve the complete historical discussion that led to the clarification of Goal Funding, Goal Planner feasibility, and Strategy Builder responsibilities. Rejected or superseded statements are retained as history only and must not be used as current implementation instructions.  
**Status:** Historical business-decision log. It preserves earlier rejected interpretations and later corrections; it is not a standalone coding specification. The canonical target rule is settled: Goal Funding belongs to Goal Planner / Goal Feasibility and is not a Strategy Builder strategy. Current runtime/code migration is a separate task.

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


---

# 19. Case 2 — Education Goal: Feasible Goal, Then Strategy Execution

Case 2 was initially framed as a question about multiple Goal Funding paths. The discussion clarified that the case should be much simpler.

## Client Situation

An education goal is already defined and the purpose is to determine whether the goal is feasible and, once feasibility is established, what should happen next.

The important distinction is:

> **Once the goal is established as feasible, we do not need another layer that re-solves feasibility through Strategy Builder.**

Goal Planner can show the available funding mechanisms required to make the goal feasible, such as:

- SIP;
- lump sum;
- step-up SIP;
- combinations of existing assets and contributions.

These are funding options shown by Goal Planner.

Strategy Builder then deals with **how the feasible goal should actually be executed**.

---

## 20. Questions Created by Case 2

### Question 1 — Does Goal Planner need to create a second strategic decision layer after establishing feasibility?

**No.**

If the goal is already visible and Goal Planner has established that it is feasible, Goal Planner should provide the feasible funding requirement/options.

Strategy Builder should not repeat the same feasibility calculation.

---

### Question 2 — What is the role of Strategy Builder after feasibility?

Strategy Builder answers:

> **How should we execute the feasible goal without unnecessarily damaging the client's existing financial position?**

For example, an education goal may be feasible without liquidating the client's entire existing investment corpus.

A possible Strategy Builder decision could be:

> Use **Credit Utilisation** where appropriate, rather than immediately withdrawing productive assets and destroying years of compounding.

The Strategy Builder can then examine:

- education loan / credit utilisation;
- amount financed;
- repayment structure;
- EMI impact;
- existing asset preservation;
- future compounding;
- repayment capacity;
- overall long-term financial effect.

This is a strategy/execution question, not a Goal Funding feasibility question.

---

## 21. The Important Insight from Case 2

Case 2 clarified that **Goal Funding and Strategy Builder should not compete for the same decision**.

The separation is:

| Layer | Question | Output |
|---|---|---|
| Goal Planner / Goal Funding | Is the goal feasible? How can it be funded? | Feasibility + funding options |
| Strategy Builder | How should the feasible plan be executed? | Strategy + variant + techniques + architecture + execution |

Therefore:

> **Goal Funding is not another Strategy Builder strategy.**

For example, SIP or lump sum can be displayed as funding options by Goal Planner, while Credit Utilisation can be selected by Strategy Builder when financing the goal is economically preferable to liquidating productive assets.

---

# 22. New Finding from Case 1 + Case 2: Money Wheel Should Measure, Not Decide

The combined discussion of Case 1 and Case 2 produced another important system-level finding.

The **Money Wheel** should contain financial measurements and indicators.

It should not itself make the final financial planning decision through generic hard thresholds.

For example:

> DTI = 37%

is a measurement.

But:

> DTI > X% → automatically repay debt / stop investing

is a planning decision.

That decision belongs to the appropriate Goal Planner / Goal Feasibility analysis, where the actual goal, debt economics, cash flow and alternatives can be considered together.

---

## 23. New Debt Measurements Identified

The discussion identified the need for a new measurement family for debt economics.

### 23.1 Weighted Debt Rate

When a client has multiple loans, a simple average of interest rates is misleading.

The proposed measurement is:

**Weighted Debt Rate**

= Sum of (Outstanding Loan Principal × Loan Interest Rate)  
÷ Total Outstanding Loan Principal

This gives a single measurement of the approximate interest-rate cost of the client's outstanding debt portfolio.

Example:

| Loan | Outstanding | Interest Rate |
|---|---:|---:|
| Home loan | ₹50 lakh | 8% |
| Personal loan | ₹5 lakh | 18% |
| Car loan | ₹10 lakh | 10% |

The weighted rate gives more weight to the large home loan than to the smaller personal loan.

---

### 23.2 Investment–Debt Spread

A second useful measurement emerged from the discussion:

**Investment–Debt Spread**

= Relevant Investment Return Assumption − Weighted Debt Rate

This measurement answers:

> **Is the return expected from deploying additional capital higher or lower than the cost of carrying the debt?**

For example:

- Investment return assumption = 12%
- Weighted debt rate = 9.23%
- Spread = +2.77 percentage points

This does **not** mean investing is automatically better.

The investment return must be treated as a scenario/risk-adjusted assumption, not a guaranteed return.

Similarly, a negative spread should trigger deeper debt-vs-investment analysis rather than an automatic universal rule.

---

## 24. What Happens to DTI and Other Money Wheel Ratios?

The discussion established a change in philosophy:

> **Existing Money Wheel ratios should remain measurements, but their generic hard decision thresholds should not be used as automatic planning gates.**

For example:

**DTI**

should report the actual DTI.

It should not independently conclude:

> “DTI above the threshold = repay debt.”

Instead, Goal Planner should interpret DTI together with:

- loan interest rate;
- outstanding principal;
- remaining tenure;
- EMI;
- monthly surplus;
- goal horizon;
- goal funding requirement;
- liquidity;
- investment opportunity;
- repayment alternatives.

The same principle applies to other Money Wheel ratios: their calculation remains useful, but the generic ratio threshold should not silently become the financial decision.

---

# 25. Revised Responsibility of the Money Wheel

The resulting conceptual boundary is:

```
FINANCIAL STATE
      ↓
MONEY WHEEL
      ↓
Financial Measurements
      ↓
Debt Metrics
      ↓
Goal Planner / Goal Feasibility
      ↓
Contextual Interpretation
      ↓
Goal Funding / Feasibility
      ↓
Strategy Builder
      ↓
Strategy & Execution
```

### Money Wheel

**Measures.**

### Goal Planner

**Interprets those measurements in the context of the goal and determines feasibility/funding.**

### Strategy Builder

**Determines how the feasible plan should be executed.**

---

# 26. What Case 2 Added to the System Design

| Question / Finding | Decision |
|---|---|
| Should Goal Planner and Strategy Builder both calculate feasibility? | **No** |
| Once a goal is feasible, should Goal Planner show funding options? | **Yes** |
| Are SIP/lump sum/step-up mechanisms themselves Strategy Builder strategies? | **No** |
| Can Strategy Builder use Credit Utilisation for an education goal? | **Yes, where the economics support it** |
| Should productive assets automatically be liquidated to fund a goal? | **No** |
| Should Money Wheel make the final debt/investment decision? | **No** |
| Should Money Wheel display DTI and other ratios? | **Yes** |
| Should generic hard thresholds in Money Wheel automatically decide planning actions? | **No** |
| Is a weighted debt-rate measurement useful? | **Yes — candidate canonical measurement** |
| Is Investment–Debt Spread useful? | **Yes — candidate canonical measurement** |
| Are these new measurements finalised in code? | **No** |
| Are the exact Money Wheel thresholds/decision rules frozen? | **No** |

---

# 27. Combined Learning from Case 1 and Case 2

The two cases now establish a clearer architecture:

> **Money Wheel tells us what the financial condition looks like.**

> **Goal Planner tells us whether the goal is feasible and what funding options can make it feasible.**

> **Strategy Builder tells us how to execute that feasible goal without unnecessarily destroying the client's existing financial position.**

And the key principle emerging from both cases is:

> **A financial ratio is a measurement. It should not automatically become a financial decision rule merely because a generic threshold has been assigned to it.**

The actual decision should be made after considering the client's goal, debt economics, cash flow, liquidity, opportunity cost and available alternatives.

---

## Updated Change Status

| Item | Status |
|---|---|
| Case 1 — Debt / goal feasibility | **Documented** |
| Case 2 — Feasible education goal / strategy execution | **Documented** |
| Goal Planner → Strategy Builder boundary | **Further clarified** |
| Money Wheel as measurement layer | **Business direction established** |
| Generic Money Wheel hard thresholds as automatic decision gates | **Rejected as the planning decision mechanism** |
| Weighted Debt Rate | **Candidate new canonical measurement** |
| Investment–Debt Spread | **Candidate new canonical measurement** |
| Debt economics as Goal Planner input | **Business direction established** |
| Credit Utilisation as Strategy Builder strategy | **Validated as a possible execution path** |
| Implementation changes | **Not made** |
| Exact formulas/thresholds | **Not yet frozen** |
| Next phase | **Continue real-life case validation before implementation** |
