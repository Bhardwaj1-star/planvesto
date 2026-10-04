# 3. Strategy Choice — Dependency Graph

```text
USER
  │
  │ asks for a strategy
  ▼
GOAL + FINANCIAL SITUATION
  │
  ▼
POSSIBLE STRATEGIES
  │
  ├── goal fit
  ├── funding fit
  ├── risk fit
  ├── horizon fit
  └── other suitability checks
          │
          ▼
STRATEGY EVALUATION
          │
          ▼
RECOMMENDED OPTIONS
          │
          ▼
USER SELECTS ONE
          │
          ▼
CURRENT SELECTED STRATEGY
          │
          ▼
STRATEGY VERSION
          │
          ▼
READY FOR APPROVAL
```
