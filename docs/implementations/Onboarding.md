# Onboarding — Final Implementation Specification

**Document type:** Authoritative implementation specification  
**Scope:** Investor intake, canonical financial-input categories, section validation, persistence, reload consistency, and Financial State initialization  
**Status:** Consolidated from the existing Onboarding code evidence and the canonical goal decisions already recorded in the project. No dedicated `docs/feature/Onboarding.md` exists in the current repository, so missing business policy is marked unresolved rather than invented. Existing code is evidence of current behavior, not proof that the complete target contract is satisfied.

## 1. Design references

This specification separates canonical business requirements from the inspected implementation baseline.

- **Existing-code baseline:** `docs/existing features/Onboarding/00-BACKEND-INDEX.md` and the frontend/backend files listed in Section 10.
- **Canonical goal definition:** `frontend/lib/onboarding/goals/types.ts` contains the current canonical goal IDs and labels. Project-level canonical goal decisions take precedence over stale labels or aliases in other surfaces.
- **Profile boundary:** `docs/feature/Profile.md` defines Profile as the place to review account and financial information; it is not a replacement for the onboarding intake contract.
- **Downstream financial record:** Onboarding saves source records. Financial State is built through the Financial State service and is a separate derived snapshot.
- **Conflict rule:** preserve verified current behavior as evidence; distinguish it from required behavior and unresolved policy. Do not treat the current UI, a database column, or an audit document as proof that canonicalization is complete.

## 2. Purpose and ownership

Onboarding collects the investor's initial personal, household, income, expense, asset, liability, insurance, and goal information so the rest of Planvesto can work from consistent source records.

Onboarding owns:
- The investor intake flow and its section-level forms.
- Validation of user-entered fields before saving.
- Canonical category selection and mapping from UI values to stored records.
- Saving and reloading intake data for the correct planning unit.
- The completion state of each intake section.
- The handoff that builds the initial Financial State after required intake is complete.

Onboarding does not own:
- Financial ratios, financial-health interpretation, or Moneywheel calculations.
- Goal feasibility, funding-gap calculations, or required-return calculations.
- Strategy selection or the Accepted Plan.
- Deciding that a mapped asset is earmarked or committed to a goal.
- Treating a saved form or a completed step as proof that the financial plan is feasible.

Saving intake data and building Financial State are separate events. A Financial State snapshot is derived output; it must not become a second editable source of truth for the same inputs.

## 3. Canonical intake sections and data ownership

The current onboarding navigation defines eight steps:

| Step | Route | Data collected | Current storage target |
|---|---|---|---|
| 1 | `/personal-information` | Name, date of birth, gender, marital status, contact/address, occupation | `investors` |
| 2 | `/family-dependents` | Family member, relationship, date of birth, occupation, financial dependency, include-in-planning flag | `dependents` |
| 3 | `/income` | Income type, amount, frequency, expected annual growth | `income` |
| 4 | `/expenses` | Expense category, amount, frequency | `expenses` |
| 5 | `/assets` | Asset type, description, current value, purchase value/date | `assets` |
| 6 | `/insurance` | Policy details, premiums, cover and policy-related values | `insurance_policies`, with linked expense/asset records where applicable |
| 7 | `/liabilities` | Liability type, description, outstanding amount, interest rate, payment, frequency, end date | `liabilities` |
| 8 | `/goals` | Canonical goal type, target amount/date, priority, flexibility, goal-specific details | `goals`, with defined-goal calculations handled downstream |

This table reflects the current route/provider order, not the older ordering in the existing backend index. The index must not be treated as the authority for the current UI sequence.

The persistence layer scopes these records by `planning_unit_id`. Income also links to the investor record. Personal information currently loads the first investor record for the planning unit; the single-investor/multi-investor policy must remain explicit and consistent with the product's planning-unit model.

## 4. Canonical goal contract

The onboarding goal selector must use the canonical goal IDs and labels only. The canonical set is:

| Canonical ID | Canonical display name |
|---|---|
| `retirement` | Retirement |
| `marriage` | Marriage |
| `vehicle` | Vehicle |
| `dream_home` | Dream Home |
| `education` | Education |
| `vacation` | Vacation |
| `debt_freedom` | Debt Freedom |
| `wealth_creation` | Wealth Creation |
| `fire_passive_income` | FIRE / Passive Income / Financial Freedom |
| `others` | Others |

Required rules:
- Persist the canonical `goal_type` independently of the display name.
- Do not create aliases such as “Child Education”; “child” is captured as a goal-specific detail, not as a separate goal type.
- Retirement and FIRE / Passive Income / Financial Freedom are separate goals and must not be merged.
- Do not restore removed goal types such as Permanent or Philanthropy.
- For `others`, preserve the canonical type `others` and store the investor-provided name/details separately. A custom name must not become a new canonical type.
- Reload must reconstruct the same canonical type and goal-specific details that were saved. A blank goal type after reload is not acceptable.
- Canonical goal IDs and their ownership must not depend on display wording or the composition of goal-specific details.

