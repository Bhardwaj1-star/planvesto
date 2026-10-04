# Investor Profile

## 1. Feature Scope

Investor Profile captures risk information, preferences, priorities and constraints that describe investor decision context and can be consumed by strategy eligibility and decision logic.

```text
User
└── Investor Profile
    ├── Risk information
    ├── Preferences
    ├── Priorities
    └── Constraints
        ↓
    Profile / Risk Evidence
        ↓
    Strategy Eligibility
        ↓
    Strategy Decision
```

Investor Profile is decision context. It is not a replacement for FinancialState or a strategy itself.

## 2. User / Request Inputs

The profile domain includes:

- risk information
- preferences
- priorities
- constraints

Strategy Builder explicitly consumes investor priorities:

- safety
- liquidity
- growth
- flexibility

Risk/suitability evidence is consumed separately from financial metrics.

## 3. Authority Boundary

| Concept | Authority |
|---|---|
| Financial condition | FinancialStateService |
| Investor profile | Profile / investor-profile domain |
| Risk capacity evidence | Risk Profiler / suitability layer |
| Strategy eligibility | Strategy applicability / eligibility layer |
| Strategy decision | Strategy decision rules |

Investor Profile supplies evidence; it does not decide the final strategy.

## 4. Input Consumption Boundary

### Risk evidence

Risk information can establish investor risk/suitability evidence used in strategy evaluation.

### Preferences

Preferences describe investor choices and constraints. They are not automatically financial ratios.

### Priorities

Strategy decision priorities currently include:

- safety
- liquidity
- growth
- flexibility

These are decision preferences, not financial-health measures.

### Constraints

Profile constraints can be consumed as strategy/planning evidence. Their source and semantic kind must remain explicit.

## 5. Canonical Risk / Eligibility Boundary

Strategy eligibility remains:

- pass
- conditional
- fail

Risk capacity assessment is evidence for eligibility. It must not be confused with goal funding status or financial-ratio classification.

The strategy layer may evaluate required risk capacity against investor capacity, producing eligibility evidence.

## 6. Decision Logic Boundary

```text
Investor Profile
    ↓
Risk / Preference / Constraint Evidence
    +
DefinedGoal
    +
FinancialState
    ↓
Strategy Eligibility
    ↓
Strategy Decision
```

Investor Profile does not own strategy scoring or current StrategyVersion authority.

## 7. Output Contract

Profile output can provide:

- risk evidence
- preference context
- investor priorities
- profile constraints
- conflict/evidence information where available

The output is consumed by planning/strategy layers rather than directly becoming an implementation.

## 8. Ownership Boundary

- Profile models/domain: `backend/models/profile.py` and related profile services
- Risk policy: `backend/rules/risk_profiler.py`
- Strategy eligibility: `backend/engines/strategy/applicability.py` / eligibility layer
- Strategy decision policy: `backend/rules/strategy_decision.py`
- StrategyVersion authority: `backend/data/strategy_repository.py`
- Frontend profile contract/components: investor profile frontend modules

Exact profile persistence endpoints should remain aligned with the current backend/frontend contract; this document does not infer an endpoint not established in the source.

## 9. Downstream Dependencies

```text
Investor Profile
├── Strategy Eligibility
├── Strategy Decision
├── Suitability / Risk Evidence
└── Planning constraints
```

The profile should not directly mutate StrategyVersion or ActionPlan authority.

## 10. Versioning / Change Boundary

A profile change can change strategy evidence and therefore may require strategy reassessment according to policy.

It does not by itself imply a new Goal/DefinedGoal version.

A profile revision must not silently mutate an immutable StrategyVersion.

## 11. Regression Contract

Tests should protect:

- risk evidence remains distinct from financial metrics;
- investor priorities remain decision preferences;
- profile constraints preserve their source/semantic kind;
- eligibility remains pass/conditional/fail;
- profile changes do not directly bypass strategy decision lifecycle;
- StrategyVersion remains immutable/current only through explicit authority.

## 12. Known Implementation Notes / Gaps

1. The source material establishes profile/risk/constraint concepts but does not establish one universal persistence API contract for every profile field.
2. Risk capacity and risk preference must remain semantically distinct where the underlying implementation distinguishes them.
3. Strategy Builder remains the owner of strategy decision, not Investor Profile.

## 13. Important Semantic Boundaries

1. Investor Profile ≠ FinancialState.
2. Risk capacity ≠ risk preference.
3. Investor priority ≠ financial metric.
4. Profile constraint ≠ strategy decision.
5. Risk evidence ≠ StrategyVersion.
6. Profile update ≠ automatic StrategyVersion mutation.

## 14. Final Investor Profile Output

```text
Investor Inputs
    ↓
Profile / Risk / Preference / Constraint Context
    ↓
Strategy Eligibility Evidence
    ↓
Strategy Decision Evidence
    ↓
Strategy Builder
```

## 15. Investor Profile End-to-End Contract

USER
    ↓
INVESTOR PROFILE
    ↓
RISK / PREFERENCE / PRIORITY / CONSTRAINT EVIDENCE
    ↓
STRATEGY ELIGIBILITY
    ↓
STRATEGY DECISION
    ↓
STRATEGYVERSION LIFECYCLE

Scope: Investor Profile only.