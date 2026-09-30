# Planvesto Backend — Rule Finalization & Production Readiness Process

## 1. Purpose

This document defines the exact process to follow after structural cleanup and before finalizing Planvesto's financial decision rules.

### Objective

- Keep the existing backend architecture intact.
- Remove responsibility overlap and duplicate business logic.
- Establish one authoritative home for each business rule.
- Make the backend understandable before adding final decision policy.
- Finalize Strategy Builder and Action Plan rules only after ownership is clear.
- Preserve existing backend connections and working behaviour.

### Core principle

```text
CLEAN STRUCTURE
      ↓
CLEAR OWNERSHIP
      ↓
CENTRAL BUSINESS RULES
      ↓
FINAL DECISION POLICY
      ↓
PRODUCTION-READY BEHAVIOUR
```

This is a **cleanup + rule-finalization process**, not an architecture rewrite.

---

# 2. Current State

The backend already has the major architectural pieces required for Planvesto:

- API layer
- schemas / validation
- services
- engines
- data/repositories
- financial state
- goals
- constraints
- Moneywheel
- strategy system
- strategy library
- multi-goal orchestration
- action-plan generation
- tests

The problem is not that these components do not exist.

The problem is that some business decisions are still distributed across them.

### Current structural issue

```text
One business concept
      ↓
Rule file
+ Engine
+ Service
+ Strategy component
+ API/helper
```

This creates uncertainty about:

- which implementation is authoritative;
- where a rule should be changed;
- whether two modules are doing the same thing;
- whether two modules can produce different decisions.

---

# 3. Ownership Model — Lock This First

Every backend responsibility must fit into one of these categories.

| Layer | Responsibility | Example |
|---|---|---|
| `rules/` | Business truth/policy | emergency reserve threshold |
| `engines/` | Calculation/evaluation mechanics | calculate ratio, evaluate eligibility |
| `library/` | Reusable strategy knowledge | bucket strategy definition |
| `services/` | Workflow coordination | build planning workflow |
| `api/` | Transport/authentication | POST strategy endpoint |
| `data/` | Persistence | read financial state |
| `schemas/` | Input/output shape validation | StrategyRequest |
| `models/` | Internal data structures | StrategyDefinition |
| `tests/` | Verification | eligibility scenarios |

## Non-negotiable rule

A business rule must not have two independent authoritative implementations.

---

# 4. Rule vs Engine vs Service

This distinction must remain explicit.

### Business Rule

Answers:

> What condition is considered true?

Example:

```text
Emergency reserve below required threshold
→ safety condition is breached
```

### Engine

Answers:

> How do we calculate/evaluate that condition?

Example:

```text
Calculate available liquid resources
Compare with required reserve
Return result
```

### Service

Answers:

> When and where is this result used in the workflow?

Example:

```text
Build financial plan
→ evaluate constraints
→ evaluate strategies
→ generate output
```

### Library

Answers:

> What reusable strategies/techniques exist?

It must not decide which strategy is appropriate for a specific investor.

---

# 5. Phase A — Complete Rule Ownership Audit

Before writing new decision rules, inspect the whole backend.

Create/maintain:

`docs/backend-audit-cleanup/RULE_OWNERSHIP_MAP.md`

For every important business concept record:

| Concept | Current implementation | Duplicate locations | Final owner | Status |
|---|---|---|---|---|

Audit at minimum:

### Financial truth

- income
- expenses
- surplus
- savings rate
- investment rate
- liquidity
- emergency reserve
- debt burden
- leverage
- net worth
- protection/insurance
- financial health metrics

### Goal truth

- goal type
- goal normalization
- goal category
- goal priority
- goal horizon
- goal feasibility
- funding gap
- goal conflict

### Strategy truth

- strategy applicability
- strategy eligibility
- eligibility status
- strategy constraints
- strategy variants
- strategy selection
- strategy priority
- conditional status
- adaptation conditions
- strategy conflict
- strategy replacement

### Action truth

- action eligibility
- action generation
- action priority
- action ordering
- action dependencies
- action completion conditions

### Multi-goal truth

- goal ordering
- resource allocation
- trade-offs
- competing goals
- priority preservation
- surplus allocation

