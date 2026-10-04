# Onboarding

## 1. Feature Scope

Onboarding collects the user's raw planning information and persists the foundational Planning Unit data used by downstream financial planning.

```text
User
└── Onboarding
    ├── Personal information
    ├── Family / dependents
    ├── Income
    ├── Expenses
    ├── Assets
    ├── Liabilities
    └── Goals
        ↓
    Raw Planning Unit Records
        ↓
    FinancialState Construction
        ↓
    Financial Measures
        ↓
    Goal Planner / MoneyWheel / Strategy Builder
```

Onboarding owns raw-input capture and persistence. It does not own derived FinancialState calculations.

## 2. User / Request Inputs

Current onboarding covers:

- personal information
- family / dependents
- income
- expenses
- assets
- liabilities
- goals

The frontend is organized into dedicated onboarding steps and forms for these domains.

## 3. Input Source / Authority Boundary

| Domain | Onboarding role | Downstream authority |
|---|---|---|
| Personal information | collect/persist raw input | Planning Unit / profile data |
| Family/dependents | collect/persist raw input | Planning Unit records |
| Income | collect/persist raw input | FinancialStateService derives measures |
| Expenses | collect/persist raw input | FinancialStateService derives measures |
| Assets | collect/persist raw input | FinancialStateService / Goal Planner consumers |
| Liabilities | collect/persist raw input | FinancialStateService |
| Goals | collect/persist goal input | Goal Planner / DefinedGoal lifecycle |

Onboarding must not become a second owner of derived financial metrics.

## 4. Input Consumption Boundary

Inputs are classified as:

### Raw source records

- income sources
- expenses
- assets
- liabilities
- family/dependent records
- personal information
- goal inputs

### Context / ownership

- authenticated user
- Planning Unit
- investor context

### Derived outputs

These are not owned by onboarding:

- FinancialState
- savings rate
- liquidity ratios
- DTI
- MoneyWheel classifications
- goal funding calculations
- strategy eligibility

## 5. Onboarding State / Persistence

The frontend onboarding flow maintains step/navigation state and local form state while collecting inputs.

The persisted raw records become the source of truth for downstream FinancialState construction.

A completed onboarding step must not be interpreted as a completed financial plan; the downstream services still validate and derive their own authoritative state.

## 6. FinancialState Boundary

```text
Onboarding Raw Inputs
        ↓
Persisted Planning Unit Data
        ↓
FinancialStateService
        ↓
Authoritative FinancialState
        ↓
Canonical Financial Calculations
```

FinancialState freshness depends on source revision. Changed onboarding inputs must cause downstream state rebuild/refresh according to FinancialState authority rules.

## 7. Goal Boundary

Goals collected during onboarding are inputs to the Goal Planner.

The canonical goal taxonomy belongs to Goal Planner/rules, not to onboarding UI labels.

Therefore:

- onboarding can collect goal information;
- Goal Planner canonicalizes goal identity;
- DefinedGoal owns versioned calculated planning fields;
- onboarding does not become the owner of goal funding or feasibility.

## 8. Output Contract

Onboarding produces persisted raw planning data sufficient for downstream services to construct:

- current financial state
- canonical financial measures
- defined goals
- planning context

It does not directly produce a canonical strategy or Action Plan.

## 9. Ownership Boundary

- Onboarding entry/UI: `frontend/app/investor/onboarding/*`
- Onboarding shell/navigation: `frontend/components/onboarding/OnboardingShell.tsx`, `OnboardingProvider.tsx`
- Step hooks/forms: `frontend/hooks/onboarding/*`, `frontend/components/onboarding/*`
- Goals onboarding persistence: `frontend/hooks/onboarding/goals/*`
- FinancialState authority: `backend/services/financial_state_service.py`
- Goal canonicalization/calculation: `backend/rules/goals.py`, `backend/engines/goal/*`

The frontend captures data; backend domain services own authoritative derived state.

## 10. Downstream Dependencies

```text
Onboarding
├── Financial Health & Rules
├── Goal Planner
├── Investor Profile / planning context
└── MoneyWheel / Strategy Builder indirectly
```

Downstream consumers must read their canonical sources rather than relying on transient onboarding UI state.

## 11. Regression Contract

Tests should protect:

- onboarding data persists to the correct Planning Unit;
- ownership boundaries are enforced;
- individual/family context remains valid;
- raw financial inputs remain available to FinancialState construction;
- changed raw inputs invalidate stale derived FinancialState;
- goal input does not bypass Goal Planner canonicalization;
- onboarding does not write competing financial metrics.

## 12. Known Implementation Notes / Gaps

1. Onboarding UI contains broader specialized fields than the generic calculation layer; a collected field is not automatically calculation-driving.
2. Raw-input persistence and derived FinancialState must remain separate authority boundaries.
3. Any frontend/backend contract changes must preserve Planning Unit ownership and source revision semantics.

## 13. Important Semantic Boundaries

1. Raw input ≠ FinancialState.
2. Onboarding ≠ Goal Planner.
3. Onboarding goal data ≠ DefinedGoal authority.
4. Form state ≠ persisted source authority.
5. FinancialState ≠ MoneyWheel output.
6. Onboarding completion ≠ strategy readiness by itself.

## 14. Final Onboarding Output

```text
User Inputs
    ↓
Validated / Persisted Raw Planning Data
    ├── Personal
    ├── Family
    ├── Income
    ├── Expenses
    ├── Assets
    ├── Liabilities
    └── Goals
    ↓
FinancialState / DefinedGoal downstream construction
    ↓
Planning-ready source data
```

## 15. Onboarding End-to-End Contract

USER
    ↓
ONBOARDING STEPS
    ↓
RAW PLANNING UNIT RECORDS
    ↓
FINANCIALSTATE CONSTRUCTION + GOAL DEFINITION
    ↓
CANONICAL FINANCIAL / GOAL OUTPUTS
    ↓
DOWNSTREAM PLANNING

Scope: Onboarding only.