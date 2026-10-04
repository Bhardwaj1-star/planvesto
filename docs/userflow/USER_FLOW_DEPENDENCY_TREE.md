# Planvesto User Flow Dependency Tree

```text
USER
└── Financial Picture
    └── Financial State
        ├── Goals
        │   └── Goal Funding
        │       └── Feasibility
        │           └── Strategy Options
        │               └── User Selection
        │                   └── Strategy Version
        │                       └── Approval
        │                           └── Actions
        │                               └── Actual Financial Change
        │                                   └── Financial State
        │
        └── Constraints
            └── Strategy Evaluation


USER
└── Goal Change
    └── New Goal Version
        └── New Strategy Evaluation
            └── New Strategy Version
                └── New Approval
                    └── New Actions

Old Strategy Version
└── History

New Strategy Version
└── Current Plan
```
