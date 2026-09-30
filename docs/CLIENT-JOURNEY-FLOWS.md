# Planvesto — Client Journey & Core User Flows

## Purpose

This document defines Planvesto from the **client's point of view**. It is the product-level flow above the backend implementation.

The client should experience a simple journey; the financial engines remain behind the scenes.

---

## 1. Master Client Journey

```text
Client Onboarding
      ↓
Financial State
      ↓
Client Intent / Goals
      ↓
Goal Definition
      ↓
Goal Feasibility
      ↓
Financial Constraints & Trade-offs
      ↓
Strategy Building
      ↓
Multi-Goal Planning
      ↓
Resource Allocation
      ↓
Final Financial Plan
      ↓
Action Plan
      ↓
Report / PDF
      ↓
Ongoing Review
```

This is the primary client journey. Individual product journeys branch from it.

---

# 2. Core Client Journeys

## Journey A — New Client / Financial Discovery

**Purpose:** Understand the person before making financial decisions.

```text
Start
 ↓
Personal Information
 ↓
Family & Dependents
 ↓
Income
 ↓
Expenses
 ↓
Assets
 ↓
Liabilities
 ↓
Financial State
 ↓
Financial Health / Ratios
 ↓
Discovery Complete
```

### Client outcome
The client gets a structured picture of their current financial position.

### System outcome
A usable Financial State is created for downstream planning.

---

## Journey B — Goal Creation

**Purpose:** Convert what the client wants into a defined financial goal.

```text
What do you want to achieve?
 ↓
Goal Type
 ↓
Goal Amount / Today's Cost
 ↓
Target Date
 ↓
Priority
 ↓
Flexibility
 ↓
Existing Assets / Funding Sources
 ↓
Goal Definition
 ↓
Defined Goal
```

A goal remains independently identifiable and auditable.

---

## Journey C — Goal Feasibility

**Purpose:** Determine whether the goal is financially achievable under the current state.

```text
Defined Goal
 ↓
Future Target
 ↓
Existing Asset Contribution
 ↓
Required Contribution
 ↓
Available Surplus
 ↓
Funding Gap / Surplus
 ↓
Feasible / Partially Feasible / Infeasible
```

### Client outcome
The client understands **whether the goal fits the current financial reality** before choosing products.

---

## Journey D — Single Goal Planning

**Purpose:** Build a strategy for one specific goal.

```text
Financial State
 ↓
Selected Goal
 ↓
Constraints
 ↓
Eligible Strategies
 ↓
Strategy Evaluation
 ↓
Strategy Selection
 ↓
Goal Strategy Result
 ↓
Goal Action Plan
 ↓
Goal Report / PDF
```

This is separate from the consolidated multi-goal plan.

---

## Journey E — Multi-Goal Planning

**Purpose:** Solve competing goals using the same financial resources.

```text
Multiple Goals
 ↓
Individual Goal Results
 ↓
Priorities + Constraints
 ↓
Available Resources
 ↓
Resource Competition
 ↓
Allocation
 ↓
Trade-offs
 ↓
Resolved Goal Plans
 ↓
Consolidated Financial Plan
```

The system must never silently allocate more resources than the investor has available.

---

## Journey F — Goal Basket Planning

**Purpose:** Group related goals for planning without merging their identities.

```text
Client Intent
 ↓
Goal Basket
 ↓
Individual Goals
 ↓
Defined Goals
 ↓
Individual Strategy
 ↓
Collective Resource Planning
 ↓
Trade-offs
 ↓
Financial Plan
```

A Basket is a **planning group**, not a goal and not a strategy.

Examples:
- Family Security
- Wealth Creation
- Home & Lifestyle
- Child Future
- Retirement

---

## Journey G — Home Planning

**Purpose:** Dedicated planning journey for purchasing/building a home.

```text
Onboarding
 ↓
Home Goal
 ↓
Property Cost
 ↓
Purchase Timeline
 ↓
Down Payment / Own Contribution
 ↓
Existing Assets
 ↓
Loan Requirement
 ↓
EMI / Affordability
 ↓
Investment / Funding Strategy
 ↓
Stress Test
 ↓
Home Plan
 ↓
Action Plan
 ↓
Home Planning PDF
```

### Important
Home Planning should remain a **goal-specific journey**, while its final funding requirements participate in the broader Multi-Goal Plan.

---

## Journey H — Retirement Planning

**Purpose:** Plan long-term financial independence.

```text
Onboarding
 ↓
Retirement Goal
 ↓
Current Lifestyle Cost
 ↓
Retirement Timeline
 ↓
Inflation / Future Requirement
 ↓
Existing Retirement Assets
 ↓
Required Corpus
 ↓
Funding Strategy
 ↓
Accumulation Plan
 ↓
Retirement Action Plan
 ↓
Retirement Report
```

---

## Journey I — Child Education / Major Future Goal

**Purpose:** Plan a large future expenditure with a defined timeline.

```text
Goal Creation
 ↓
Today's Cost
 ↓
Inflation / Future Cost
 ↓
Target Date
 ↓
Existing Funding
 ↓
Funding Gap
 ↓
Strategy
 ↓
Contribution Plan
 ↓
Goal Report
```

This should use the same core goal architecture rather than creating a separate calculation system.

---

## Journey J — Financial Health / Stabilisation

**Purpose:** Help a client become financially ready before aggressive goal funding.

```text
Financial State
 ↓
Health Ratios
 ↓
Emergency Reserve
 ↓
Debt Burden
 ↓
Savings Capacity
 ↓
Liquidity Position
 ↓
Financial Health Findings
 ↓
Prerequisite Actions
 ↓
Goal Planning Readiness
```

