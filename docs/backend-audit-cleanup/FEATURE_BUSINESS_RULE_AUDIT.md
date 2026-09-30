# Planvesto Backend — Feature & Business Rule Audit

## 1. Purpose

This document is the working audit of the current backend on `backend-audit-cleanup`.

It answers four questions for every major backend feature:

- What the feature is supposed to do.
- What the current code actually does.
- Which business rules already exist and where they live.
- Which rules are still missing, duplicated, provisional, or need a final Planvesto decision.

This is **not** a request to redesign the backend. The current architecture is treated as the base. The objective is to make responsibility and rule ownership explicit before final business-rule implementation.

---

# 2. Core Ownership Model

The production model should remain:

```text
Business Rules
      ↓
Engines
      ↓
Services / Workflow
      ↓
API
      ↓
Data
```

## Rule

- `backend/rules/` = authoritative business policy and definitions.
- `backend/engines/` = calculations, evaluation, selection and transformations using those rules.
- `backend/services/` = workflow coordination and persistence orchestration.
- `backend/api/` = authentication, request/response handling and ownership checks.
- `backend/data/` = database access only.
- `backend/library/` = reusable strategy knowledge/catalogue, not investor-specific decision policy.
- `backend/models/` and `backend/schemas/` = data contracts, not hidden business policy.

## Critical production principle

A threshold, classification, eligibility condition, selection score, priority rule, trade-off rule or action decision must have one authoritative owner.

Consumers may call the rule; they must not silently redefine it.

---

# 3. Executive Status

| Feature | Current implementation | Rule maturity | Main concern |
|---|---|---:|---|
| Financial State | Implemented | 🟢 | Must remain the authoritative financial input |
| Financial Metrics | Implemented/centralized | 🟢 | Prevent downstream recalculation |
| Moneywheel | Implemented | 🟢/🟡 | Define exact relationship with financial health |
| Financial Health | Partly derived from Moneywheel/metrics | 🟡 | Avoid becoming a second scoring system |
| Health Score | Previous duplicate removed | 🟢 | Do not recreate as a parallel engine without a distinct purpose |
| Goals | Implemented | 🟢/🟡 | Final priority/feasibility policy still needs business decisions |
| Goal Calculation | Implemented | 🟢 | Keep formulas in Goal Engine/rules, not services |
| Constraints | Implemented | 🟢/🟡 | Rule definitions should stay centralized |
| Risk Profile / Capacity | Implemented as profile constraints | 🟡 | Need final business meaning and downstream usage |
| Strategy Library | Implemented | 🟢/🟡 | Library knowledge vs decision policy must remain separate |
| Strategy Eligibility | Implemented | 🟡 | Final Planvesto thresholds/conditions pending |
| Strategy Applicability | Implemented | 🟡 | Needs one authoritative applicability policy |
| Strategy Selection | Engine exists | 🟡 | Scoring framework exists; final selection policy pending |
| Strategy Adaptation | Structure exists | 🟡 | Actual adaptation conditions are still policy work |
| Strategy Variants | Structure exists | 🟡 | Variant rules need explicit conditions |
| Multi-Goal Planning | Implemented | 🟡 | Final trade-off/resource allocation rules pending |
| Action Plan | Implemented | 🟡 | Generic generation exists; condition → action policy needs finalization |
| Financial Plan | Implemented | 🟡 | Consolidates outputs; must not invent business decisions |
| Reports | Implemented | 🟢/🟡 | Reporting should consume canonical outputs |
| Dashboard | Implemented | 🟡 | Presentation aggregation, not a new decision engine |
| Authentication/Ownership | Implemented | 🟢 | Continue strict ownership checks |

---

# 4. Financial State

## Current responsibility

`FinancialStateService` uses `FinancialStateEngine` and repositories to build/persist financial-state snapshots.

Evidence:

- `services/financial_state_service.py` uses `FinancialStateEngine` and snapshot repositories.
- Financial state is consumed by downstream services such as Moneywheel and action generation.

## Business rules already present

- Financial State is the source of investor financial data.
- Snapshot/version concepts exist.
- Missing/available data is represented rather than silently invented.

## Rules that must remain centralized

- Income definitions.
- Expense definitions.
- Essential vs discretionary expense classification.
- Asset/liability classifications.
- Surplus calculation.
- Savings/investment rate calculation.
- Safety reserve calculation.
- Debt-burden calculation.
- Liquidity calculation.
- Insurance/protection calculation.

