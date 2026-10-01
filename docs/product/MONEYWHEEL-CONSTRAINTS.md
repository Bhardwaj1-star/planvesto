# MoneyWheel — Financial Constraints

## Purpose

MoneyWheel is the **Financial Constraints Layer** of Planvesto.

It converts the investor's current financial state into measurable financial signals and identifies constraints that must be respected by the Strategy Engine.

MoneyWheel does **not** make the final financial decision and does not select products.

**Financial Inputs → Financial State → MoneyWheel Signals → Constraints → Strategy Engine**

## 1. Primary Financial Inputs

MoneyWheel is derived from six primary financial objects:

1. **Income** — recurring financial inflow.
2. **Expenses** — recurring consumption/outflow.
3. **Assets** — resources owned by the investor.
4. **Liabilities** — financial obligations owed by the investor.
5. **Insurance** — risk-transfer/protection arrangements.
6. **Goals** — future financial requirements with amount and time context.

These inputs are converted into Financial State before MoneyWheel evaluates constraints.

## 2. Final MoneyWheel Signals

The finalized MoneyWheel design contains **9 ratios + 2 coverage rules**.

### Cash Flow

#### 1. Savings Rate
**Context:** Cash-flow capacity.

Shows how much of current income remains available for future financial requirements after expenses.

**Potential constraint:** Limited cash-flow capacity.

### Liquidity

#### 2. Liquid Asset Ratio
**Context:** Liquidity position.

Shows the proportion of total assets that is readily accessible.

**Potential constraint:** Limited liquidity / weak accessible reserve.

### Debt

#### 3. Debt-to-Income Ratio (DTI)
**Context:** Debt-service burden.

Shows how much recurring income is committed to debt payments.

**Potential constraint:** Debt-service capacity constrained.

#### 4. Leverage Ratio
**Context:** Balance-sheet debt exposure.

Shows the proportion of total assets financed by liabilities.

**Potential constraint:** Balance-sheet leverage constraint.

> Solvency Ratio is not retained separately because it is mathematically derived from Leverage Ratio: Solvency = 1 − Leverage.

### Wealth

#### 5. Financial Asset Ratio
**Context:** Asset structure.

Shows how much of total assets is held in financial assets.

**Potential constraint:** Asset-structure constraint where relevant to the investor's goals and strategy.

### Insurance

#### 6. Insurance Coverage Ratio
**Context:** Protection position.

Shows existing insurance coverage relative to the required insurance cover.

**Potential constraint:** Protection gap.

### Goals

#### 7. Goal Funding Ratio
**Context:** Current goal position.

Shows how much of the goal target is already funded.

**Potential constraint:** Current funding gap.

#### 8. Future Funding Ratio
**Context:** Projected goal feasibility.

Shows how much of the future goal target is expected to be funded under the current/projected path.

**Potential constraint:** Future funding gap.

#### 9. Required Rate of Return
**Context:** Return requirement for goal feasibility.

Shows the annualized return required, given the goal amount, time horizon, existing goal funding and planned contributions.

**Potential constraint:** High return requirement / goal feasibility constraint.

## 3. Coverage Rules

Coverage rules are separate from MoneyWheel ratios.

### Expense Coverage

Formula: Liquid Assets ÷ Monthly Expenses

**Context:** How many months of normal expenses can current liquid assets cover?

**Constraint:** Expense safety / liquidity buffer constraint.

### Emergency Coverage

Formula: Liquid Assets ÷ Essential Monthly Expenses

**Context:** How many months of essential expenses can current liquid assets cover?

**Constraint:** Emergency safety constraint.

The distinction is intentional:

- Expense Coverage = normal spending resilience.
- Emergency Coverage = essential-survival resilience.

## 4. Constraint Model

A ratio is **evidence**.

A constraint is the **financial limitation inferred from that evidence**.

Example:

**Savings Rate = 8%**

does not itself become the user-facing conclusion.

Instead:

**Evidence:** Savings Rate = 8%  
**Context:** Low current surplus capacity  
**Constraint:** Limited cash-flow capacity

Similarly:

**DTI = 42%**

→ **Evidence:** High debt-service burden  
→ **Constraint:** Debt-service capacity is constrained

## 5. Constraint Categories

