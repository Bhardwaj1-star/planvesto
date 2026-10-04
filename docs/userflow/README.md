# Planvesto User Flow — Dependency Map

```text
USER
 │
 ├── 1. Financial Picture
 │      │
 │      └── Financial State
 │              │
 │              ▼
 │          Goals + Constraints
 │
 ├── 2. Goal Funding
 │      │
 │      └── Goal → Funding → Feasibility
 │
 ├── 3. Strategy Choice
 │      │
 │      └── Goal + Financial Situation
 │              ↓
 │          Strategy Options
 │              ↓
 │          User Selection
 │              ↓
 │          Strategy Version
 │
 ├── 4. Approval → Action
 │      │
 │      └── Strategy Version
 │              ↓
 │          Approval
 │              ↓
 │          Actions
 │              ↓
 │          Actual Financial Change
 │              ↓
 │          Financial State
 │
 └── 5. Goal Change
        │
        └── New Goal Version
                ↓
            New Strategy Version
                ↓
            New Approval
                ↓
            New Actions

OLD VERSION = HISTORY
NEW VERSION = CURRENT
```