## Do not put here

- Strategy selection.
- Investment product selection.
- Goal priority decisions.
- Action-plan decisions.

## Production requirement

Financial State must be the **single source of investor financial facts**. Downstream engines should consume it rather than independently rebuilding the same facts.

---

# 5. Financial Metrics / Financial Truth

## Current responsibility

Canonical financial calculations/rule definitions have been moved toward `backend/rules/financial_metrics.py` and related rule modules.

## Business rules

The canonical metric layer should own:

- Monthly/annual cash flow.
- Investable surplus.
- Savings rate.
- Emergency/safety reserve.
- Debt burden.
- Liquidity.
- Leverage.
- Insurance/protection gaps.
- Other canonical financial ratios used by multiple features.

## Required behavior

```text
Financial State
      ↓
Canonical Metrics
      ↓
Moneywheel / Constraints / Strategy / Multi-goal / Reports
```

## Forbidden duplication

- Moneywheel must not create a second definition of the same ratio.
- Constraints must not create a second threshold for the same condition.
- Strategy eligibility must not recalculate a metric differently.
- Reports must not calculate financial truth independently.

---

# 6. Moneywheel

## Current responsibility

`MoneywheelEngine` calculates the Moneywheel ratios using `rules.moneywheel`.

`MoneywheelService` adapts Financial State into Moneywheel input and persists/retrieves the result.

Evidence:

- `engines/moneywheel/engine.py` imports `RULE_SET_VERSION`, `RULES` and `classify` from `rules.moneywheel`.
- `services/moneywheel_service.py` uses `MoneywheelEngine` and `MoneywheelFinancialStateAdapter`.

## Business rules

Moneywheel owns the presentation/measurement model for its defined financial ratios.

The canonical rule layer should own:

- Ratio definitions.
- Thresholds.
- Classification/status logic.
- Rule-set version.

## Important boundary

Moneywheel should answer:

> "What does the investor's financial condition look like under these defined metrics?"

It should not answer:

> "Which strategy should the investor buy/use?"

## Financial Health relationship

Moneywheel and Financial Health must not become two independent calculation systems.

If Financial Health is derived from Moneywheel/canonical metrics, it should be a **derived interpretation**, not a second copy of ratio calculations.

---

# 7. Financial Health

## Current state

Financial-health diagnostics are already tied to the same financial metrics/rules used by Moneywheel/constraints.

The previous separate `health_score` duplicate was removed to avoid parallel scoring systems.

## Required final definition

Before implementing any new health score, decide explicitly whether Financial Health is:

- A direct Moneywheel interpretation.
- A derived composite score.
- A diagnostic status system.

Only one authoritative definition should exist.

## Rules required

- Healthy / warning / critical thresholds.
- Missing-data behavior.
- Which metrics contribute.
- Whether metrics are weighted.
- Whether a critical safety condition overrides an otherwise healthy aggregate.

## Do not do

- Create a new `HealthScoreEngine` that recalculates Moneywheel ratios.
- Put health thresholds in API/reporting code.
- Give dashboard code its own health classification.

---

# 8. Goals

## Current responsibility

`GoalEngine` calculates defined goals. `GoalService` coordinates persistence and goal updates.

Evidence:

- `engines/goal/engine.py` contains goal calculations.
- `services/goal_service.py` uses `GoalEngine` and `GoalRepository`.

## Business rules already centralized

`rules/goals.py` provides:

- Goal type aliases.
- Canonical goal type normalization.
- Essential/discretionary classification.

## Required business rules

### Goal identity

- Canonical goal type.
- Goal category.
- Goal horizon.
- Goal target date.

### Goal priority

Need final Planvesto rules for:

- Mandatory/safety goals.
- Essential goals.
- Important goals.
- Discretionary goals.
- User-defined priority.
- System-defined priority.
- Conflict resolution.

### Goal feasibility

Need final rules for:

- Target amount.
- Inflation-adjusted target.
- Existing assets assigned to goal.
- Required contribution.
- Funding gap.
- Surplus availability.
- Time horizon.

## Important boundary

Goal Engine calculates **what the goal requires**.

It does not decide **how the investor should fund it**. That belongs to strategy planning.

---

# 9. Goal Calculations

## Current capabilities

Goal calculation is decomposed into dedicated calculation responsibilities such as target calculation, funding gap, asset projection and specialized goal calculations.

