# 5. Goal Change — Dependency Graph

```text
USER
  │
  │ changes an important part of the goal
  ▼
GOAL VERSION 1
  │
  ▼
STRATEGY VERSION 1
  │
  ▼
APPROVAL 1
  │
  ▼
ACTIONS 1
  │
  │
  └──────────────► HISTORY
                  
USER
  │
  │ new goal information
  ▼
GOAL VERSION 2
  │
  ▼
NEW STRATEGY EVALUATION
  │
  ▼
NEW STRATEGY VERSION
  │
  ▼
NEW APPROVAL
  │
  ▼
NEW ACTIONS
  │
  ▼
CURRENT PLAN

Old plan ─────────► stays as history
New plan ─────────► becomes current
```
