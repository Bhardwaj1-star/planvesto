# Onboarding Execution Plan — Insurance Integration

## 1. Objective

Integrate the **existing Insurance & Protection implementation** into the guided onboarding flow.

This is an integration task, not a new insurance-domain build. The repository already contains the insurance UI, persistence model, database table, PDF extraction API, backend model/schema/API, and protection rules.

## 2. Current Code Reality

Insurance currently exists at:

- `frontend/components/onboarding/insurance/InsuranceSection.tsx`
- `frontend/lib/onboarding/insurance/types.ts`
- `frontend/lib/onboarding/insurance/persistence.ts`
- `frontend/lib/onboarding/insurance/api.ts`
- `frontend/supabase/migrations/012_insurance_policies.sql`
- `backend/models/insurance.py`
- `backend/schemas/insurance.py`
- `backend/api/insurance.py`
- `backend/rules/protection.py`

The existing InsuranceSection is already exposed from the financial information/profile UI through:

- `frontend/components/profile/FinancialInformationSection.tsx`

The current guided onboarding provider does **not** include insurance in `onboardingSteps`.

## 3. Required Onboarding Change

Add Insurance as an explicit guided onboarding stage.

Current sequence:

```text
1 Personal Information
2 Family & Dependents
3 Income
4 Expenses
5 Assets
6 Liabilities
7 Goals
```

Target sequence must explicitly include:

```text
1 Personal Information
2 Family & Dependents
3 Income
4 Expenses
5 Assets
6 Liabilities
7 Insurance
8 Goals
```

The final ordering must be confirmed against the intended financial-planning onboarding journey before implementation. Do not silently change the ordering of existing steps.

## 4. Execution Points

### 4.1 Onboarding navigation

Update `frontend/components/onboarding/OnboardingProvider.tsx`:

- add an Insurance step to `onboardingSteps`;
- give it a dedicated slug;
- update step numbering;
- ensure previous/next navigation works;
- ensure resume-step calculation includes insurance;
- ensure access blocking/redirect logic includes insurance;
- ensure final onboarding navigation still reaches the correct downstream destination.

### 4.2 Onboarding state

Do **not** duplicate the insurance data model inside the generic onboarding provider unless the existing architecture requires it.

The existing InsuranceSection already owns its policy loading/saving lifecycle through:

```text
loadInsurancePolicies()
saveInsurancePolicy()
removeInsurancePolicy()
```

The implementation should reuse that authority rather than creating a second insurance persistence path.

### 4.3 Onboarding route/page

Create or wire the dedicated onboarding route/page for Insurance using the existing:

```text
InsuranceSection
```

Do not rebuild the insurance form.

The existing UI already supports:

- policy name
- insurer
- policy number
- policy type
- premium
- premium frequency
- sum assured
- current/surrender value
- maturity date
- maturity value
- optional policy PDF extraction
- edit/remove/add policy

### 4.4 Persistence

Reuse the existing `insurance_policies` source of truth.

The current implementation already links:

```text
Insurance Policy
├── optional Asset → current/surrender value
└── optional Expense → premium
```

Do not create duplicate insurance assets or expenses as a separate onboarding mechanism.

### 4.5 Financial-state integration

Verify that adding Insurance to the onboarding journey does not bypass the existing downstream protection/financial calculations.

Existing protection rules include:

- life-insurance classification;
- health-insurance classification;
- required insurance-cover calculation.

Insurance onboarding must remain raw source-data capture; derived protection metrics remain downstream authority.

### 4.6 Completion semantics

Insurance completion must have an explicit, code-consistent definition.

Do not assume that merely visiting the Insurance page means the step is complete.

Define completion from the actual insurance persistence lifecycle and make it consistent with the existing onboarding completion model.

### 4.7 Profile compatibility

The existing Profile → Financial Information → Insurance entry point must continue working.

The onboarding integration must reuse the same InsuranceSection and persistence layer so that onboarding and profile editing do not create two competing insurance implementations.

## 5. Documentation Updates Required

After implementation, update:

- `docs/userflow/features/06-onboarding.md`

The document must reflect the actual implemented step list and insurance persistence contract.

It must explicitly document that:

```text
Onboarding
    ↓
Insurance Policy source records
    ↓
Insurance-linked asset / expense
    ↓
Financial / protection calculations
```

Only document behavior that is verified in code.

## 6. Tests / Regression Requirements

Add or update tests for:

- Insurance step route exists;
- Insurance appears in onboarding navigation;
- previous/next navigation works;
- resume-step logic includes Insurance;
- inaccessible future steps remain blocked;
- InsuranceSection loads existing policies;
- save/update/remove continue working;
- policy premium synchronization remains correct;
- current/surrender value synchronization remains correct;
- onboarding and Profile use the same insurance persistence authority;
- existing seven onboarding domains remain unaffected;
- final onboarding completion still reaches the correct downstream route.

## 7. Canonicalization / Duplication Constraint

Do **not** introduce:

- a second InsurancePolicy type;
- a second insurance database table;
- a second insurance persistence module;
- a second premium-to-expense mapping;
- a second current-value-to-asset mapping;
- a second protection-rule taxonomy.

The existing insurance implementation is the authority to reuse.

## 8. Implementation Order

```text
1. Confirm existing Insurance route/component wiring
        ↓
2. Add Insurance to canonical onboarding step navigation
        ↓
3. Wire existing InsuranceSection into the new step
        ↓
4. Integrate step completion/resume behavior
        ↓
5. Verify persistence and linked asset/expense behavior
        ↓
6. Verify Profile compatibility
        ↓
7. Update onboarding documentation
        ↓
8. Run frontend/backend/insurance regression tests
        ↓
9. Run CI
```

## 9. Definition of Done

Insurance is considered integrated only when:

- it is a first-class step in guided onboarding;
- the existing InsuranceSection is reused;
- insurance data persists through `insurance_policies`;
- linked asset/expense behavior remains intact;
- onboarding navigation and resume logic understand the step;
- Profile insurance editing still works;
- downstream protection/financial calculations continue using the existing insurance authority;
- documentation matches the final code;
- CI passes.

## 10. Explicit Non-Goals

This execution plan does **not** authorize:

- redesigning the insurance domain;
- inventing new insurance fields;
- changing existing policy semantics;
- changing protection formulas;
- creating new insurance taxonomy without code evidence;
- moving insurance into Personal Information merely because it is financial information;
- changing unrelated onboarding domains.

The task is to **integrate the already-existing Insurance implementation into the guided onboarding flow without creating a duplicate authority**.
