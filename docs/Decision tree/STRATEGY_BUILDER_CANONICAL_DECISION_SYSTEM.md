# Strategy Builder — Canonical Decision System

## 1. Purpose

Define the canonical decision system for the Strategy Builder before refactoring implementation code.

This document separates:
- what is currently implemented,
- what must become canonical,
- what decisions still need to be frozen,
- and the sequence for refactoring.

## 2. Current Problem

The Strategy Builder rules are currently distributed across:
- `backend/rules/`
- `backend/library/strategies/`
- `backend/engines/rules/`
- `backend/engines/strategy/`

The main problem is **rule ownership is not consistently centralized**.

Canonical strategy/variant definitions exist, but several executable business rules remain inside engines:
- strategy applicability,
- eligibility/fit evaluation,
- strategy selection,
- variant selection.

There is also stale strategy-decision logic that does not match the current canonical 5-strategy set.

Therefore, refactoring should not start until the decision authority and rule ownership are frozen.

## 3. Current-State Rule Inventory

| Decision | Current implementation | Current issue | Target authority |
|---|---|---|---|
| Goal classification | `backend/rules/goals.py` | Mostly centralized | Keep canonical |
| Strategy definitions | `backend/library/strategies/canonical.py` | Definitions are centralized; interpretation is elsewhere | Keep canonical |
| Strategy variants | `backend/library/strategies/variants.py` | 22 variants are defined, but selection rules are in engine code | Keep definitions; centralize selection rules |
| Strategy applicability | `backend/engines/rules/engine.py` | Applicability signals/thresholds are executable engine logic | Canonical strategy-applicability rules |
| Eligibility / 8 fits | `backend/rules/eligibility.py` + `backend/engines/strategy/eligibility.py` | Vocabulary is centralized, business thresholds/logic are not | Canonical strategy-eligibility rules |
| Hard constraints | `backend/engines/constraints/` | Relatively centralized, but ownership must be frozen | Confirm canonical constraint authority |
| Strategy selection | `backend/engines/strategy/decision.py` | Actual selection authority lives in engine | Canonical strategy-selection rules |
| Ranking | `backend/engines/strategy/ranking.py` | DecisionResult is authoritative, but eligibility is evaluated again | Keep as execution/evidence layer after authority is frozen |
| Variant selection | `backend/engines/strategy/variant_selector.py` | Hardcoded executable selection rules | Canonical variant-selection rules |
| Technique selection | Strategy/library + engine flow | Exact authority needs to be frozen | Canonical technique-selection policy |
| Architecture composition | `backend/engines/strategy/` + strategy library | Rule ownership needs to be explicit | Canonical architecture policy |
| Stress testing | Existing what-if capability, but no verified canonical stress-rule framework | No single canonical authority verified | Define canonical stress policy |

## 4. Canonical Decision Tree

The intended Strategy Builder decision sequence is:

```text
Goal
  ↓
Goal Classification
  ↓
Strategy Applicability
  ↓
Hard Constraints
  ↓
Eligibility / 8 Fits
  ↓
PASS / CONDITIONAL / FAIL
  ↓
Strategy Selection
  ↓
Variant Selection (22 active variants)
  ↓
Technique Selection
  ↓
Architecture Composition
  ↓
Stress Test
  ↓
Resilience / Re-selection
  ↓
Final Recommendation
```

Each stage must have one authoritative rule owner and a defined input/output contract.

## 5. Canonical Rule Ownership

The target architecture is to move business-decision authority into canonical rule modules under `backend/rules/`.

Proposed ownership:

```text
backend/rules/
├── goals.py
├── strategy_applicability.py
├── strategy_eligibility.py
├── strategy_selection.py
├── strategy_variants.py
├── strategy_techniques.py
├── strategy_architecture.py
└── strategy_stress.py
```

These names are a proposed target structure, not yet an implementation requirement.

Principle:

> Strategy engines should orchestrate and execute canonical rules; they should not contain competing business-rule definitions.

## 6. Decisions To Freeze Before Refactoring

### 6.1 Strategy Applicability
Decide:
- authoritative goal characteristics/signals,
- horizon boundaries,
- fixed/flexible timeline semantics,
- priority semantics,
- how applicable strategies are determined.

### 6.2 Hard Constraints
Decide:
- which rules are true hard gates,
- their canonical owner,
- normalization/conflict handling,
- whether a hard-constraint failure can ever be overridden.

### 6.3 Eligibility
The current vocabulary contains 8 fits:

- cashflow_fit
- liquidity_fit
- debt_fit
- asset_resource_fit
- risk_capacity_fit
- goal_constraint_fit
- multi_goal_conflict_fit
- implementation_fit

Freeze:
- exact meaning of each fit,
- PASS / CONDITIONAL / FAIL semantics,
- thresholds,
- precedence,
- missing-data behavior,
- whether any fit is a hard gate.

### 6.4 Strategy Selection
Freeze:
- PASS vs CONDITIONAL precedence,
- score dimensions,
- score weighting,
- tie-breakers,
- feasibility role,
- whether ranking can ever override eligibility,
- authoritative selection output.

### 6.5 Variant Selection
There are 22 active variants across the 5 canonical strategies.

Freeze:
- selection conditions for every variant,
- rule precedence,
- mutually exclusive conditions,
- fallback/default behavior,
- missing-data behavior.

### 6.6 Technique Selection
Freeze:
- whether techniques are strategy-driven, goal-driven, or context-driven,
- selection precedence,
- whether techniques are mandatory/optional,
- canonical technique-to-strategy relationships.

### 6.7 Architecture Composition
Freeze:
- component activation rules,
- component dependencies,
- strategy/variant/technique interaction,
- architecture validity rules.

### 6.8 Stress Testing
Freeze:
- canonical stress scenarios,
- shock magnitudes,
- correlated shocks,
- metrics to evaluate,
- resilience classification,
- whether stress results can trigger strategy/variant re-selection.

## 7. Refactor Sequence

Refactor only after the decisions above are frozen.

1. **Freeze canonical decision contract.**
2. **Inventory existing rules** as KEEP / MOVE / MERGE / REPLACE / REMOVE / NEW.
3. **Create/update canonical rule modules** under `backend/rules/`.
4. **Make strategy engines consume canonical rules.**
5. **Remove duplicate and stale decision logic.**
6. **Add/adjust tests at each decision layer.**
7. **Run end-to-end Strategy Builder verification.**
8. **Make one consolidated implementation commit.**

## 8. Acceptance Criteria

The refactor is complete when:

- every strategy decision has one authoritative rule owner;
- the canonical set remains 5 strategies and 22 active variants;
- no stale strategy IDs remain in active decision logic;
- eligibility has one authoritative implementation;
- strategy selection has one authoritative implementation;
- variant selection has one authoritative implementation;
- stress testing has a defined canonical authority;
- engines primarily orchestrate/execute rather than redefine business rules;
- duplicate decision paths are removed;
- decision behavior is covered by tests;
- the complete Strategy Builder flow follows the canonical decision sequence.

## 9. Status

**Design phase — refactor not started.**

This document intentionally identifies decisions that still require explicit agreement. It does not invent unresolved business rules.
