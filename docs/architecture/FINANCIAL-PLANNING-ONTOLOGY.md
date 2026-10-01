# Financial Planning Ontology — Core System
Status: LOCKED | Version: 1.0 | Branch: backend-audit-cleanup

## Purpose
This is the reference ontology and implementation boundary for Planvesto. It defines what the core entities mean, which engine owns each responsibility, how outputs flow, and where each engine stops.

## Core Questions
- MoneyWheel: Financially abhi kya ho raha hai?
- Risk Profiler: Investor ka investment risk structure kya hai?
- Goal Engine: Future mein kya accomplish karna hai, kab aur kitna?
- Investment Engine: Available capital ko kaise allocate/invest karna hai?

Core flow: Financial Data → Financial State → MoneyWheel / Risk Profiler / Goal Engine → Investment Engine → Investment Plan → Financial Plan → Report.
Strategy Builder is a separate problem-solving layer. It may consume relevant Goal, Financial Situation and Constraint context, but does not replace the four core engines.

## Core Entities
- Person / Household: financial planning subject.
- Financial State: current measurable financial position; Income, Expenses, Assets, Liabilities and Cash Flow.
- Goal: future financial objective requiring funding; includes type, timeline, target, funding, gap, priority and constraints.
- Risk Profile: Risk Capacity, Risk Tolerance, Investment Horizon, Investor Identity and Strategic Asset Allocation.
- Strategic Asset Allocation: portfolio-level asset-class structure produced by Risk Profiler. Exact percentages are business rules, not ontology.
- Investment Plan: Target Allocation, Current Allocation, Allocation Gap, Sub-Asset Allocation, Portfolio Structure and Implementation Allocation.
- Strategy: method for solving a specific financial problem; not a goal, allocation, portfolio, product or technique.
- Financial Situation: structured diagnosis of current financial position.
- Financial Plan: consolidated planning output.
- Report: presentation of Financial Plan; not an independent decision engine.

## MoneyWheel — LOCKED
Purpose: answer Financially abhi kya ho raha hai?
Role: Observe → Calculate → Diagnose → Explain.
Does not: select products, determine asset allocation, determine risk profile, select strategies, or construct portfolios.

### Inputs
Income: gross monthly income.
Expenses: monthly total expenses; monthly essential expenses.
Assets: total assets; liquid assets; financial assets.
Liabilities: total liabilities; monthly debt payments.
Insurance: existing sum assured; required insurance cover.
Goals: current funding; current target; projected funding; future target; duration.
Portfolio: asset-wise current holdings for concentration diagnostics.

### Core Metrics
1. Savings Rate = (Income − Expenses) / Income × 100.
2. Liquid Asset Ratio = Liquid Assets / Total Assets × 100.
3. Debt-to-Income Ratio = Monthly Debt Payments / Gross Monthly Income × 100.
4. Leverage Ratio = Total Liabilities / Total Assets × 100.
5. Financial Asset Ratio = Financial Assets / Total Assets × 100.
6. Insurance Coverage Ratio = Existing Sum Assured / Required Insurance Cover × 100.
7. Goal Funding Ratio = Current Goal Funding / Goal Target × 100.
8. Future Funding Ratio = Projected Goal Funding / Future Goal Target × 100.
9. Required Rate of Return = derived from current funding, future target and goal duration.

Required Rate of Return is mathematical evidence only; it does not directly create a product or investment recommendation.

### Coverage Metrics
Expense Coverage = Liquid Assets / Monthly Expenses. Unit: months.
Emergency Coverage = Liquid Assets / Essential Monthly Expenses. Unit: months.

### Metric Contract
Each metric exposes: Value, Unit, Status, Formula, Inputs Used, Availability and Data Quality.
Missing data must never be treated as zero. If required data is unavailable, the metric is unavailable and no conclusion is made from it.
Status categories: Excellent, Healthy, Attention, Critical. Status is evidence, not the final financial conclusion.

### Diagnostics
- Liquidity Constraint: Low Liquid Asset Ratio + High hard-asset concentration.
- Cashflow Pressure: High DTI + Low Savings Rate.
- Balance-Sheet Dependency: High Leverage + Low Financial Asset Ratio.
- Funding / Return Constraint: High Required Return + Low Goal Funding.
- Future Contribution Constraint: High Current Goal Funding + Low Future Funding.
Diagnostics are evidence-based financial diagnoses, not automatic strategy or product selections.

### Financial Situation
Organizes the diagnosis into Cashflow Position, Liquidity Position, Debt Position, Asset Structure, Protection Position and Goal Funding Position.

### Financial Story
A. Current Position
B. Primary Constraint
C. Supporting Evidence
D. Goal Impact
E. Financial Priorities
F. Strategy Input
Financial Priority ≠ Strategy.

### MoneyWheel Output
MoneyWheelResult = Metrics + Diagnostics + Financial Situation + Financial Story.

## Engine Boundaries
| Component | Owns | Does not own |
|---|---|---|
| Financial State | Current financial reality | Recommendations |
| MoneyWheel | Financial diagnosis | Investment decisions |
| Risk Profiler | Investment risk structure | Goal funding calculations |
| Goal Engine | Goal requirement and feasibility | Portfolio construction |
| Investment Engine | Capital allocation and implementation structure | Financial diagnosis |
| Strategy Builder | Specific financial problem solving | Generic portfolio construction |
| Product Selection | Actual financial products | Risk profiling |
| Financial Plan | Consolidated planning output | Raw calculation ownership |
| Report | Presentation | Decision logic |

## Implementation Rule
Ontology → Engine Contract → Business Rules → Calculations → Engine Output → Cross-Engine Integration → Financial Plan → Report.
Lower-level implementation details must not silently redefine ontology boundaries.

## Existing Repository Note
The repository already contains MoneyWheel rules, but the rules engine still references legacy keys such as emergency_fund_coverage and current_liquidity_ratio while the current MoneyWheel definitions use the newer metric/coverage names. This is an implementation mismatch to resolve later; it does not change the locked ontology.
No frontend redesign, database schema change, SQL migration, or git CLI operation is part of this document.

## Status
MoneyWheel Ontology: LOCKED.
Next ontology component: Risk Profiler.