# Personalised Financial Planning System — Canonical Architecture & Flow

> This is the single working reference for the business architecture and runtime planning flow. Architecture/code must not be changed based on assumptions outside this document; when a business rule is locked, update this document first.

## 1. Canonical End-to-End Architecture

**Financial Data** → **Financial State** → **Goals** → **Goal Feasibility** → **Constraints** → **Strategy Engine** → **Scenarios** → **Comparison** → **Decision** → **Report** → **Investor Decision**

This is the primary architecture. Individual modules and services may implement multiple stages internally, but they must not create a competing business flow.

### Stage 1 — Financial Data

Raw investor/family financial inputs: income, expenses, assets, liabilities, family/dependents, existing commitments and other explicitly collected financial inputs.

Financial Data is source information. It is not itself a financial decision.

### Stage 2 — Financial State

Financial Data is normalized and calculated into the investor's current financial reality.

Typical outputs include net worth, total assets, total liabilities, cash-flow position, surplus/available amount, savings/investment indicators, financial ratios and health indicators.

Canonical backend ownership:
- backend/engines/financial_state/
- backend/services/financial_state_service.py
- backend/models/financial_state.py
- backend/data/financial_state_repository.py

Financial State is an input to downstream goal and strategy decisions.

### Stage 3 — Goals

The investor's defined financial objectives are represented as versioned DefinedGoal objects. A goal contains the information required to evaluate what must be funded/achieved, including target, horizon and goal-specific calculation inputs.

Goal definition is distinct from strategy selection.

### Stage 4 — Goal Feasibility

Goal Feasibility answers: given the defined goal and available financial state, what is required to fund the goal and what funding gap/surplus exists?

Relevant outputs include future target/required amount, projected mapped resources, funding gap or surplus, required monthly contribution, funding status and feasibility evidence where available.

Goal Feasibility is a first-class planning stage. It is not merely a report section.

Important distinction: Goal Feasibility is not the same as Strategy Feasibility.
- Goal Feasibility evaluates whether the goal's funding requirement is supportable from the financial reality.
- Strategy Feasibility evaluates whether a particular strategy architecture is viable/appropriate for that goal under its constraints.

Unavailable inputs must not be silently converted into a false feasible/infeasible conclusion; feasibility may be represented as unknown where required financial state is unavailable.

### Stage 5 — Constraints

Constraints combine investor circumstances, goal context, financial rules and explicitly defined priorities.

Canonical mechanisms include RuleEngine, ConstraintAggregator and ConstraintSet.

Constraints can play different decision roles: eligibility/hard constraint, ranking input, recommendation-only evidence and explanatory evidence.

Constraints are supplied to the Strategy Engine; they do not independently make the final investor decision.

### Stage 6 — Strategy Engine

The Strategy Engine is the central goal-level strategy decision system.

Canonical internal flow:

Applicability → Eligible Strategy Set → Scenario Generation → Comparison → Architecture Composition → Decision Evaluation → Ranking → Recommendation

The Strategy Engine may also execute deterministic technique outputs required by the selected/composed strategy architecture.

The Strategy Engine is the authoritative source for strategy evaluation and recommendation. Services may orchestrate calls to it, but must not duplicate its business logic.

### Stage 7 — Scenarios

Scenarios represent alternative assumption/implementation states used to examine outcomes. The current engine supports baseline, what-if and investor-customized scenarios.

### Stage 8 — Comparison

The Strategy Engine builds the comparison matrix across candidate strategies/scenarios. Comparison is an explicit decision-support stage, not a separate competing strategy system.

### Stage 9 — Decision

Decision Evaluation determines how candidate strategies/architectures perform against goal fit, financial-state fit, horizon, funding/feasibility evidence, constraints, investor priorities, trade-offs and architecture/technique evidence where applicable.

Decision output feeds ranking and recommendation. The recommendation must be derived from canonical decision output.

### Stage 10 — Report

Reports present canonical planning outputs for the investor.

Individual-goal reporting follows:

Strategy Run → GoalReportService → Structured Goal Decision Report → PDF

GoalReportService is the canonical individual-goal report authority.

Reports consume canonical outputs. Reporting code must not create an alternative strategy/calculation/decision path.

Two report scopes must remain distinct:
1. Individual Goal Decision Report — one defined goal, its feasibility/funding result, strategy evaluation, scenarios/comparison, decision/recommendation, constraints, trade-offs, assumptions/provenance and investor-selection context.
2. Consolidated Financial Plan / Multi-Goal Report — multiple goals, cross-goal resource allocation, conflicts/trade-offs, resolved priorities, consolidated actions and overall financial-plan outputs.

These report scopes may compose one another but must not duplicate their underlying decision logic.

### Stage 11 — Investor Decision

The system recommendation is decision support, not the investor's final decision.

The investor may select/persist strategy, scenario, architecture and implementation parameters. Canonical persisted selection fields include selected_strategy_id, selected_scenario_id, selected_architecture, selected_implementation_parameters and selection_timestamp.

Therefore: Strategy Recommendation ≠ Investor Decision.

