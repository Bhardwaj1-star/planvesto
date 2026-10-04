# 1. Financial Picture — Dependency Graph

```text
USER
  │
  │ enters income, expenses, assets, debts
  ▼
FINANCIAL PICTURE
  │
  ├── income
  ├── expenses
  ├── assets
  └── debts
        │
        ▼
CURRENT FINANCIAL STATE
        │
        ▼
FINANCIAL MEASURES
        │
        ├── savings position
        ├── debt position
        ├── liquidity position
        └── emergency coverage
                │
                ▼
        PLANNING DECISIONS
                │
        ┌───────┴────────┐
        ▼                ▼
     GOALS           CONSTRAINTS
        │                │
        └───────┬────────┘
                ▼
             STRATEGY
                │
                ▼
               USER
```
