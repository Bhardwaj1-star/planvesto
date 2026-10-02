# Participate With Your Numbers — Decision Workspace Design

## 1. Purpose

**Participate With Your Numbers** is the investor-facing decision workspace that sits between **Strategy Selection** and the **Final Investor Decision**.

Its purpose is to let the investor interact with the selected strategy using their own financial numbers, explore possible changes, understand outcomes and trade-offs, and make a better-informed final decision.

The system calculates and explains.

**The investor participates.  
The investor decides.**

---

## 2. Position in the Financial Decision Engine

The complete decision flow is:

**WHERE AM I?**
→ Financial State

**WHERE DO I WANT TO GO?**
→ Goals

**WHAT CAN / CANNOT CHANGE?**
→ Constraints

**WHAT AM I CONSIDERING?**
→ Action / Problem

**WHAT POSSIBLE PATHS EXIST?**
→ Strategy Engine

**WHAT DOES EACH PATH PRODUCE?**
→ Calculation Engine

**STRATEGY SELECTED**
→ Investor enters the Participate With Your Numbers workspace

**WHAT IF CONDITIONS CHANGE?**
→ Scenario Engine

**HOW LIKELY / UNCERTAIN ARE THE OUTCOMES?**
→ Probability Engine

**WHICH PATH FITS BEST?**
→ Optimization Engine

**WHY?**
→ Explainability Engine

**WHAT DO I CHOOSE?**
→ Investor Decision

**WHAT CHANGED?**
→ Updated Financial State

The workspace therefore does not replace the Strategy Engine. It is the interactive decision layer that follows strategy selection and precedes final investor choice.

---

## 3. Core Product Principle

### Participate With Your Numbers

The investor should not receive a strategy as a static answer.

After selecting a strategy, the investor should be able to ask:

- What happens if I change my contribution?
- What happens if my income changes?
- What happens if expenses increase?
- What happens if the goal timeline changes?
- What happens if the expected return changes?
- What happens if another relevant strategy parameter changes?

The workspace recalculates the resulting outcomes and shows the resulting trade-offs.

The purpose is not to let the investor arbitrarily manipulate the model.

The purpose is to let the investor **participate in the decision using their own numbers**.

---

## 4. The Fundamental Boundary: Constraints

**Constraints are the boundary of the workspace.**

The investor can explore within the feasible financial space defined by the Financial State, Goals, and Constraints.

Conceptually:

**Constraints**
→ define what can / cannot change

**Workspace**
→ explores what happens within those boundaries

This prevents the workspace from becoming an unrealistic calculator where any arbitrary number produces a seemingly valid outcome.

### Example

If the investor wants to increase a monthly contribution:

**Feasible**
→ the workspace recalculates the strategy and outcomes.

**Not feasible under the defined constraints**
→ the workspace must explicitly identify the violated constraint.

It must not silently treat an infeasible value as a realistic recommendation.

---

## 5. Workspace Inputs

The workspace should expose only the variables that are relevant to the selected strategy.

Possible examples include:

- monthly contribution
- contribution step-up
- existing corpus
- goal timeline
- goal amount
- expected return
- income
- expenses
- other strategy-specific parameters

Not every strategy will expose every variable.

### Rule

**Strategy determines the available parameters.  
Constraints determine their feasible range.**

The workspace should not expose arbitrary financial variables simply because they exist in the Financial State.

---

## 6. Three Engines Become One Investor Workspace

The workspace combines three analytical engines:

### A. Scenario Engine

Answers:

> **What happens if conditions change?**

It evaluates the selected strategy under alternative assumptions or parameter values.

Examples:

- contribution increases/decreases
- goal date changes
- return assumption changes
- income changes
- expense changes

Output:
**scenario outcomes**

---

### B. Probability Engine

Answers:

> **How likely / uncertain are the outcomes?**

It adds uncertainty to the scenario results where the underlying model supports probabilistic analysis.

Output may include:

- probability of goal achievement
- outcome ranges
- uncertainty bands
- probability-adjusted results

The Probability Engine must not create false precision. If the available model/data cannot support a probability estimate, the system should state that probability is unavailable rather than inventing one.

---

### C. Optimization Engine

Answers:

> **Which feasible path fits best under the defined objectives and constraints?**

Optimization operates inside the constraint boundary.

It can identify:

- feasible combinations
- trade-offs
- efficient alternatives
- parameter combinations that improve specified objectives

Optimization is **not** the final investor decision.

It should not turn the system into an autonomous decision-maker.

---

## 7. Relationship Between the Three Engines

They are analytically separate but presented to the investor as one workspace.

### Scenario

**Change the number → see what happens.**

### Probability

**Understand uncertainty around what happens.**

### Optimization

**Understand which feasible combinations satisfy the defined objectives/trade-offs better.**

Together:

**Scenario + Probability + Optimization**
→ **Participate With Your Numbers Workspace**

---

## 8. Workspace Interaction Model

The investor enters the workspace only after a strategy has been selected.

### Step 1 — Strategy Selected

The Strategy Engine has generated possible strategies.

The investor selects a strategy to explore.

### Step 2 — Strategy Baseline

The workspace loads:

- selected strategy
- current Financial State
- relevant Goal
- applicable Constraints
- strategy parameters
- baseline assumptions
- baseline calculated outcome

