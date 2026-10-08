# Financial State Journey

**Document Type:** User Journey  
**Status:** CANONICAL DESIGN

## Journey

```
Current Financial Information → Income / Expenses / Assets / Liabilities
→ System validates & calculates → Financial State → Investor reviews
→ Correct / Update → Planning continues
```

## Investor Sees
- Income and expense position
- Existing assets
- Liabilities and debt obligations
- Available financial capacity
- Relevant planning indicators

## System Does
- Creates a current Financial State snapshot.
- Calculates derived planning values.
- Flags missing or inconsistent information.
- Keeps evidence separate from recommendations.

## Handoff

```
Financial State → Goal Planning / Strategy Decision / Impact Analysis
```

## Core Rule

Financial State is **evidence** used by downstream decisions. It is not itself a Strategy recommendation.
