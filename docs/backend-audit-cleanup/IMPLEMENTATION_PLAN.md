# Backend Production Cleanup — Structure, Duplication & Rule Centralization

## Purpose

The Planvesto backend architecture is already largely built and connected. **Do not redesign or rebuild the architecture.**

The current problem is structural clarity:
- similar responsibilities exist in multiple places;
- financial/business rules are spread across engines, services and rule files;
- different components can make their own interpretation of the same condition;
- the actual decision-policy layer is still pending.

The goal is to make the existing backend **clean enough that every rule has one obvious home** before finalizing the actual decision rules for Strategy Builder and Action Plan.

## 1. Ownership Model

```text
RULES       = What is true / what condition applies
ENGINES     = Calculate or evaluate using those rules
LIBRARY     = What reusable strategies/techniques exist
SERVICES    = Coordinate the workflow
API         = Expose the workflow
DATA        = Read/write persistent data
```

Do not move code merely because of filenames. Move/merge only when responsibilities overlap.

## 2. Audit Before Editing

Create `docs/backend-audit-cleanup/RULE_OWNERSHIP_MAP.md`.

For every important business decision or financial metric, record:

| Decision / Metric | Current files | Current owner | Duplicate? | Final owner |
|---|---|---|---|---|

At minimum audit:
- Moneywheel
- Financial Health
- Health Score
- financial metrics
- constraints
- eligibility
- goal priority
- goal-type classification
- strategy applicability
- strategy selection
- strategy variants
- adaptation conditions
- multi-goal allocation
- trade-offs
- action-plan generation

**Do not implement new decision rules during this audit.** First establish where they will live.

## 3. Financial Truth — Consolidate

Audit Moneywheel, Financial Health, Health Score, `rules/`, `engines/rules/`, `engines/constraints/`, and financial-state components together.

Find repeated calculations for:
- emergency reserve
- liquidity
- savings/investment rate
- debt ratios
- leverage
- surplus
- protection/insurance measures
- cash-flow health
- other Moneywheel metrics

Target:

```text
Financial State
      ↓
Canonical Financial Metrics / Rules
      ↓
 ┌────┼───────────┐
Moneywheel  Health  Constraints
```

**Calculate once. Consume everywhere.**

Moneywheel may remain a product/view of those metrics. Financial Health may remain a derived interpretation. They must not become competing sources of financial truth.

## 4. Business Rules — Centralize

Establish one authoritative business-rule layer for genuine policy/truth such as:
- thresholds
- classifications
- goal categories
- priority rules
- eligibility conditions
- applicability conditions
- constraint conditions
- strategy-selection conditions
- action-generation conditions
- multi-goal trade-off rules

Do not centralize ordinary algorithms merely because they are code.

```text
Rule    = What is true
Engine  = Evaluate it
Service = Use the result in workflow
```

No service or engine should silently create a different threshold for the same concept.

## 5. Remove Duplicate Components

Find components that:
- calculate the same metric;
- classify the same condition differently;
- wrap another component without adding responsibility;
- maintain a second copy of the same business rule;
- are obsolete versions of a current component.

For each candidate:
1. Search all references.
2. Identify actual runtime owner.
3. Identify API/frontend dependencies.
4. Compare tests.
5. Choose one authoritative component.
6. Redirect consumers.
7. Delete only after proving it is unused.

Do not delete based on similar names alone.

## 6. Moneywheel / Financial Health / Health Score

Explicitly define:

```text
Moneywheel    = ?
Financial Health = ?
Health Score   = ?
```

If they represent the same underlying capability:

```text
Canonical Financial Metrics
          ↓
Moneywheel / Financial Health presentation
          ↓
Optional overall Health Score
```

There must be no second independent calculation system unless it has a clearly different business purpose.

## 7. Strategy Architecture — Prepare for Pending Rules

Do not invent final strategy rules during cleanup. Establish ownership:

```text
Strategy Library = What strategies exist?
Eligibility      = Which strategies are allowed?
Applicability    = Which fit investor + goal?
Decision Rules   = Which eligible strategy is selected?
Adaptation Rules = How can a conditional strategy be modified?
Action Rules     = What should the investor actually do?
```

The future Strategy Builder rules must not be scattered across strategy engine, service, library and API.

## 8. Strategy Builder — Rule Slots

Architecture must be ready to answer later:

- Which strategy is eligible?
- Which eligible strategy is selected?
- When is a strategy conditional?
- How can it be adapted?
- What action plan follows?
- What happens when multiple goals compete?

These are **pending business decisions**, not tasks to invent during this cleanup.

## 9. Action Plan Architecture

Action Plan must not invent its own financial logic.

```text
Financial State
 + Goal
 + Selected Strategy
 + Strategy Parameters
 + Rule Results
        ↓
Action Plan Generator
        ↓
Ordered Actions
```

Action-generation rules should have one authoritative home.

## 10. Services

For each condition in large services, ask:

> Is this workflow coordination, or is it a business rule?

If business rule → central rule layer.
If workflow coordination → service stays.

Do not split services merely to make files smaller.

## 11. Engines

Keep engines responsible for calculations, evaluations, transformations and decision execution using centralized rules.

They must not maintain competing versions of business thresholds or classifications.

## 12. What NOT to Change

Do not redesign APIs, database schema, frontend, working engine architecture, product philosophy or multi-goal architecture merely for cleanliness.

Do not add new financial features.
Do not finalize Strategy Builder policy.
Do not invent Action Plan policy.

This phase is **structural preparation**, not feature expansion.

## 13. Target Structure

```text
                 FINANCIAL STATE
                        ↓
            CANONICAL FINANCIAL TRUTH
                        ↓
              CENTRAL BUSINESS RULES
                        ↓
       ┌────────────────┼────────────────┐
       ↓                ↓                ↓
   GOAL ENGINE      CONSTRAINTS     MONEYWHEEL/HEALTH
       │                │                │
       └────────────────┼────────────────┘
                        ↓
                STRATEGY LIBRARY
                        ↓
                  ELIGIBILITY
                        ↓
                 APPLICABILITY
                        ↓
              PENDING DECISION RULES
                        ↓
                  STRATEGY
                        ↓
                ACTION PLAN RULES
                        ↓
                  ACTION PLAN
```

Folder names may remain if responsibilities are clear. **The goal is ownership, not cosmetic restructuring.**

## 14. Definition of Done

- Every important financial metric has one authoritative calculation.
- Every business rule has one authoritative definition.
- Moneywheel and Financial Health no longer compete for the same truth.
- Health Score has a clearly defined relationship with those metrics.
- Constraints consume canonical metrics/rules.
- Strategy components do not invent their own eligibility policy.
- Strategy Library only defines reusable strategy knowledge.
- Services coordinate rather than hide policy.
- Future Strategy Builder decision rules have an obvious central home.
- Future Action Plan rules have an obvious central home.
- Duplicate/legacy components are removed or explicitly justified.
- Existing backend connections continue to work.
- Existing behaviour remains intact unless a duplication/ownership bug is being fixed.

## Final principle

**Clean the structure first. Centralize the rules second. Finalize the decision policy third.**

Do not mix these three stages.