## Rules

Centralize/reuse:

- Future value/inflation calculation.
- Required investment/contribution calculation.
- Existing asset projection.
- Funding gap calculation.
- Goal feasibility status.

## Production requirement

The same goal formula must not be reimplemented inside Strategy, Reports, Financial Plan or API layers.

Consumers should call the Goal Engine/calculation rule.

---

# 10. Constraints

## Current responsibility

`FinancialRatioConstraintEvaluator` evaluates financial ratios and goal priorities against approved constraints.

It is used by multi-goal planning and related orchestration.

## Centralized rule ownership

Constraint thresholds and rule IDs belong in `backend/rules/constraints.py` and related canonical rule modules.

## Constraints should answer

- Is the investor financially safe enough to proceed?
- Is liquidity sufficient?
- Is debt burden acceptable?
- Is reserve adequate?
- Is the goal allowed to receive incremental resources?
- Does a financial condition restrict a strategy?

## Constraints should NOT answer

- Which strategy is the best overall.
- Which product should be selected.
- What exact action the investor must take.

Those are downstream decisions.

---

# 11. Risk Profile / Risk Capacity

## Current state

`engines/profile/risk.py` derives risk-capacity constraints from financial-state facts such as surplus, reserve and EMI burden.

Evidence:

- `backend/engines/profile/risk.py` contains `risk_capacity_surplus`, `risk_capacity_reserve` and debt/EMI-related constraints.

## Business distinction

Keep separate:

- Risk tolerance = behavioral/psychological capacity to tolerate volatility.
- Risk capacity = financial ability to absorb risk.
- Risk requirement = risk needed to achieve a goal.

## Required final rule

The strategy system must define exactly where each of these is used.

Risk capacity should not automatically become a strategy recommendation by itself.

---

# 12. Strategy Library

## Current responsibility

The strategy library stores reusable strategy knowledge/catalogue and strategy versions/definitions.

## Library owns

- Strategy identity.
- Strategy description.
- Strategy architecture.
- Supported goal types.
- Components/techniques.
- Strategy version.
- General implementation structure.

## Library must NOT own investor-specific decisions

It should not permanently decide:

- This investor must use Strategy X.
- Strategy X wins over Strategy Y for this investor.
- This investor must perform Action Z.

Those belong to the rule/decision system.

---

# 13. Strategy Applicability

## Current state

Strategy definitions include applicability information such as supported goal types and constraints.

## Final business rules required

For every strategy define:

- Applicable goal types.
- Minimum/maximum horizon.
- Required liquidity conditions.
- Required surplus conditions.
- Debt restrictions.
- Required asset resources.
- Risk-capacity requirements.
- Goal constraints.
- Multi-goal compatibility.
- Implementation requirements.

## Central rule

Applicability answers:

> "Can this strategy logically be considered for this investor/goal?"

It does not answer:

> "Should this be the final selected strategy?"

---

# 14. Strategy Eligibility

## Current state

The system has eight eligibility fits:

1. `cashflow_fit`
2. `liquidity_fit`
3. `debt_fit`
4. `asset_resource_fit`
5. `risk_capacity_fit`
6. `goal_constraint_fit`
7. `multi_goal_conflict_fit`
8. `implementation_fit`

Eligibility produces statuses such as:

- PASS
- CONDITIONAL
- FAIL

## Current architectural issue

The centralized `rules/eligibility.py` defines the policy vocabulary/status layer, but actual fit evaluation remains in the strategy eligibility engine.

## Final requirement

Each fit must have an authoritative business rule specification:

```text
Fit
→ input data
→ condition
→ PASS condition
→ CONDITIONAL condition
→ FAIL condition
→ evidence
→ required adaptation
```

## Example

```text
cashflow_fit

PASS:
    required contribution <= investable surplus

CONDITIONAL:
    contribution can become feasible after an approved cash-flow adjustment

FAIL:
    contribution remains unaffordable under allowed adjustments
```

The actual numerical thresholds must be finalized as Planvesto business decisions, not guessed by developers.

---

# 15. Strategy Selection

## Current state

`engines/strategy/decision.py` performs strategy decision/scoring and now delegates scoring policy to `rules/strategy_decision.py`.

## Centralized policy slots

The rule layer contains scoring functions/slots for dimensions such as:

- Goal fit.
- Horizon fit.
- Funding fit.
- Feasibility.
- Component fit.
- Overall decision score.