### Goal-specific details

The current frontend model includes fields such as life expectancy and desired monthly lifestyle expense for Retirement; desired passive income for FIRE / Passive Income; who the Education or Marriage goal is for; preferred location for Dream Home; vehicle type/condition; vacation frequency/type; target wealth corpus; selected liability for Debt Freedom; and custom details for Others.

These fields describe the selected canonical goal. They must not be promoted to independent canonical goals or used to alter the canonical goal identity. Required fields and calculation dependencies must stay aligned with Goal Planner's approved input contract; the current frontend validation is not, by itself, proof that backend requirements are satisfied.

## 5. Canonical categories for financial inputs

The UI's current option sets are recorded below as existing-code evidence. They must be maintained in a single authoritative definition per domain and mapped consistently between UI, persistence, reload, and downstream consumers. This document does not invent a new category taxonomy where the business definition has not been supplied.

### Income

Current UI values in `frontend/lib/onboarding/income/types.ts`:
- Salary
- Business
- Professional/Freelance
- Rental
- Interest
- Dividend
- Pension
- Other

Current frequency options: Monthly, Annual.

### Expenses

Current UI values in `frontend/lib/onboarding/expenses/types.ts`:
- Housing
- Food & Groceries
- Utilities
- Transportation
- Education
- Healthcare
- Insurance
- Debt Payments
- Family Support
- Travel
- Entertainment
- Shopping
- Other

Current frequency options: Monthly, Annual.

### Assets

Current UI values in `frontend/lib/onboarding/assets/types.ts`:
- Bank / Cash
- Fixed Deposits
- Mutual Funds
- Stocks / Equity
- Bonds / Debt
- EPF / PPF
- NPS
- Gold
- Real Estate
- Business Ownership
- Vehicle
- Other

The current persistence layer stores the selected type and description together in `asset_name`, using a text pattern, then parses that text during reload. This is a current implementation detail, not a preferred canonical data contract.

### Liabilities

Current UI values in `frontend/lib/onboarding/liabilities/types.ts`:
- Home Loan
- Car Loan
- Personal Loan
- Education Loan
- Business Loan
- Credit Card
- Other

Current frequency options: Monthly, Quarterly, Annual.

### Category ownership rules

- A category shown in onboarding must map to one stable stored value; labels must not become accidental identifiers.
- Do not maintain competing category lists in forms, persistence helpers, calculations, and backend rules.
- Descriptions are additional details, not substitutes for the category/type.
- A category or frequency change must not silently reinterpret an existing record.
- Exact canonical stored IDs and any legacy-category migration are unresolved unless explicitly established in the repository's business rules. Do not invent them in code or documentation.
- Numeric amounts must be stored as numeric values, with missing optional values represented as null rather than silently changed to zero.

## 6. Validation and save behavior

Current code has domain-specific validation modules for goals, income, expenses, assets, liabilities, personal information, and family dependents. The required contract is:

- Validate required fields and numeric/date formats before saving.
- Amounts that are required must be finite and greater than zero.
- Optional values must remain genuinely optional; do not convert blank optional inputs into misleading zero values.
- A target date must be valid and not in the past where the selected goal requires a future target date.
- Goal-specific required inputs must be validated for the selected canonical goal type.
- Invalid or missing data must produce a clear validation/persistence error; it must not be represented as a successful save.
- A section's saved state must reflect successful persistence, not only a button click or local form state.
- If a multi-record save partially succeeds and a later operation fails, the user must not be shown a false all-saved state. Transaction/rollback behavior for the current multi-row saves is not established and must be verified before being promised.
- Saving one section must not silently delete unrelated records or overwrite records belonging to another planning unit.

Current implementation uses a mix of dedicated save functions and a shared save helper. Some sections reconcile existing IDs by deleting rows omitted from the submitted list; this behavior must be treated as a potentially destructive contract and covered by tests before changing it.

## 7. Persistence, canonical identity, and reload consistency

The required data lifecycle is:

```text
Investor input
    ↓
Section validation
    ↓
Canonical type/category + stable record identity
    ↓
Save to the correct planning unit
    ↓
Reload persisted records
    ↓
Reconstruct the same UI state
    ↓
Build Financial State when the completion contract is met
```

