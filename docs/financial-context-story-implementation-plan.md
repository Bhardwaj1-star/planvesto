# Financial Context & Personalized Story — Implementation Plan

## 1. Objective

Build the layer that converts the investor's raw financial data into a structured, personalized financial context and then into an explainable financial story.

Core flow:

**6 Primary Financial Objects → Financial State → Ratios + Rules → Financial Context → Personalized Financial Story → Financial Priorities → Strategy Engine**

This layer is not a recommendation engine. It explains the investor's current financial situation and identifies the constraints/context that the Strategy Engine should use.

---

## 2. Primary Inputs

The system starts from six primary financial objects:

1. **Income** — cash inflow / earning capacity
2. **Expenses** — cash consumption / lifestyle cost
3. **Assets** — owned economic resources
4. **Liabilities** — financial obligations
5. **Insurance** — risk-transfer/protection position
6. **Goals** — future financial requirements

Do not introduce new primary financial objects for this layer unless a business decision explicitly requires them.

---

## 3. MoneyWheel Metrics

### Cash Flow
- **Savings Rate**
  - Context: current surplus/cash-flow capacity.

### Liquidity
- **Liquid Asset Ratio**
  - Context: proportion of total assets that is readily accessible.

### Debt
- **Debt-to-Income Ratio (DTI)**
  - Context: income burden created by debt servicing.
- **Leverage Ratio**
  - Context: debt weight relative to total assets.

### Wealth
- **Financial Asset Ratio**
  - Context: proportion of total assets held as financial assets.

### Insurance
- **Insurance Coverage Ratio**
  - Context: current protection relative to required protection.

### Goals
- **Goal Funding Ratio**
  - Context: current funding position of a goal.
- **Future Funding Ratio**
  - Context: projected funding position at the goal date.
- **Required Rate of Return**
  - Context: return required to bridge the goal funding requirement under the defined assumptions.

---

## 4. Coverage Rules

Coverage rules are diagnostics, not MoneyWheel spokes.

### Expense Coverage
**Liquid Assets / Monthly Expenses**

Answers:
> How many months of normal expenses can current liquid resources cover?

### Emergency Coverage
**Liquid Assets / Essential Monthly Expenses**

Answers:
> How many months of essential expenses can current liquid resources cover?

The existing emergency_fund_coverage implementation should not be treated as a final naming decision. Its expense basis must be explicitly defined so that Expense Coverage and Emergency Coverage remain distinct.

---

## 5. Financial Context Layer

The system must not interpret each ratio independently.

It should combine related signals into contextual dimensions.

### Context dimensions

**Cash-flow capacity**
- Savings Rate

**Liquidity / safety**
- Liquid Asset Ratio
- Expense Coverage
- Emergency Coverage

**Debt pressure**
- DTI
- Leverage

**Asset structure**
- Financial Asset Ratio
- Liquid Asset Ratio

**Protection**
- Insurance Coverage Ratio

**Goal position**
- Goal Funding Ratio
- Future Funding Ratio
- Required Rate of Return

The output of this layer is a structured context object, not prose.

Example:

cash_flow_context = constrained

liquidity_context = weak

debt_context = elevated

protection_context = undercovered

goal_context = underfunded_with_high_return_requirement

The exact status vocabulary and thresholds must be defined as explicit business rules, not inferred by the implementation.

---

## 6. Context Combination Rules

The important implementation principle is:

**Do not simply concatenate ratio statuses.**

The system must identify relationships between signals.

Example:

**Low Savings Rate + High DTI + Low Liquid Asset Ratio + Low Emergency Coverage**

should produce a higher-level context such as:

> **Financial flexibility is constrained.**

Another example:

**Low Future Funding Ratio + High Required Rate of Return**

should produce:

> **Goal feasibility is under pressure under the current funding path.**

Another:

**Low Insurance Coverage Ratio + High financial dependency/commitment exposure**

should produce:

> **Protection gap is material.**

These contextual conclusions must be generated from explicit rules.

---

## 7. Personalized Financial Story

The Financial Story is a human-readable interpretation of the structured context.

It should follow this order:

### A. Current Position
What is the investor's financial state?

### B. Primary Constraint
What is currently limiting financial flexibility or progress?

### C. Supporting Evidence
Which ratios/rules create that context?

### D. Goal Impact
How does the current state affect important goals?

### E. Financial Priorities
What financial problems need to be addressed before or alongside goal/investment decisions?

### F. Strategy Input
What constraints/context should be passed to the Strategy Engine?

Example structure:

> **Your current financial flexibility is constrained.** Your savings capacity is limited while debt servicing consumes a significant portion of income, and your liquid reserves provide a relatively small safety buffer. This also affects your goal trajectory: the current funding path is projected to leave a gap, increasing the return requirement. Your immediate financial priorities therefore relate to improving flexibility, strengthening safety reserves, and addressing the goal funding gap.