## Missing final business decisions

Need to finalize:

- Which criteria matter.
- Weight of each criterion.
- Whether some criteria are hard gates instead of scores.
- What happens on a tie.
- Whether a higher score can ever override a hard constraint.
- Minimum score to select.
- What happens when no strategy passes.
- What happens when several strategies are conditionally eligible.

## Critical rule

```text
FAIL eligibility
    ↓
Cannot win by score.
```

Scoring must never override a hard business constraint.

---

# 16. Strategy Adaptation

## Current state

`rules/adaptation.py` provides standardized adaptation formatting for conditions such as:

- Cash flow.
- Liquidity.
- Risk.
- Other strategy requirements.

## Missing final business rules

Need to define:

- Which conditions are adaptable.
- Which conditions are never adaptable.
- Maximum allowed adaptation.
- Who/what can change: contribution, horizon, allocation, strategy variant, supporting strategy, etc.
- When adaptation must be re-evaluated.
- When the strategy must be rejected.

## Required flow

```text
Strategy
  ↓
Eligibility
  ↓
CONDITIONAL
  ↓
Allowed adaptation
  ↓
Re-check eligibility
  ↓
PASS → continue
FAIL → reject/replace
```

The adaptation layer must not simply convert every conditional case into a pass.

---

# 17. Strategy Variants

## Required rules

For every variant define:

- Parent strategy.
- Variant purpose.
- Trigger conditions.
- Differences from base strategy.
- Required investor conditions.
- Risk/cash-flow implications.
- When the variant becomes unavailable.

## Boundary

Strategy Variant = a defined version of a strategy.

Strategy Technique = a reusable method such as bucketing, laddering or glide path.

Do not mix these concepts.

---

# 18. Multi-Goal Planning

## Current state

Multi-goal planning uses `MultiGoalPlanningService`, `MultiGoalOrchestrator` and `FinancialRatioConstraintEvaluator`.

`rules/multi_goal.py` contains priority hierarchy and trade-off policy helpers.

## Rules already identified

- Priority ranking.
- Essential vs discretionary handling.
- Higher-priority comparison.
- Resource competition.
- Trade-off representation.

## Final rules required

Need exact policies for:

- How available surplus is allocated.
- Whether safety goals always preempt discretionary goals.
- Whether user priority can override system priority.
- Minimum funding floor per goal.
- What happens when no allocation satisfies all goals.
- Whether goal horizon affects allocation priority.
- How partially funded goals are handled.
- How a goal is paused/deferred.
- How strategy choices interact across competing goals.

## Important boundary

Multi-goal orchestration should coordinate decisions. The underlying priority/trade-off rules must remain centralized.

---

# 19. Action Plan

## Current state

Action-plan infrastructure exists across:

- `rules/action_plan.py`
- `services/strategy_action_generator.py`
- `services/action_plan_service.py`
- `engines/action_plan/impact_engine.py`
- Action Plan API/repository/models/schemas.

## Current rule maturity

The system can generate deterministic implementation actions from selected strategy/version information.

However, the final Planvesto business policy is still incomplete.

## Final action rules required

For each action define:

- Trigger condition.
- Source decision.
- Action type.
- Exact action description.
- Goal/strategy relationship.
- Sequence/order.
- Priority.
- Required amount if applicable.
- Deadline/frequency if applicable.
- Expected impact.
- Preconditions.
- Completion condition.
- Failure/review condition.

## Required decision

```text
Financial condition
        ↓
Selected strategy
        ↓
Strategy-specific conditions
        ↓
Action rule
        ↓
Action
```

Generic "implement strategy" actions are not enough for the final product.

---

# 20. Action Impact Engine

## Responsibility

Calculate/estimate the financial impact of an action.

## Must not decide

- Whether the action should exist.
- Whether the action is suitable.
- Whether the strategy should be selected.

Those decisions belong upstream.

## Required relationship

```text
Action Rule
   ↓
Action generated
   ↓
Impact Engine
   ↓
Projected effect
```

---

# 21. Financial Plan

## Current state

`FinancialPlanService` consolidates multi-goal planning and strategy outputs into a live consolidated plan.

## Correct responsibility

Financial Plan should be the **assembled output**, not a new rule engine.

It should consolidate:

- Financial state summary.
- Financial health/metrics.
- Goals.
- Goal feasibility.
- Constraints.
- Selected strategies.
- Strategy variants/scenarios.
- Multi-goal allocation.
- Actions.
- Trade-offs.
- Warnings/review items.