---

# 6. Phase B — Remove Duplicate Financial Truth

This is the first actual consolidation.

## Target

```text
Financial State
      ↓
Canonical Financial Metrics
      ↓
Consumers
 ├── Moneywheel
 ├── Financial Health
 ├── Constraints
 ├── Strategy Eligibility
 └── Multi-Goal Planning
```

## Rules

- Do not calculate the same metric independently in multiple engines.
- Do not create a second threshold for an existing metric.
- Do not create a service-specific interpretation of the same financial condition.
- Do not make Moneywheel and Financial Health competing sources of truth.

## Moneywheel / Financial Health / Health Score

Explicitly define:

```text
Canonical Financial Metrics = underlying financial facts
Moneywheel = financial-health view/system using those facts
Financial Health = interpretation/diagnostic layer using canonical facts
Health Score = only if a separate composite score is actually required
```

If two components perform the same business function, consolidate them rather than preserving both for naming reasons.

---

# 7. Phase C — Centralize Business Rules

Move genuine policy decisions into the authoritative rule layer.

## Centralize

- thresholds
- benchmarks
- classifications
- aliases
- goal categories
- priority definitions
- constraint definitions
- eligibility definitions
- applicability conditions
- selection conditions
- adaptation conditions
- action conditions
- trade-off policy

## Do not centralize

- ordinary mathematical algorithms
- database access
- API handling
- workflow sequencing
- UI formatting
- generic utilities

### Example

```text
rules/constraints.py
    ↓
EMERGENCY_RESERVE_CRITICAL_MONTHS = X

engines/constraints/evaluator.py
    ↓
calculate/evaluate investor state

services/...
    ↓
use result in planning workflow
```

The threshold exists once.

---

# 8. Phase D — Strategy Builder Rule Ownership

This is where the pending Planvesto decision system begins.

Do not immediately write arbitrary strategy-selection code.

First lock these separate questions.

## 8.1 Strategy Library

Answers:

> What strategies does Planvesto know?

Contains:

- strategy definitions
- strategy architecture
- strategy purpose
- strategy techniques
- strategy variants
- implementation concepts
- version information

Does **not** answer:

> Which strategy should this investor receive?

---

# 9. Strategy Eligibility

Answers:

> Is this strategy allowed for this investor + goal + financial state?

Eligibility should evaluate defined fits such as:

- cash-flow fit
- liquidity fit
- debt fit
- asset/resource fit
- risk-capacity fit
- goal-constraint fit
- multi-goal conflict fit
- implementation fit

Each fit must have:

```text
condition
→ status
→ reason
→ required change (if conditional)
```

Possible statuses:

```text
PASS
CONDITIONAL
FAIL
```

### Important

The `rules/` layer must eventually contain the **actual business conditions**.

The engine should execute/evaluate those conditions.

It must not silently invent its own policy.

---

# 10. Strategy Applicability

Eligibility and applicability are different.

### Eligibility

> Is this strategy permitted/possible?

### Applicability

> Does this strategy make sense for this investor and goal context?

Applicability may use:

- goal type
- goal horizon
- financial state
- constraints
- available resources
- strategy characteristics

The final implementation must clearly identify where applicability rules live.

---

# 11. Strategy Selection

This is currently one of the major pending decision layers.

It must eventually answer:

> If multiple strategies pass, which one should Planvesto select?

Do not bury this logic inside:

- API routes
- service conditionals
- StrategyDefinition classes
- random ranking code
- strategy library definitions

Create one authoritative decision-policy location.

### Selection inputs

At minimum:

```text
Financial State
Goal
Goal priority
Canonical financial metrics
Constraints
Eligible strategies
Applicability results
Strategy characteristics
Multi-goal context
```

### Selection output

```text
Selected Strategy
+ reason
+ relevant rule results
+ variant/parameters if applicable
```

The final selection policy must be documented before implementation.

---

# 12. Strategy Priority / Ranking

Do not confuse:

- eligibility
- applicability
- ranking
- selection

Example flow:

```text
10 strategies in library
        ↓
Eligibility
        ↓
6 allowed
        ↓
Applicability
        ↓
3 suitable
        ↓
Selection policy
        ↓
1 selected strategy
```