Rules:
- Use the database record ID for persisted records; temporary browser IDs must not be mistaken for database UUIDs.
- Every read, update, and delete must be scoped to the correct planning unit and, where required, record ownership.
- The save mapping and reload mapping must be inverse-compatible: saving a canonical value and reloading it must not lose the type, name, description, or relevant details.
- Do not infer canonical identity from a user-facing label when an explicit canonical ID is available.
- Avoid packing type and description into one free-text field when the schema supports separate fields; if the current schema requires this format, preserve round-trip behavior and document the limitation.
- Reloading a saved goal must restore its canonical `goal_type` and `dynamic_details`, rather than reconstructing the goal with an empty type and blank details.
- An existing saved goal must not be deleted merely because the current form could not reconstruct its identity or details.
- Historical/defined goal status must be respected when deciding which goals appear in onboarding. A cancelled goal must not be silently revived as active just because its source row still exists.

## 8. Completion and Financial State handoff

The current provider tracks section completion and the existing backend index describes a Financial State build after onboarding. The target contract is:

1. Each section saves and reloads its records successfully.
2. The completion indicator reflects the actual persisted section data and any explicit completion marker required by the section.
3. Insurance completion must be based on insurance-specific evidence or an explicit saved completion marker; unrelated liabilities or goals must not accidentally satisfy it.
4. The final onboarding completion action must call the authenticated Financial State build contract with the correct planning unit and scope.
5. A successful source-record save does not prove Financial State was rebuilt successfully.
6. If Financial State build fails, preserve the source records, show a clear failure, and allow a safe retry. Do not report the entire onboarding process as complete when the required handoff failed.
7. Routing to Moneywheel or Dashboard must happen only after the actual completion conditions are satisfied.
8. Financial State remains a derived snapshot; it must not overwrite source records or imply that goals are feasible.

The exact product policy for whether every section is mandatory, whether a user can skip a section, and which completion marker is authoritative is not fully defined in the inspected sources. Preserve the existing approved journey until that policy is explicitly settled.

## 9. Cross-feature boundaries

### Profile
Profile may display and allow approved edits to personal/financial information. Profile completion is not a financial-health score and does not prove financial inputs are mathematically valid. Onboarding and Profile must not silently maintain conflicting copies of the same source fields.

### Financial State
Onboarding writes source records; Financial State compiles a snapshot from those records. Keep input ownership and derived snapshot ownership separate.

### Moneywheel
Moneywheel consumes Financial State and relevant goal context to calculate canonical metrics. Onboarding must not calculate, duplicate, or hard-code Moneywheel formulas or status thresholds.

### Goal Planner
Onboarding captures canonical goal type, goal inputs, and goal-specific details. Goal Planner owns goal definition, funding requirements, feasibility, funding gap, and Goal-Level Return Required. Goal Funding, SIP, lump sum, and contribution escalation are funding/feasibility concepts, not extra onboarding goal types or Strategy Builder strategies.

### Strategy Builder
Strategy Builder consumes goal/financial context after the relevant planning decisions. Onboarding must not select a strategy, score strategies, apply the removed eight Eligibility Fits, or treat a saved goal as an accepted strategy/plan.

### Insurance
Insurance policy entry has its own policy record and can create linked asset/expense records. These linked records must remain traceable to the policy so edits/deletion do not create orphaned or duplicate financial entries. The full linkage/deletion contract requires verification.

## 10. Existing code and implementation status

### Frontend entry, routes, and state
- `frontend/app/investor/onboarding/page.tsx`
- `frontend/app/investor/onboarding/personal-information/page.tsx`
- `frontend/app/investor/onboarding/family-dependents/page.tsx`
- `frontend/app/investor/onboarding/income/page.tsx`
- `frontend/app/investor/onboarding/expenses/page.tsx`
- `frontend/app/investor/onboarding/assets/page.tsx`
- `frontend/app/investor/onboarding/insurance/page.tsx`
- `frontend/app/investor/onboarding/liabilities/page.tsx`
- `frontend/app/investor/onboarding/goals/page.tsx`
- `frontend/components/onboarding/OnboardingProvider.tsx`
- `frontend/lib/onboarding/persistence.ts`

### Domain definitions and validation
- `frontend/lib/onboarding/goals/types.ts`
- `frontend/lib/onboarding/goals/validation.ts`
- `frontend/lib/onboarding/goals/dynamicPersistence.ts`
- `frontend/lib/onboarding/income/types.ts`
- `frontend/lib/onboarding/expenses/types.ts`
- `frontend/lib/onboarding/assets/types.ts`
- `frontend/lib/onboarding/liabilities/types.ts`
- `frontend/lib/onboarding/family-dependents/types.ts`
- `frontend/lib/onboarding/personal-information/model.ts`
- `frontend/lib/onboarding/insurance/persistence.ts`