## Forbidden

Financial Plan must not silently invent new thresholds or select a strategy using its own rules.

---

# 22. Reports

## Current components

The backend contains goal/strategy/retirement reporting services and PDF/report renderers.

## Rule

Reports are presentation/output layers.

They should consume persisted/canonical planning results.

## They should not

- Recalculate financial truth.
- Re-select strategies.
- Change eligibility.
- Change goal priority.
- Create new action decisions.

If a report needs a missing calculation, add it to the correct engine/rule owner rather than embedding it in the renderer.

---

# 23. Dashboard

## Responsibility

Dashboard aggregates the investor's current state for display.

## Should consume

- Financial State.
- Canonical Metrics.
- Goals.
- Strategy state.
- Action state.
- Moneywheel result.

## Should not become

A second financial-analysis engine.

Any dashboard-specific classification must call the canonical rule rather than reproduce it.

---

# 24. Planning Orchestration

## Current state

`PlanningOrchestrationService` exposes module availability and planning context; multi-goal orchestration produces funding status, trade-offs and action-plan information.

## Correct responsibility

Coordinate:

- What modules are available.
- What data is available.
- What sequence should run.
- How outputs are assembled.

## Not responsible for

- Defining financial thresholds.
- Defining strategy eligibility.
- Defining strategy selection weights.
- Defining action business policy.

---

# 25. Authentication & Ownership

## Current state

API authentication and ownership helpers exist for planning units and child resources such as strategies/actions.

## Business/security rules

- User can access only their planning unit.
- Child resources must belong to the requested planning unit.
- Strategy versions/runs must be ownership checked.
- Action-plan records must be ownership checked.
- Cross-investor resource access must fail.

## Production requirement

Every new endpoint must use the same ownership pattern.

Never rely only on an ID being supplied by the client.

---

# 26. Data / Repository Layer

## Responsibility

Repositories read/write database state.

## Should not contain

- Strategy selection rules.
- Goal priority policy.
- Financial thresholds.
- Eligibility decisions.
- Action decisions.

Repositories may enforce data-level constraints and query ownership, but business policy should remain above them.

---

# 27. Main Rule Duplication Audit

## Known areas to watch

### Moneywheel / Financial Health / Constraints

- Same financial ratios must come from canonical metric/rule definitions.
- Classification should not be recreated in each consumer.

### Goal classification

- Goal aliases/types must come from `rules/goals.py`.
- Engines should not maintain private goal-type maps.

### Protection

- Insurance types and cover calculation must come from `rules/protection.py`.

### Financial classifications

- Expense/liability classifications must come from `rules/financial_metrics.py` or the designated canonical rule module.

### Constraint thresholds

- Thresholds must come from `rules/constraints.py`.

### Eligibility

- Fit names/statuses and final conditions must have one authoritative rule owner.

### Strategy decision

- Scoring weights/formulas must come from `rules/strategy_decision.py`.

### Multi-goal

- Priority and trade-off rules must come from `rules/multi_goal.py`.

### Action plan

- Action-trigger/business-policy rules must come from `rules/action_plan.py` or its final designated rule modules.

---

# 28. Rules That Are Already Structural vs Rules That Need Business Decisions

## Already structural / largely implemented

- Financial-state capture.
- Financial-state snapshots.
- Goal calculation.
- Financial metrics.
- Moneywheel calculation.
- Constraint evaluation framework.
- Strategy library.
- Strategy applicability framework.
- Eight eligibility fits.
- PASS/CONDITIONAL/FAIL model.
- Strategy decision/scoring framework.
- Multi-goal orchestration framework.
- Action-plan infrastructure.
- Financial-plan aggregation.
- Report generation.
- Ownership/security framework.

## Still require explicit Planvesto business decisions

- Exact financial thresholds.
- Final financial-health interpretation.
- Goal priority hierarchy.
- User priority vs system priority.
- Goal feasibility classification.
- Exact eligibility conditions.
- PASS vs CONDITIONAL boundaries.
- Allowed adaptations.
- Strategy-selection weights.
- Tie-breaking.
- No-strategy outcome.
- Strategy variant triggers.
- Multi-goal allocation policy.
- Trade-off policy.
- Action triggers.
- Action ordering.
- Action priority.
- Action completion/review conditions.
- Product/implementation selection rules if product selection is introduced.