The exact Planvesto ranking/selection policy is a **business decision to be finalized**, not something the coding agent should invent.

---

# 13. Conditional Strategy

A conditional strategy means:

> It is not immediately ready under current conditions, but may become valid after defined changes.

The architecture must support:

```text
Evaluate
   ↓
CONDITIONAL
   ↓
Required Changes
   ↓
Adapt / modify implementation
   ↓
Re-evaluate
   ↓
PASS or FAIL
```

Do not treat every `CONDITIONAL` strategy as automatically eligible for final recommendation.

The actual adaptation rules must be finalized as business policy before implementation.

---

# 14. Strategy Variant

A variant is not a separate strategy unless the business model explicitly says so.

Example:

```text
Strategy
  ↓
Variant A
Variant B
Variant C
```

Define exactly what changes between variants:

- risk
- liquidity
- contribution pattern
- time horizon
- implementation technique
- asset mix
- de-risking pattern

Variant rules must have one owner.

---

# 15. Action Plan Rule Ownership

Action Plan must not become another strategy engine.

It answers:

> Given the investor state, selected strategy, constraints and strategy parameters, what should the investor actually do?

Target:

```text
Financial State
+
Goal
+
Selected Strategy
+
Strategy Parameters
+
Rule Results
        ↓
Action Rules
        ↓
Action Plan Generator
        ↓
Ordered Actions
```

## Action rules eventually need to define

- action type
- trigger condition
- required input
- amount/target if applicable
- priority
- sequence
- dependency
- deadline/horizon
- completion condition
- reason

### Important

Generic templates such as “implement primary strategy” are not the final business policy.

The final system must eventually explain the concrete financial action generated from the selected strategy and investor condition.

---

# 16. Multi-Goal Rule Ownership

Multi-goal planning must consume centralized rules rather than invent separate policies.

Eventually define:

- priority hierarchy
- minimum funding requirements
- essential vs discretionary treatment
- resource allocation
- goal conflict handling
- trade-off rules
- partial funding rules
- deferral rules
- goal interaction rules

Target:

```text
Goals
 ↓
Goal Priority Rules
 ↓
Financial Constraints
 ↓
Available Resources
 ↓
Allocation Rules
 ↓
Strategy Decisions
```

Do not finalize these rules inside the orchestration service before the business policy is agreed.

---

# 17. What We Must NOT Do Yet

Until the business rules are finalized:

- Do not invent strategy selection priorities.
- Do not invent which strategy is “best.”
- Do not add arbitrary scoring systems.
- Do not create new strategy categories without business approval.
- Do not create new financial thresholds without business approval.
- Do not make Action Plan more intelligent by adding hidden heuristics.
- Do not rewrite the existing strategy architecture.
- Do not redesign the database.
- Do not redesign the API.
- Do not redesign the frontend.

The coding agent prepares the system to execute the policy.

The business policy itself must be explicitly decided.

---

# 18. Rule Finalization Workflow

Once structure is clean, finalize rules in this order.

## Step 1 — Financial Truth

Finalize:

- canonical metrics
- formulas
- thresholds
- classifications
- financial-health conditions

## Step 2 — Goal Rules

Finalize:

- goal categories
- goal priority
- goal types
- horizon treatment
- feasibility conditions

## Step 3 — Constraint Rules

Finalize:

- safety constraints
- liquidity constraints
- debt constraints
- cash-flow constraints
- risk-capacity constraints

## Step 4 — Strategy Eligibility

For every Strategy × Investor/Goal condition define:

```text
PASS
CONDITIONAL
FAIL
```

## Step 5 — Strategy Applicability

Define when a strategy is appropriate for a specific goal/context.

## Step 6 — Strategy Selection

Define how multiple valid strategies are resolved into one strategy/variant.

## Step 7 — Strategy Adaptation

Define what changes can convert a conditional strategy into a valid strategy.

## Step 8 — Multi-Goal Allocation

Define how competing goals affect strategy selection and resources.

## Step 9 — Action Plan

For each selected strategy define the concrete action logic.

## Step 10 — Edge Cases

Define behaviour for:

- missing data
- zero income
- negative surplus
- insufficient liquidity
- high debt
- conflicting goals
- unavailable strategy resources
- impossible goal
- multiple equally applicable strategies
- incomplete risk information

---

# 19. Rule Specification Format

Every finalized business rule should be documented in a consistent format.

```text
Rule ID:

Name:

Purpose:

Applies When:

Inputs:

Condition:

PASS:

CONDITIONAL:

FAIL:

Required Action:

Priority:

Exceptions:

Dependencies:

Consumers:

Source of Truth:
```

This makes rules:

- understandable;
- testable;
- implementable;
- auditable;
- changeable without searching the entire codebase.

---

# 20. Coding Implementation Process

After a business rule is finalized:

1. Add/update the authoritative rule definition.
2. Add tests for the rule.
3. Make the relevant engine consume the rule.
4. Remove duplicate implementation.
5. Make services consume the engine result.
6. Verify API output.
7. Run regression tests.
8. Search the repository for old/duplicate implementations.
9. Update the ownership map.

### Required pattern

```text
Business decision
      ↓
Rule definition
      ↓
Engine evaluation
      ↓
Service workflow
      ↓
API output
```

---

# 21. QA Requirements

Every finalized rule must have tests for:

### Normal case

- expected PASS behaviour

### Boundary case

- exactly at threshold
- just below threshold
- just above threshold

### Failure case

- FAIL behaviour

### Conditional case

- CONDITIONAL behaviour
- required change

### Missing data

- incomplete input
- unknown value

### Interaction

- multiple rules triggering together

### Regression

- existing consumers continue to behave correctly

---

# 22. Duplicate Detection After Every Rule Change

After implementing a rule, search the entire backend for:

- old constant names
- old threshold values
- equivalent formulas
- duplicate condition strings
- duplicate classifications
- duplicate goal aliases
- duplicate strategy conditions
- duplicate action templates

The result should be:

```text
1 business rule
1 authoritative definition
N consumers
```

Not:

```text
1 business rule
3 implementations
4 slightly different thresholds
```

---

# 23. Production Readiness Gate

The structural cleanup is complete only when:

- every major financial metric has one authoritative definition;
- every business threshold has one authoritative definition;
- goal classification is centralized;
- constraint policy is centralized;
- eligibility policy has a clear authoritative home;
- applicability policy has a clear authoritative home;
- strategy selection has a clear authoritative home;
- action generation policy has a clear authoritative home;
- Moneywheel and Financial Health have non-overlapping responsibilities;
- services do not hide independent business policy;
- engines do not maintain competing rules;
- strategy library does not make investor-specific decisions;
- existing backend connections still work;
- regression tests pass;
- every final rule is traceable from definition → engine → consumer.

---

# 24. Final Architecture Goal

```text
                    FINANCIAL STATE
                           ↓
              CANONICAL FINANCIAL TRUTH
                           ↓
                 CENTRAL BUSINESS RULES
                           ↓
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
     GOALS             CONSTRAINTS      FINANCIAL HEALTH
        ↓                  ↓                  ↓
        └──────────────────┼──────────────────┘
                           ↓
                   STRATEGY LIBRARY
                           ↓
                    ELIGIBILITY
                           ↓
                    APPLICABILITY
                           ↓
                  STRATEGY SELECTION
                           ↓
                     ADAPTATION
                           ↓
                   MULTI-GOAL RULES
                           ↓
                    ACTION RULES
                           ↓
                     ACTION PLAN
```

The diagram represents **responsibility flow**, not necessarily folder names.

---

# 25. Final Rule

The backend should become boring to change.

When a business rule changes, the developer should be able to answer immediately:

```text
What is the rule?
        ↓
Where is it defined?
        ↓
Which engine evaluates it?
        ↓
Which services consume it?
        ↓
Which API output changes?
        ↓
Which tests prove it?
```

If the answer requires searching five engines and three services, the structure is not clean enough yet.

## Sequence to follow

**1. Clean ownership → 2. Consolidate duplicates → 3. Centralize rules → 4. Finalize Planvesto decision policy → 5. Implement rules → 6. QA the complete decision flow.**
