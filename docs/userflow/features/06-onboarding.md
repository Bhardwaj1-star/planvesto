# Onboarding

## Purpose

Onboarding collects the user's core financial information and creates the **single financial picture** used by the rest of Planvesto.

## Flow

```text
User
  ↓
Onboarding
  ├── Personal Information
  ├── Family / Dependents
  ├── Income
  ├── Expenses
  ├── Assets
  ├── Liabilities
  ├── Insurance
  └── Goals
  ↓
Financial Picture
  ↓
Financial Measures
  ↓
Goal Planner / MoneyWheel / Strategy
```

## What Each Step Establishes

| Step | Establishes |
|---|---|
| Personal Information | User's planning context |
| Family / Dependents | People relevant to the plan |
| Income | Money coming in |
| Expenses | Money going out |
| Assets | Financial resources |
| Liabilities | Financial obligations |
| Insurance | Financial protection and related commitments/value |
| Goals | What the user wants to achieve |

## Core System Rules

1. **One user → one consistent Financial Picture.**
2. Onboarding **collects facts**; it does not decide financial health, goal feasibility, or strategy.
3. Income, expenses, assets, liabilities and insurance must contribute to the same financial picture.
4. Goals describe the user's objectives; the system determines feasibility and strategy later.
5. Goal meaning must remain consistent across the entire system.
6. **Retirement and Financial Independence are separate goals.**
7. A beneficiary or circumstance such as a child does not automatically create a separate goal category.
8. Financial Measures, Goal Planner, MoneyWheel and Strategy must use the same underlying financial picture.

## Insurance Correction

**Current problem:** Insurance is already implemented in the system but is missing from the guided onboarding flow.

**Required flow:**

```text
Liabilities
    ↓
Insurance
    ↓
Goals
```

Insurance must be a dedicated onboarding step and must use the existing Insurance functionality rather than creating a duplicate system.

## Final Contract

```text
Onboarding
    ↓
One Financial Picture
    ↓
Measure
    ↓
Plan Goals
    ↓
Build Strategy
```

**This document defines the business-level onboarding flow and decisions. Implementation details belong to the code.**