This baseline becomes the reference point.

### Step 3 — Participate

The investor changes one or more permitted parameters.

Example:

**Monthly contribution**
₹50,000 → ₹65,000

The system recalculates the strategy.

### Step 4 — Compare

The workspace shows:

- baseline
- changed case
- outcome difference
- trade-offs
- constraint impact
- uncertainty/probability where available

### Step 5 — Explore

The investor can test multiple feasible combinations.

### Step 6 — Decide

The investor chooses the path they are comfortable with.

---

## 9. What the Investor Should See

The workspace should answer:

### “What changed?”

For every meaningful interaction, show the effect of the change.

Examples:

- Goal funding ↑
- Required return ↓
- Monthly surplus ↓
- Safety buffer ↓
- Probability of achievement ↑
- Time to goal changed
- Funding gap reduced

The workspace should emphasize **cause → effect**, not just updated numbers.

---

## 10. Trade-Off Model

Financial decisions rarely improve every dimension simultaneously.

Therefore the workspace must surface trade-offs.

Example:

Increasing monthly investment may:

**Improve**
- future goal funding
- required return

But may:

**Reduce**
- monthly surplus
- liquidity
- emergency flexibility

The system should show both sides.

It must not label the result as universally “better” simply because one goal metric improved.

---

## 11. Constraint Handling

Constraints must be explicit.

Each workspace parameter should have:

- current value
- allowed range, where applicable
- constraint source
- constraint status

When a user moves outside a feasible boundary:

### Option A — Prevent the invalid state

Do not allow the parameter to move beyond the boundary.

### Option B — Show an explicit violation

Allow exploration but clearly mark:

**Constraint violated**

and identify which constraint was violated.

The implementation choice between A and B is a product/UI decision. The core rule is fixed:

> **The system must never present a constraint-violating scenario as a normal feasible path.**

---

## 12. Explainability

The workspace must preserve the reasoning chain.

For every material outcome, the system should be able to explain:

**Input changed**
→ **Calculation changed**
→ **Scenario changed**
→ **Outcome changed**
→ **Trade-off changed**
→ **Decision implication**

Example:

**Contribution increased**
→ higher future contributions
→ higher projected corpus
→ lower funding gap
→ lower required return
→ lower current monthly surplus
→ reduced cash-flow flexibility

This is the explanation the investor needs before making a decision.

---

## 13. Optimization Boundary

Optimization must remain subordinate to investor agency.

It should answer:

> “Within your constraints and stated objectives, these are the feasible trade-offs and combinations.”

It should not answer:

> “This is what you must choose.”

The final selection remains:

**Investor Decision**

---

## 14. Final Decision

The workspace culminates in a decision state.

The investor should be able to choose:

- selected strategy
- selected parameter values
- selected assumptions
- accepted trade-offs

The system records the decision context so that the resulting financial state can be updated correctly.

---

## 15. Updated Financial State

After the investor makes the decision:

**Investor Decision**
→ implementation/action
→ updated financial data
→ updated Financial State

The decision loop then begins again.

This creates the closed loop:

**Financial State**
→ Goals
→ Constraints
→ Problem
→ Strategy
→ Participate With Your Numbers
→ Investor Decision
→ Updated Financial State
→ **repeat**

---

## 16. Separation of Responsibilities

### Financial State
Describes where the investor is.

### Goals
Define where the investor wants to go.

### Constraints
Define the boundaries.

### Strategy Engine
Generates possible paths.

### Calculation Engine
Calculates what each path produces.

### Scenario Engine
Tests changed conditions.

### Probability Engine
Evaluates uncertainty/likelihood where supported.

### Optimization Engine
Analyzes feasible trade-offs and combinations.

### Explainability Engine
Explains the reasoning and effects.

### Participate With Your Numbers
Combines the analytical outputs into an interactive investor decision workspace.

### Investor Decision
The investor chooses.

### Updated Financial State
Records the resulting financial reality.

---

## 17. What This Workspace Is Not

It is not:

- a generic financial calculator
- an unrestricted simulation sandbox
- a replacement for the Strategy Engine
- an autonomous recommendation engine
- an optimization black box
- a portfolio trading interface
- a mechanism for forcing the investor into a system-selected answer

---

## 18. Product Philosophy

The workspace implements a core Planvesto principle:

> **The system should not make the investor passive.**

The investor should be able to see how their own numbers affect the decision.

Therefore:

**System calculates.  
System explains.  
Investor participates.  
Investor evaluates trade-offs.  
Investor decides.**

---

## 19. Final Architecture

**Financial Data**
↓
**Financial State**
↓
**Financial Context**
↓
**Goals**
↓
**Constraints**
↓
**Action / Problem**
↓
**Strategy Engine**
↓
**Strategy Selected**
↓
### **PARTICIPATE WITH YOUR NUMBERS**
**Scenario Engine + Probability Engine + Optimization Engine**
↓
**Outcomes + Uncertainty + Trade-offs + Explainability**
↓
**Investor Decision**
↓
**Updated Financial State**
↓
**↻**

### Core Design Rule

**Constraints define the boundary.  
The workspace enables exploration.  
The engines calculate the consequences.  
The investor makes the decision.**