---

# 29. Required Final Decision Flow

The target business flow should be:

```text
1. Financial State
       ↓
2. Canonical Financial Metrics
       ↓
3. Moneywheel / Financial Health interpretation
       ↓
4. Defined Goals
       ↓
5. Goal calculations + feasibility
       ↓
6. Constraints
       ↓
7. Strategy applicability
       ↓
8. Strategy eligibility
       ↓
9. PASS / CONDITIONAL / FAIL
       ↓
10. Allowed adaptation + re-check
       ↓
11. Strategy scoring / selection
       ↓
12. Multi-goal conflict / allocation
       ↓
13. Selected strategy + variant
       ↓
14. Action rules
       ↓
15. Action plan
       ↓
16. Consolidated Financial Plan
       ↓
17. Investor Report
```

This is the target **business flow**, not a request to create new layers if existing modules already perform the job.

---

# 30. Rule Finalization Order

Do not write strategy-selection rules before the underlying financial truth is locked.

Use this order:

### Phase 1 — Financial Truth

- Lock financial metric definitions.
- Lock thresholds.
- Lock missing-data behavior.
- Lock financial-health interpretation.

### Phase 2 — Goal Truth

- Lock goal types.
- Lock priority.
- Lock feasibility.
- Lock conflict hierarchy.

### Phase 3 — Strategy Truth

- Lock applicability.
- Lock all eight eligibility fits.
- Lock PASS/CONDITIONAL/FAIL.
- Lock adaptations.
- Lock selection scoring.
- Lock variants.

### Phase 4 — Multi-Goal Truth

- Lock resource allocation.
- Lock trade-offs.
- Lock competing-goal behavior.

### Phase 5 — Action Truth

- Lock strategy → action mapping.
- Lock action triggers.
- Lock sequence/priority.
- Lock completion/review conditions.

### Phase 6 — Report Truth

- Assemble canonical outputs.
- No new decision logic in reports.

---

# 31. Rule Specification Template

Every final business rule should be documented in this format before coding:

```text
Rule ID:
Rule Name:
Owner Module:
Purpose:
Inputs:
Condition:
PASS:
CONDITIONAL:
FAIL:
Priority:
Exceptions:
Missing-data behavior:
Downstream consumers:
Evidence/output:
Version:
Tests required:
```

## Example

```text
Rule ID: STR-ELIG-CASHFLOW-001
Rule Name: Cash Flow Fit
Owner Module: rules/eligibility.py
Purpose: Determine whether the investor can fund the strategy
Inputs: investable surplus, required contribution
Condition: required contribution vs available surplus
PASS: contribution is affordable
CONDITIONAL: affordability can be achieved through an approved adaptation
FAIL: contribution remains unaffordable
Exceptions: explicitly defined by Planvesto policy
Missing-data: do not assume affordability
Tests: pass / conditional / fail / missing data
```

---

# 32. Production Rule Integrity Checks

Before calling the backend production-ready, verify:

- Every business rule has exactly one owner.
- No engine duplicates a threshold.
- No service creates a private financial classification.
- No API performs business calculations.
- No report changes a decision.
- No score overrides a hard constraint.
- Every conditional strategy has a defined adaptation path.
- Every adaptation is re-evaluated.
- Every selected strategy has an explainable reason.
- Every action has a trigger/source decision.
- Multi-goal decisions expose trade-offs.
- Missing data never silently becomes a positive assumption.
- Rule versions are traceable.
- Tests cover each final rule branch.

---

# 33. Final Audit Conclusion

The backend is structurally mature enough to move from architecture cleanup into **business-rule finalization**.

The highest-value work now is not adding more folders or engines. It is making the decision policy explicit and authoritative.

The key transition is:

```text
CURRENT
Code contains the machinery,
but some decisions are still provisional.

        ↓

TARGET
Every important Planvesto decision has:

ONE RULE OWNER
ONE CLEAR CONDITION
ONE OUTPUT
ONE ENGINE CONSUMER
ONE TEST SET
```

The most important pending decisions are:

1. What makes a strategy eligible.
2. What makes it conditional.
3. What adaptation is allowed.
4. How eligible strategies are selected.
5. How competing goals are resolved.
6. What exact actions follow from each decision.
7. How the complete financial plan/report assembles those outputs.

Once those are finalized, the existing engines/services can implement them without creating another layer of duplicated business logic.
