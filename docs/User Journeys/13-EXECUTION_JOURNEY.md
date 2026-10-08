# Execution Journey

**Document Type:** User Journey  
**Status:** CANONICAL DESIGN

## Journey

```
Action Plan → Investor Executes Action → System Records Execution
→ Actual State Changes → Investor Reviews Result → Continue / Change
```

## Investor Does
- Executes or authorises planned actions.
- Records relevant actual outcomes.
- Reviews progress.

## System Does
- Tracks action status.
- Updates relevant financial / goal state.
- Identifies material deviations.
- Preserves planned vs actual execution.

## Core Rule

Execution changes the real financial state. Material execution changes can trigger Impact Analysis and targeted revalidation.
