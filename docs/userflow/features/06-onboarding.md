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

The intended onboarding flow covers:

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

## 16. Code-Verified Step Contracts

The current frontend implements exactly seven ordered onboarding steps:

| Step | Route | State collection |
|---|---|---|
| 1 | `/investor/onboarding/personal-information` | `personalInformation` |
| 2 | `/investor/onboarding/family-dependents` | `familyMembers[]` |
| 3 | `/investor/onboarding/income` | `incomeSources[]` |
| 4 | `/investor/onboarding/expenses` | `expenses[]` |
| 5 | `/investor/onboarding/assets` | `assets[]` |
| 6 | `/investor/onboarding/liabilities` | `liabilities[]` |
| 7 | `/investor/onboarding/goals` | `goals[]` |

The navigation authority is `frontend/components/onboarding/OnboardingProvider.tsx`. The provider calculates the resume step from persisted record presence and prevents access beyond the next available step.

## 17. Code-Verified Onboarding State

The provider currently owns:

```text
planningUnitId
investorId
personalInformation
familyMembers[]
incomeSources[]
expenses[]
assets[]
liabilities[]
goals[]
completedSteps[]
isLoading
persistenceError
```

Persisted data is loaded whenever the pathname is under `/investor/onboarding/*` or `/investor/profile`.

Step completion is reconstructed as:

```text
fullName present       → step 1
familyMembers.length   → step 2
incomeSources.length   → step 3
expenses.length        → step 4
assets.length          → step 5
liabilities.length     → step 6
goals.length           → step 7
```

There is no separate persisted onboarding-completion field in the current provider/persistence implementation.

## 18. Code-Verified Input Contracts

### Personal information

```text
fullName
dateOfBirth
gender
maritalStatus
mobileNumber
address
city
state
country
occupation
```

Required validation is implemented for name, DOB, marital status, occupation and address/location fields. Mobile is optional but validated when supplied.

### Family / dependents

```text
name
relationship
dateOfBirth
occupation
financialDependency
includeInPlanning
```

The validator requires name, relationship, valid DOB and boolean financial dependency. Occupation and include-in-planning are not required by the current validator.

### Income

```text
incomeType
amount
frequency
expectedAnnualGrowth
```

Supported income types are Salary, Business, Professional/Freelance, Rental, Interest, Dividend, Pension and Other. Frequency is Monthly or Annual.

### Expenses

```text
category
amount
frequency
```

Supported categories and frequencies are defined in `frontend/lib/onboarding/expenses/types.ts`.

### Assets

```text
assetType
description
currentValue
purchaseValue
purchaseDate
```

Current value is required and positive. Purchase value/date are optional.

### Liabilities

```text
liabilityType
description
outstandingAmount
interestRate
regularPayment
frequency
endDate
```

Outstanding amount is required and positive. Interest rate and regular payment are optional. The current validator does not enforce frequency/endDate.

### Goals

The current frontend Goal model contains:

```text
name
goalType
targetAmount
targetMode
targetDate
targetAge
currentSavedAmount
monthlyContribution
priority
flexibility
inflationApplicability
notes
dynamicDetails
```

The current dynamic-details model contains goal-specific fields including retirement, passive-income, education, marriage, home, vehicle, vacation, wealth, debt and "other" details.

## 19. Code-Verified Persistence Contract

Persistence is implemented in `frontend/lib/onboarding/persistence.ts` and uses `getPlanningUnitId()`.

```text
Personal information → investors
Family/dependents   → dependents
Income              → income
Expenses            → expenses
Assets              → assets
Liabilities         → liabilities
Goals               → goals
```

List persistence follows the same general lifecycle:

```text
read existing IDs
    ↓
identify retained UUIDs
    ↓
delete omitted persisted records
    ↓
update existing records
    ↓
insert new records
    ↓
reload Planning Unit data
```

Income additionally requires an investor row before it can be saved.

## 20. Goal-Specific Onboarding Boundary

The onboarding goal UI currently exposes:

```text
retirement
marriage
vehicle
dream_home
education
vacation
debt_freedom
wealth_creation
fire_passive_income
others
```

This is the **frontend onboarding vocabulary**. It must not be treated as the backend canonical goal taxonomy.

The current goal persistence is split into two operations:

1. `saveGoals()` writes the base goal row.
2. `saveDynamicGoalDetailsForList()` writes `goal_type` and `dynamic_details`.

For `others`, the dynamic persistence uses `otherGoalName` as the stored `goal_name`.

The onboarding document therefore records goal collection only. Canonical identity, DefinedGoal calculation, funding gap and feasibility remain downstream Goal Planner responsibilities.

## 21. Current Code Gaps / Non-Assumptions

The following are directly observable implementation facts:

1. The frontend goal taxonomy differs from the backend canonical taxonomy; no canonicalization is asserted at onboarding level.
2. `saveGoals()` does not persist every field present in the frontend Goal model.
3. Goal priority is written from the current UI value rather than being canonicalized by the onboarding persistence layer.
4. Dynamic goal details are saved in a follow-up update after base goal persistence.
5. Dynamic goal persistence pairs saved/source goals by array index, not by a verified goal-ID mapping.
6. Liability validation does not currently enforce frequency or end date.
7. Step completion is inferred from loaded record presence rather than a dedicated persisted completion status.
8. Persistence is performed directly from the frontend through Supabase.
9. No field is described as calculation-driving merely because it exists in a frontend type.
10. No downstream FinancialState, Goal Engine, DefinedGoal or Strategy Builder behavior is claimed as onboarding behavior.

## 22. Regression Contract

### Navigation
- Eight steps remain ordered after the correction.
- Future steps remain inaccessible until the preceding step is completed.
- Completed steps remain revisitable.
- Resume behavior remains deterministic from persisted data.
- Successful persistence is required before a step advances.

### Input validation
- Existing per-domain validators remain authoritative for frontend validation.
- Required/optional status must not be strengthened in documentation without a corresponding code change.
- Enum vocabularies must match the current type definitions.

### Persistence
- Every onboarding save remains scoped to the current Planning Unit.
- Existing persisted UUID records are updated.
- Removed list records are deleted.
- Reloaded state matches persisted records.
- Income requires an investor row.
- Goal dynamic details remain attached to the saved goal.

### Authority
- Onboarding remains a source-input/persistence feature.
- FinancialState remains downstream.
- Goal canonicalization/calculation remains downstream.
- Strategy eligibility/selection remains downstream.

## 23. Final Onboarding Contract

```text
USER
  ↓
ONBOARDING ENTRY
  ↓
STEP ACCESS / RESUME LOGIC
  ↓
CLIENT VALIDATION
  ↓
ONBOARDING PROVIDER STATE
  ↓
PLANNING UNIT-SCOPED SUPABASE RECORDS
  ├── investors
  ├── dependents
  ├── income
  ├── expenses
  ├── assets
  ├── liabilities
  ├── insurance_policies
  └── goals + dynamic_details
  ↓
DOWNSTREAM AUTHORITIES
  ├── FinancialState
  ├── Goal Planner / DefinedGoal
  ├── MoneyWheel
  └── Strategy Builder
```

Scope: this document describes the onboarding behavior that is directly supported by the current repository implementation. It deliberately separates frontend collection/persistence from downstream canonical financial and goal-planning authorities.
