# Canonical Financial Calculation System — Implementation Prompt

You are a Senior Full-Stack Architect and Backend Engineer working on the existing Planvesto repository.

## OBJECTIVE

Make the current backend architecture **canonical and internally consistent** on the existing branch.

The goal is NOT to redesign the system.

The goal is to ensure that every shared financial calculation / derived financial fact has:

- one canonical definition,
- one canonical implementation/owner,
- one canonical output,
- and multiple consumers where required.

After this work, future engines such as MoneyWheel, Risk Profiler, Goal Engine, Investment Engine and Strategy Builder must consume canonical financial facts instead of independently recreating the same calculations.

---

# HARD CONSTRAINTS

1. Work ONLY on the existing backend.
2. Do NOT modify frontend.
3. Do NOT redesign frontend.
4. Do NOT modify Supabase database schema.
5. Do NOT create SQL migrations.
6. Do NOT run SQL migrations.
7. Do NOT use git commands.
8. Do NOT invent missing business rules.
9. Do NOT invent calculation formulas where the repository/docs have not defined them.
10. Do NOT change locked business decisions merely to make implementation easier.
11. Do NOT rewrite Strategy Engine unless required strictly to remove a confirmed calculation duplication.
12. Do NOT redesign MoneyWheel, Risk Profiler, Goal Engine or Investment Engine business scope.
13. Do NOT introduce product-selection logic.
14. Do NOT introduce new strategy logic.
15. Preserve existing API contracts unless a change is absolutely required for canonicalization.
16. If an architectural or business decision is genuinely missing, document it instead of guessing.

---

# SOURCE OF TRUTH

First inspect the existing repository completely enough to understand:

- `docs/architecture/FINANCIAL-PLANNING-ONTOLOGY.md`
- `docs/financial-planning/financial-situation-risk-investment-planning.md`
- all relevant backend architecture documents
- `backend/engines/calculation/`
- `backend/rules/`
- `backend/engines/rules/`
- `backend/engines/goal/`
- `backend/engines/strategy/`
- existing services
- existing schemas/models
- existing tests

Do not assume that documentation and implementation are already synchronized.

Explicitly identify:

1. what is already canonical,
2. what is duplicated,
3. what is calculated in multiple places,
4. what is only documented but not implemented,
5. what is implemented but not documented,
6. what cannot safely be canonicalized because the business rule is undefined.

---

# TARGET ARCHITECTURE

The canonical architecture must become:

```
RAW / PRIMARY FINANCIAL DATA
            ↓
CANONICAL FINANCIAL CALCULATIONS
            ↓
CANONICAL DERIVED FINANCIAL FACTS
            ↓
┌───────────┼───────────┬───────────────┐
↓           ↓           ↓               ↓
MoneyWheel  Risk        Goal Engine     Investment
            Profiler                    Engine
└───────────┴───────────┴───────────────┘
                    ↓
             Strategy Builder
                    ↓
             Financial Plan
                    ↓
                 Report
```

The important principle is:

> **Calculation ownership is centralized. Decision ownership remains domain-specific.**

Do NOT turn the central calculation layer into a decision engine.

---

# CANONICALIZATION RULE

For every financial fact:

```
ONE DEFINITION
ONE CALCULATION OWNER
ONE CANONICAL OUTPUT
MANY CONSUMERS
```

Example:

```
Risk Required
     ↓
Canonical Calculation
     ↓
MoneyWheel
Risk Profiler
Goal-related consumers
```

Risk Required must NOT be independently calculated by MoneyWheel and Risk Profiler.

Similarly, if the same canonical financial fact is required by multiple engines, calculate it once and expose it as a shared fact.

---

# IMPORTANT DISTINCTION

Do NOT centralize domain interpretation.

For example:

