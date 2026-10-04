# 2. Goal Funding — Dependency Graph

```text
USER
  │
  │ chooses / updates a goal
  ▼
GOAL
  │
  ├── what is the goal?
  ├── when is it needed?
  └── how much is needed?
          │
          ▼
HOW MUCH IS ALREADY FUNDED?
          │
          ├── Shortfall
          ├── On Track
          └── Overfunded
          │
          ▼
AVAILABLE MONEY
          │
          ▼
CAN THIS GOAL BE FUNDED?
          │
          ├── yes ───────► strategy options
          │
          └── limited ──► changes / conditions needed
                                  │
                                  ▼
                               USER
```
