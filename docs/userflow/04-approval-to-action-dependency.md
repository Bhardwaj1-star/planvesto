# 4. Approval → Action — Dependency Graph

```text
USER
  │
  │ reviews selected strategy
  ▼
SELECTED STRATEGY
  │
  │ user approves
  ▼
APPROVED STRATEGY VERSION
  │
  ▼
ACTIONS
  │
  ├── what should the user do?
  ├── which strategy does it belong to?
  └── what result is expected?
          │
          ▼
USER COMPLETES ACTION
          │
          ▼
ACTUAL FINANCIAL CHANGE
          │
          ▼
CURRENT FINANCIAL STATE
          │
          ▼
NEXT PLANNING CYCLE
```