```
Canonical Fact:
Risk Required = X%

MoneyWheel:
interprets X% as financial evidence.

Risk Profiler:
compares X% against Risk Capacity and Risk Tolerance.

Goal Engine:
uses relevant goal facts for feasibility.

Investment Engine:
uses approved risk/allocation outputs for investment construction.

Strategy Builder:
uses relevant facts and constraints to solve a financial problem.
```

The fact is shared.

The decision remains owned by the appropriate engine.

---

# REQUIRED AUDIT

Before changing code, produce an internal mapping of:

| Financial Fact | Current Owner | Current Consumers | Duplicate Locations | Canonical Owner | Action |
|---|---|---|---|---|---|

At minimum inspect:

- Savings Rate
- Monthly Surplus
- Liquid Assets
- Liquid Asset Ratio
- Expense Coverage
- Emergency Coverage
- DTI
- Leverage Ratio
- Financial Asset Ratio
- Insurance Coverage Ratio
- Goal Funding Ratio
- Future Funding Ratio
- Required Rate of Return
- Goal Future Value
- Goal Funding Gap
- Required Monthly Contribution
- Current Portfolio Allocation
- Portfolio Concentration
- Allocation Gap
- Risk Required
- other repeated financial calculations discovered in the repository

Do not assume all of these belong in one calculation function/module. Determine the appropriate canonical ownership based on the existing architecture.

---

# CANONICAL FACT CONTRACT

Where appropriate, canonical derived facts should have a consistent structure containing concepts such as:

```
fact_id
value
unit
formula / calculation identity
inputs_used
availability
data_quality
calculation_version
source
```

Use the repository's existing models/types/conventions where available.

Do NOT create unnecessary abstractions merely for theoretical purity.

The implementation should remain simple and maintainable.

---

# DUPLICATION RULE

If two modules calculate the same financial fact:

1. determine which implementation is consistent with the locked documentation/business rules;
2. make that implementation canonical;
3. remove or replace the duplicate calculation;
4. make the other module consume the canonical result;
5. preserve behavior unless the existing behavior is demonstrably inconsistent with the documented rule;
6. if the correct behavior cannot be determined from the repository, STOP and document the ambiguity instead of guessing.

---

# MONEYWHEEL

MoneyWheel remains responsible for:

```
Observe
→ Calculate/consume canonical facts
→ Diagnose
→ Explain
```

But after canonicalization, MoneyWheel must not independently recreate a financial calculation that already has a canonical implementation.

MoneyWheel remains responsible for:

- metrics
- relationships between metrics
- diagnostics
- financial situation
- financial story

It does NOT:

- select products
- determine investment strategy
- determine strategic asset allocation
- construct portfolios
- own Risk Profiler decisions.

Also inspect and resolve the currently documented implementation mismatch between:

- legacy rule keys such as `emergency_fund_coverage`
- `current_liquidity_ratio`

and the current MoneyWheel definitions:

- `emergency_coverage`
- `expense_coverage`
- `liquid_asset_ratio`

Do this only where the intended mapping is unambiguous from the existing repository.

---

# RISK PROFILER

Do NOT implement Risk Profiler as a questionnaire.

The locked conceptual dimensions are:

```
Risk Capacity
Risk Capacity Constraints
Risk Required
Risk Tolerance
```

Risk Tolerance is behavioral/psychological.

Risk Required must be consumed from the canonical financial calculation/fact layer.

Risk Profiler must NOT recalculate Risk Required.

Do not invent the Risk Profiler's detailed scoring/business rules if they are not already defined.

---

# GOAL ENGINE

Goal Engine remains responsible for:

- goal target
- duration
- goal funding
- funding gap
- required contribution
- goal feasibility
- specialized goal calculations

But audit it for calculations that duplicate canonical financial facts.

Do not automatically move every Goal Engine calculation into the global calculation layer.

A calculation should become globally canonical only when it represents a reusable financial fact required by multiple domains.

Goal-specific calculations may remain owned by Goal Engine.

---