## 2. Strategy Feasibility vs Goal Feasibility

These terms must not be collapsed during backend cleanup.

### Goal Feasibility

Question: Can the defined financial objective be funded under the investor's current/projected financial resources?

Evidence includes future target, mapped resources, funding gap, required contribution and funding status.

### Strategy Feasibility

Question: Is this specific strategy architecture viable/appropriate for this goal under the financial state and constraints?

The Strategy Engine represents this through architecture/decision feasibility evidence and statuses such as feasible, conditional and infeasible.

Eligibility Fit is a feasibility/evidence layer, not the final decision-maker. A conditional strategy may be adapted and re-checked.

## 3. Multi-Goal Architecture

Multi-goal planning is a cross-goal orchestration layer. It does not replace the canonical goal-level chain.

For multiple goals:

Financial State → Goals → Goal Feasibility → Constraints → individual Strategy Engine execution per goal → Cross-Goal Orchestration → Resource Allocation / Conflict Resolution → Consolidated Financial Plan → Report → Investor Decision

The Multi-Goal layer owns goal prioritisation/reprioritisation, competition for shared resources, existing-asset allocation, liquidity/resource conflicts, cross-goal trade-offs, consolidated allocation and overall plan assembly.

It must not duplicate the individual-goal Strategy Engine.

## 4. Canonical Backend Responsibility Map

| Responsibility | Canonical ownership |
|---|---|
| Raw financial inputs | Financial Data / source services |
| Financial-state calculation | FinancialStateEngine |
| Financial-state persistence | FinancialStateSnapshotRepository |
| Goal definition/calculation | DefinedGoal / Goal domain |
| Goal feasibility evidence | Goal calculation + funding/feasibility outputs |
| Constraint evaluation | RuleEngine + ConstraintAggregator |
| Strategy applicability | Strategy Engine |
| Scenario generation | Strategy Engine scenario module |
| Strategy comparison | Strategy Engine comparison module |
| Strategy architecture composition | Strategy Engine composition module |
| Decision evaluation | Strategy Engine decision module |
| Ranking | Strategy Engine ranking module |
| Recommendation | Strategy Engine recommendation module |
| Individual-goal report | GoalReportService |
| Cross-goal orchestration | Multi-Goal Orchestration layer |
| Consolidated financial plan | FinancialPlanService / consolidated-plan layer |
| Investor selection | Strategy selection/persistence flow |

## 5. Architectural Boundaries

Services orchestrate application workflows, repositories and engines. They must not become a second implementation of underlying business logic.

Engines own deterministic domain calculations, rules, strategy evaluation and decision logic appropriate to their domain.

Reports consume canonical outputs and must not silently recalculate or replace business decisions.

PDF/HTML/export layers are presentation adapters. They serialize canonical report data and must not become independent business-logic authorities.

Compatibility routes/helpers are allowed only when an active consumer still requires them, and they must delegate to the canonical implementation.

## 6. Locked Product Rules

1. Planvesto is goal-first.
2. Goal Feasibility is a first-class stage before strategy evaluation.
3. Strategy Feasibility is distinct from Goal Feasibility.
4. Eligibility Fit is feasibility/evidence, not the final decision-maker.
5. Conditional strategies may be adapted and re-checked.
6. Failed strategies after reasonable adaptation are removed.
7. Multiple eligible strategies can produce multiple strategy variants; Decision Evaluation selects/recommends among them.
8. Risk capacity is primarily for investment implementation / portfolio construction, not the primary goal-strategy selection factor.
9. Goal Reprioritisation & Resource Allocation is a Multi-Goal Orchestration layer.
10. Goal Funding + Long-Term Accumulation are unified under Goal Funding.
11. Income Transition is a Goal Funding variant.
12. Progressive De-risking and Capital Preservation remain separate strategies.
13. Debt Reduction and Credit Utilisation remain separate strategies.
14. Global investor constraints can affect evaluation of every candidate strategy.
15. The investor retains final decision authority.

## 7. Cleanup Rule

When auditing or deleting backend code, map every implementation to the architecture above.

The correct question is not whether two files have similar names. The correct question is whether a file implements a responsibility that already has a canonical owner.

Classification:
- CANONICAL — authoritative implementation
- COMPATIBILITY — required consumer-facing alias that delegates to canonical
- LEGACY — old duplicate implementation
- DEAD — no active architectural/runtime role
- DOMAIN LOGIC — legitimate goal/domain-specific behavior

Only confirmed LEGACY and DEAD implementations should be deleted.

## 8. Current Architecture Status

The repository contains the major layers required by this architecture: Financial State engine/service/repository; Defined Goal domain; goal calculation/funding outputs; constraint engine/aggregator; Strategy Engine with applicability, scenarios, comparison, composition, decision, ranking and recommendation; technique execution; Individual Goal Report Service; Multi-Goal orchestration components; Consolidated Financial Plan service; and investor strategy selection persistence.

The cleanup phase must now verify whether each implementation is the single canonical owner of its mapped responsibility or a duplicate/compatibility implementation.