This journey is especially important when the client's current financial state makes discretionary goals unsafe or difficult to fund.

---

## Journey K — Strategy Review / Decision Review

**Purpose:** Let the client understand why the system produced a particular plan.

```text
Final Strategy
 ↓
Assumptions
 ↓
Constraints
 ↓
Alternatives Considered
 ↓
Trade-offs
 ↓
Resolved Outcome
 ↓
Why This Plan
```

The system should distinguish:
- Client-selected priority
- System-resolved outcome
- Reason for any difference

---

## Journey L — Final Financial Plan & PDF

**Purpose:** Convert the finalized planning result into a client-readable output.

```text
Finalized Financial Plan
 ↓
Plan Summary
 ↓
Goal-by-Goal Outcomes
 ↓
Funding / Allocation
 ↓
Constraints
 ↓
Trade-offs
 ↓
Required Actions
 ↓
PDF
```

The report/PDF must consume the finalized plan. It must not independently recalculate the financial plan.

---

## Journey M — Ongoing Review / Replanning

**Purpose:** Financial plans are not one-time calculations.

```text
Existing Plan
 ↓
New Income / Expense / Asset / Liability / Goal Data
 ↓
Financial State Updated
 ↓
Goal Impact Check
 ↓
Strategy Re-evaluation
 ↓
Resource Reallocation
 ↓
Updated Financial Plan
 ↓
Updated Action Plan / PDF
```

Recommended triggers:
- Major income change
- Major expense change
- New liability
- Major asset change
- Goal date/amount change
- Goal priority change
- Completion/cancellation of a goal

---

# 3. Recommended Product-Level Journey Map

| Journey | Core question answered | Output |
|---|---|---|
| Financial Discovery | "Meri current financial position kya hai?" | Financial State |
| Financial Health | "Meri financial condition kaisi hai?" | Health / Constraints |
| Goal Creation | "Mujhe kya achieve karna hai?" | Defined Goal |
| Goal Feasibility | "Kya main ise afford kar sakta hoon?" | Feasibility |
| Single Goal Planning | "Is goal ko kaise achieve karun?" | Goal Strategy |
| Multi-Goal Planning | "Mere saare goals ko saath kaise fund karun?" | Consolidated Plan |
| Goal Basket | "Kaunse goals ko saath plan karna hai?" | Planning Group |
| Home Planning | "Ghar kaise afford karun?" | Home Plan |
| Retirement Planning | "Financial independence kaise achieve karun?" | Retirement Plan |
| Major Future Goal | "Bade future expense ko kaise fund karun?" | Goal Plan |
| Strategy Review | "System ne ye plan kyun diya?" | Decision Explanation |
| Final Report | "Mera complete plan kya hai?" | PDF |
| Ongoing Review | "Situation badalne par plan kya hoga?" | Updated Plan |

---

# 4. Additional Journeys Worth Building

These are **candidate journeys**, not automatically approved features.

### A. Debt Resolution
```text
Debt Position → Burden → Priority → Repayment Strategy → Cash-flow Release → Re-plan Goals
```

### B. Emergency Fund Journey
```text
Current Liquidity → Required Reserve → Gap → Build-up Strategy → Safety Achieved
```

### C. Wealth Accumulation Journey
```text
Surplus → Long-term Objective → Capacity → Strategy → Portfolio Implementation → Review
```

### D. Life Event Planning
```text
Life Event → Financial Impact → New Goal(s) → Resource Requirement → Strategy → Plan
```

Examples: marriage, child, relocation, career break, business start.

### E. Goal Change / What-if Journey
```text
Change Goal Amount/Date → Recalculate → Funding Impact → Strategy Impact → Trade-off → Updated Plan
```

### F. Plan Health Check
```text
Existing Plan → Current Data → Actual vs Planned → Variance → Corrective Action
```

---

# 5. Rules for All Client Journeys

1. **Client journey must remain simpler than backend architecture.**
2. **Financial calculations happen in backend, not UI.**
3. **Goal ≠ Strategy ≠ Product.**
4. **Individual Goal Plan ≠ Consolidated Financial Plan.**
5. **Goal Basket ≠ Goal.**
6. **Client priority and system-resolved outcome must remain distinguishable.**
7. **No resource allocation may exceed available resources.**
8. **Reports consume finalized results; they do not create a second calculation path.**
9. **Every major decision must have an explainable reason.**
10. **A change in financial state should be capable of triggering replanning.**

---

# 6. Target End-State

```text
                         CLIENT
                           │
                    ┌──────▼──────┐
                    │  ONBOARDING │
                    └──────┬──────┘
                           ↓
                   FINANCIAL STATE
                           ↓
                 FINANCIAL HEALTH
                           ↓
                    CLIENT INTENT
                           ↓
                ┌──────────┴──────────┐
                ↓                     ↓
          GOAL JOURNEYS          LIFE EVENTS
                ↓                     ↓
          GOAL DEFINITION             ↓
                ↓                     ↓
          FEASIBILITY                 ↓
                └──────────┬──────────┘
                           ↓
                 STRATEGY PLANNING
                           ↓
                 MULTI-GOAL PLANNING
                           ↓
                RESOURCE ALLOCATION
                           ↓
                  TRADE-OFFS
                           ↓
                FINANCIAL PLAN
                           ↓
                  ACTION PLAN
                           ↓
                    REPORT / PDF
                           ↓
                    ONGOING REVIEW
                           ↺
```

## Status Convention

- **Existing / supported:** already represented in the current architecture/docs.
- **Planned:** logically required but implementation may be incomplete.
- **Candidate:** useful future journey requiring separate product/business approval.

This document is the client-journey layer; backend implementation documents remain the technical source of truth for implementation details.