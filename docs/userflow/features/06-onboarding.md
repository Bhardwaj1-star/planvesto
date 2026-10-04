# Onboarding

## Purpose

Onboarding collects, validates and persists the user's core financial information and creates the **single financial picture** used by the rest of Planvesto.

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
  ├── Insurance
  ├── Liabilities
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
| Insurance | Financial protection and related commitments/value |
| Liabilities | Financial obligations |
| Goals | What the user wants to achieve |

## Core System Rules

1. **One user → one consistent Financial Picture.**
2. Onboarding **collects, validates and persists** financial data.
3. Onboarding does not analyse financial health, determine goal feasibility, or choose strategies.
4. Income, expenses, assets, liabilities and insurance contribute to the same financial picture.
5. Goals describe the user's objectives; the system determines feasibility and strategy later.
6. Goal meaning must remain consistent across the entire system.
7. **Retirement and Financial Independence are separate goals.**
8. A beneficiary or circumstance such as a child does not automatically create a separate goal category.
9. Financial Measures, Goal Planner, MoneyWheel and Strategy must use the same underlying financial picture.
10. Insurance is a dedicated onboarding step between Assets and Liabilities and uses the existing Insurance functionality.

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