| Dimension | Primary signal | Constraint |
|---|---|---|
| Cash Flow | Savings Rate | Cash-flow capacity |
| Liquidity | Liquid Asset Ratio | Liquidity capacity |
| Debt Service | DTI | Debt-service capacity |
| Balance Sheet | Leverage | Leverage constraint |
| Asset Structure | Financial Asset Ratio | Asset-structure constraint |
| Protection | Insurance Coverage | Protection gap |
| Current Goal | Goal Funding Ratio | Current funding gap |
| Future Goal | Future Funding Ratio | Future funding gap |
| Goal Feasibility | Required Rate of Return | Return/feasibility constraint |
| Spending Safety | Expense Coverage | Expense safety |
| Emergency Safety | Emergency Coverage | Emergency safety |

## 6. Constraints Are Contextual, Not Isolated

MoneyWheel should not treat every ratio independently.

The Strategy Engine needs the **combined constraint context**.

Example:

- Low Savings Rate
- High DTI
- Low Liquid Asset Ratio
- Low Emergency Coverage
- Low Future Funding Ratio
- High Required Rate of Return

These signals together describe a different financial situation than any individual ratio alone.

The resulting context could be represented as:

> **Limited financial flexibility + high debt burden + weak safety buffer + underfunded goal + elevated return requirement.**

The exact narrative should be generated from the evaluated signals and relationships, not from a hard-coded generic paragraph.

## 7. Constraint Severity

Each constraint should ultimately be classified by its effect on planning.

### Hard Constraint
A condition that the Strategy Engine should not violate without an explicit, explainable override.

Examples:
- Critically inadequate emergency coverage.
- Debt burden beyond the approved ceiling.
- Other future business rules explicitly designated as non-negotiable.

### Soft Constraint
A condition that materially affects strategy selection but may be traded off.

Examples:
- Moderate liquidity weakness.
- Moderate savings-rate weakness.
- Elevated required return.

### Warning
A condition worth surfacing but not necessarily restrictive enough to alter the strategy by itself.

## 8. Constraint → Strategy Relationship

MoneyWheel does not answer:

> "What product should the investor buy?"

It answers:

> **"What financial constraints must the strategy solve or respect?"**

The Strategy Engine then uses those constraints together with:

- Investor priorities
- Goals
- Time horizons
- Financial State
- Available surplus
- Assets and liabilities
- Assumptions
- Other approved planning rules

to generate strategy options.

### Example

**MoneyWheel**

- Cash-flow constraint
- Debt-service constraint
- Emergency-safety constraint
- Goal-funding constraint

↓

**Strategy Engine**

Generate strategies that improve/operate within those constraints.

↓

**Calculation / Scenario Engine**

Evaluate the consequences of each strategy.

↓

**Decision Output**

Explain the trade-offs and proposed actions.

## 9. Personalized Financial Story

MoneyWheel should ultimately provide structured context for a personalized financial story.

The story is generated from **relationships between constraints**, not from simply listing ratios.

### Structure

**Current State**  
→ What is happening financially?

**Constraints**  
→ What is limiting the investor?

**Goal Impact**  
→ Which goals are affected and how?

**Trade-offs**  
→ What must be balanced or changed?

**Strategy Implication**  
→ What must a viable strategy solve?

Example:

> The investor has limited monthly surplus and a relatively high debt-service burden. Liquidity and emergency coverage are also weak. As a result, discretionary goal funding is constrained and the current path requires a relatively high return to meet the target.

This is the bridge from **MoneyWheel → Strategy Engine**.

## 10. Non-Goals

MoneyWheel is not:

- A portfolio recommendation engine.
- A mutual-fund/product selection engine.
- A risk-profile engine.
- A complete financial plan.
- A strategy generator.
- A final decision maker.

Those responsibilities belong to other layers of Planvesto.

## 11. Final Architecture

Investor  
↓  
6 Financial Objects  
↓  
Financial State  
↓  
MoneyWheel  
├── 9 Ratios  
└── 2 Coverage Rules  
↓  
Financial Constraints  
↓  
Personalized Financial Context  
↓  
Strategy Engine  
↓  
Strategy Options  
↓  
Calculation / Scenario Evaluation  
↓  
Decision + Action Plan

## 12. Implementation Status

The repository currently contains an earlier MoneyWheel implementation with 12 ratio definitions and an existing constraints evaluator.

The **final business design in this document supersedes that earlier ratio set conceptually**.

Implementation work should separately reconcile:

1. Ratio set
2. Ratio formulas
3. Classification thresholds
4. Coverage rules
5. Constraint severity
6. Goal-impact rules
7. Required Rate of Return calculation
8. MoneyWheel result schema
9. Strategy Engine input contract

No database schema or frontend change is implied by this document.

## Core Principle

> **MoneyWheel does not tell the investor what to do. It tells the Strategy Engine what constraints the investor's financial reality creates.**