### Backend and downstream handoff
- `backend/api/financial_state.py` — authenticated Financial State build/latest/history endpoints and planning-unit/scope ownership checks.
- `backend/api/goals.py` — authenticated goal preview/save/list and defined-goal version endpoints.
- `backend/api/profile.py` — authenticated profile build/latest/history endpoints.
- `docs/existing features/Onboarding/00-BACKEND-INDEX.md` — existing evidence index; its page-order description differs from the current provider order.

### Current-code findings requiring correction or verification

1. **Goal type is lost on reload:** `loadRows()` reconstructs each goal with `goalType: ""`, even though the canonical `goal_type` exists in the goal model and the dynamic persistence helper writes it.
2. **Goal details are lost on reload:** `loadRows()` replaces `dynamic_details` with `emptyGoalDynamicDetails` instead of restoring persisted details.
3. **Primary goal save path does not persist canonical type/details:** `saveGoals()` writes `goal_name`, target amount/date, priority, and flexibility, but does not write `goal_type` or `dynamic_details`. A separate `saveDynamicGoalDetails()` helper exists; the complete call-path and consistency are not established by this file alone.
4. **Goal display-name mismatch:** the current goal type label for `fire_passive_income` is “FIRE / Passive Income”; the canonical business label recorded for this project is “FIRE / Passive Income / Financial Freedom”. Keep the ID stable and align the label with the canonical definition.
5. **Goal names and types are mixed:** the primary save path uses `value.name` for most goals and the custom name for Others. Canonical type and investor-provided display name must be stored separately.
6. **Insurance step completion can be inferred from unrelated data:** the provider's `step6Completed` calculation includes liabilities and goals in addition to insurance-policy evidence and a local completion marker. Since the current route order makes Insurance step 6, this can mark the step complete for the wrong reason.
7. **Category/description are packed into text:** assets and liabilities encode the selected type plus description in a single name field and parse it back. Unknown or changed labels can break round-trip reconstruction.
8. **Legacy index order is stale:** the existing backend index describes a different order and describes a Financial State build after Step 8. The current route/provider order must be used when describing current UI behavior; the exact final completion trigger needs verification.
9. **Insurance linked records need lifecycle verification:** insurance persistence may create or delete associated asset and expense records. Verify policy edit/delete and failure paths so linked rows do not become duplicates or orphans.
10. **Multi-row save atomicity is unverified:** the shared list save path can delete omitted rows and then update/insert rows in separate operations. A mid-save error can leave a partially updated section.

These are source-inspection findings, not claims that a fix has already been made.

## 11. Acceptance criteria

1. The eight current onboarding sections have one documented order and each section's completion state is tied to its own saved data/approved completion marker.
2. The canonical goal selector exposes only the ten canonical goal IDs in Section 4; no removed goal type or alias is reintroduced.
3. Every saved goal has a canonical `goal_type` separate from `goal_name`; `others` preserves the custom name separately.
4. Goal type, goal-specific details, target fields, priority, and flexibility survive save → reload → edit → save without loss.
5. FIRE / Passive Income / Financial Freedom and Retirement remain distinct canonical goals.
6. Income, expense, asset, and liability option sets are centrally defined and round-trip consistently through persistence.
7. Missing optional values remain null/empty as specified; numeric values and dates are validated before persistence.
8. Reads/writes/deletes remain scoped to the authenticated planning unit and the correct record ownership.
9. A failed save or Financial State build is surfaced as a failure and does not create a false completed state.
10. Insurance completion is not inferred from unrelated liabilities/goals; linked insurance asset/expense records remain consistent with policy records.
11. Building Financial State does not silently rewrite onboarding source records or mark goals feasible.
12. Tests cover canonical goal IDs/labels, save/reload round trips, custom Others goals, goal-specific details, section completion, deletion safety, planning-unit isolation, partial-save failure, and Financial State handoff.
13. Current code behavior and target behavior are reported separately; no claim of runtime, migration, or test success is made without verification.

## 12. Explicit non-goals and unresolved policy

This specification does not authorize inventing a new income/expense/asset/liability taxonomy, changing the planning-unit model, making every section mandatory without an approved product rule, converting profile completion into financial-health status, or using onboarding to calculate feasibility/strategy decisions.

The following require an explicit source-defined decision or further code verification:
- Canonical stored IDs and migration mapping for non-goal categories.
- Which onboarding sections are mandatory versus skippable.
- The authoritative completion marker and exact final Financial State build trigger.
- Whether onboarding is strictly single-investor per planning unit.
- Atomicity/rollback expectations for multi-row saves.
- The approved lifecycle for insurance-linked assets and expenses.
- Whether and where the dynamic goal persistence helper is invoked on every save path.
- Database schema/migration and production RLS state; repository source alone does not prove deployed database behavior.