# INVESTMENT ENGINE

Do not redesign Investment Engine.

Only prepare the architecture so that it can consume canonical facts instead of duplicating them.

Maintain separation between:

```
Risk Profile
→ Strategic Asset Allocation
→ Sub-Asset Allocation
→ Product Category
→ Product Selection
→ Implementation
```

Do not invent allocation percentages.

---

# STRATEGY ENGINE

Keep Strategy Engine single-goal.

Do not rewrite its strategy logic.

Only remove confirmed duplication if it independently calculates a financial fact that should clearly come from the canonical fact layer.

Strategy Engine remains responsible for:

```
Goal/Problem
+
Constraints
+
Relevant Financial Facts
→ Strategy
→ Scenarios
→ Decision
```

---

# DATA FLOW

The final implementation should make the dependency direction clear:

```
Primary Financial Data
        ↓
Canonical Calculation
        ↓
Derived Financial Fact
        ↓
Domain Engine
        ↓
Domain Decision / Diagnosis
```

Never:

```
MoneyWheel → recalculates fact
Risk Profiler → recalculates same fact
Goal Engine → recalculates same fact
Investment Engine → recalculates same fact
```

---

# VERSIONING / TRACEABILITY

Where the existing architecture supports it, preserve calculation provenance.

A derived fact should be traceable to:

```
inputs
→ calculation
→ result
→ consuming engine
```

Do not introduce a complicated event-sourcing system or unnecessary infrastructure.

Simple deterministic provenance is sufficient.

---

# TESTING

After implementation, add/update backend tests for:

1. canonical calculation correctness;
2. same input → same canonical result;
3. MoneyWheel consumes canonical facts;
4. Risk Required is calculated only once;
5. Risk Profiler consumes Risk Required rather than recalculating it;
6. Goal Engine does not duplicate shared calculations;
7. existing Strategy Engine behavior remains intact;
8. missing data is not silently treated as zero;
9. calculation/version metadata remains deterministic;
10. existing relevant tests continue to pass.

Do not weaken tests merely to make the implementation pass.

---

# DOCUMENTATION

Update the architecture documentation so it explicitly states:

> **Canonical Financial Facts / Calculation Layer is the single source of truth for reusable derived financial facts.**

Also document:

- calculation ownership;
- fact ownership;
- engine consumption;
- which calculations remain domain-specific;
- which calculations are intentionally NOT centralized;
- Risk Required's single calculation ownership;
- MoneyWheel/Risk Profiler shared consumption model.

Do not rewrite unrelated product decisions.

---

# FINAL ACCEPTANCE CRITERIA

The task is complete only when:

### Architecture
- There is a clearly identifiable canonical calculation/fact layer.
- Shared financial facts have one owner.
- Domain engines consume shared facts.

### Consistency
- No confirmed duplicate calculation remains for the same canonical financial fact.
- Same input produces the same canonical result regardless of consumer.

### Boundaries
- Calculation ownership is centralized.
- Decision ownership remains distributed by domain.
- MoneyWheel remains diagnostic.
- Risk Profiler remains risk-structure focused.
- Goal Engine remains goal-focused.
- Investment Engine remains allocation/implementation focused.
- Strategy Engine remains strategy-focused.

### Safety
- No frontend changes.
- No database schema changes.
- No migrations.
- No invented business rules.
- No unnecessary architectural redesign.

### Documentation
- The canonical architecture is explicitly documented.
- Any unresolved ambiguity is documented rather than guessed.

### Final report

At the end, report exactly:

1. **Canonical calculations established**
2. **Duplicate calculations removed/replaced**
3. **Engines now consuming canonical facts**
4. **Domain-specific calculations intentionally left where they are**
5. **Files changed**
6. **Tests added/updated**
7. **Unresolved decisions / ambiguities**
8. **Any architectural risk remaining**

Do not claim something is canonical unless the implementation actually enforces it.