The story must be generated from structured context and evidence. It must never invent facts that are not present in the Financial State.

---

## 8. Financial Priorities

The story should lead to structured priorities, for example:

- improve cash-flow capacity
- strengthen liquidity/safety reserve
- reduce debt pressure
- improve protection
- improve goal funding
- reduce required return
- reassess goal timeline
- reassess contribution requirement

Priorities are **not yet strategies**.

A priority describes the problem to solve.

A strategy describes the architecture used to solve it.

---

## 9. Strategy Engine Boundary

This layer ends at:

**Financial Context + Financial Priorities + Evidence**

The Strategy Engine begins after that.

Example:

**Context**
- constrained cash flow
- high debt burden
- weak liquidity

↓

**Priority**
- improve financial flexibility

↓

**Strategy Engine**
- evaluates applicable debt/cash-flow/safety strategies
- generates strategy alternatives
- calculates scenarios
- validates feasibility
- produces explainable decision outputs

Do not hard-code a strategy directly into the ratio/story layer.

---

## 10. Implementation Components

Recommended backend separation:

### A. Ratio Calculator
Responsible only for calculating the approved MoneyWheel ratios.

### B. Coverage Rule Evaluator
Responsible for Expense Coverage and Emergency Coverage.

### C. Context Evaluator
Combines ratios and rules into structured financial contexts.

### D. Context Relationship Rules
Defines multi-signal relationships such as:
- low savings + high debt + weak liquidity
- weak future funding + high required return
- weak protection + high protection requirement

### E. Financial Story Generator
Converts structured context + evidence into explainable human-readable narrative.

### F. Priority Generator
Converts context into structured financial priorities.

### G. Strategy Input Adapter
Passes Financial Context and Priorities to the Strategy Engine without embedding strategy logic inside the context layer.

---

## 11. Explainability Requirements

Every contextual statement should be traceable to its underlying evidence.

Example:

financial_flexibility = constrained

Evidence:
- savings_rate = 8%
- dti = 42%
- liquid_asset_ratio = 5%
- emergency_coverage = 1.2 months

The system should be able to answer:

**Why did we say this?**

This is required for auditability and user trust.

---

## 12. Missing / Invalid Data

The system must distinguish:

- calculated
- unavailable
- insufficient_data
- not_applicable

Do not convert missing data into a negative status.

Example:

If required insurance cover is unavailable, do not assume Insurance Coverage Ratio = 0%.

If essential expenses are unavailable, Emergency Coverage should be unavailable rather than calculated from an invented value.

---

## 13. Implementation Sequence

### Phase 1 — Lock Definitions
- Finalize formulas.
- Finalize denominator definitions.
- Finalize required input fields.
- Finalize threshold/status vocabulary.

### Phase 2 — Ratio & Rule Layer
- Implement/align the 9 approved ratios.
- Implement Expense Coverage.
- Implement Emergency Coverage.
- Remove/retire overlapping MoneyWheel calculations from the decision output.

### Phase 3 — Context Rules
- Define single-signal context rules.
- Define multi-signal relationship rules.
- Define priority/severity handling.
- Add evidence references to every context result.

### Phase 4 — Story Layer
- Build deterministic story assembly from structured context.
- Ensure every sentence maps to available evidence.
- Support positive, neutral, constrained, and mixed financial states.

### Phase 5 — Strategy Boundary
- Convert context into Strategy Engine input.
- Keep strategy selection outside the story/context layer.
- Ensure the Strategy Engine receives constraints, priorities, and relevant evidence.

### Phase 6 — Validation
Test:
- healthy financial state
- high-income/high-debt state
- low-liquidity state
- underfunded-goal state
- high-required-return state
- mixed/contradictory signals
- missing data
- zero/edge values
- unavailable insurance/goal data

---

## 14. Non-Goals

This implementation does **not** include:

- frontend redesign
- frontend changes
- Supabase schema changes
- SQL migrations
- product selection
- portfolio construction
- investment recommendation logic
- strategy selection inside the MoneyWheel
- opaque AI-generated financial conclusions
- invented assumptions or missing values

---

## 15. Final Architecture

**Investor Data**

↓

**Financial State**

↓

**9 MoneyWheel Ratios + 2 Coverage Rules**

↓

**Financial Context Evaluator**

↓

**Relationship / Combination Rules**

↓

**Personalized Financial Story**

↓

**Financial Priorities + Evidence**

↓

**Strategy Engine**

↓

**Strategy Options → Calculations → Scenarios → Validation → Decision Output**

### Core Principle

**Numbers describe the financial state.  
Ratios describe individual dimensions.  
Rules identify conditions.  
Context connects the dimensions.  
Story explains the context.  
Priorities define what needs attention.  
Strategy solves the problem.**
