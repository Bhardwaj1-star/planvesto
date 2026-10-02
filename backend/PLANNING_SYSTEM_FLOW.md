# Personalised Financial Planning System — Canonical Architecture & Flow

> This is the single working reference for the business architecture and runtime planning flow. Architecture/code must not be changed based on assumptions outside this document; when a business rule is locked, update this document first.

## 1. Source Blueprint and Canonical End-to-End Architecture

The Financial Planning Engine System Blueprint is the architectural baseline for this backend. It defines a dynamic Financial Decision Engine that uses actual financial state, goals, existing portfolio and proposed actions to construct strategies, calculate consequences, test scenarios, compare trade-offs and support the investor's decision.

The source blueprint's full decision loop is:

**Financial State** → **Goals** → **Constraints** → **Proposed Action / Problem** → **Strategy Engine** → **Calculation Engine** → **Scenario Engine** → **Probability / Uncertainty** → **Optimization Engine** → **Explainability** → **Investor Decision** → **Updated Financial State**

For implementation, **Financial Data** is the source layer feeding Financial State, while **Goal Feasibility** is an explicit planning stage derived from goal requirements and available financial resources before strategy evaluation.

Therefore the current implementation-level flow is:

**Financial Data** → **Financial State** → **Goals** → **Goal Feasibility** → **Constraints** → **Proposed Action / Problem** → **Strategy Engine** → **Calculation** → **Scenarios** → **Probability / Uncertainty** → **Optimization / Comparison** → **Explainability** → **Decision Options** → **Investor Decision** → **Updated Financial State**

A Report is a presentation/output layer around canonical decision outputs; it is not an additional decision engine.

Individual modules and services may implement multiple stages internally, but they must not create a competing business flow.

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

### Stage 6 — Proposed Action / Problem

The blueprint explicitly asks: **What am I considering?** An investor-proposed action or financial problem is translated into a testable object. Examples include changing contribution, adding a lump sum, changing a goal date/target, deploying cash, prepaying debt, changing allocation, or combining actions.

This is the decision context, not the strategy itself. The Strategy Engine generates the possible paths.

### Stage 7 — Strategy Engine

The Strategy Engine is the central goal-level strategy decision system.

Canonical internal flow:

Applicability → Eligible Strategy Set → Scenario Generation → Comparison → Architecture Composition → Decision Evaluation → Ranking → Recommendation

The Strategy Engine may also execute deterministic technique outputs required by the selected/composed strategy architecture.

The Strategy Engine is the authoritative source for strategy evaluation and recommendation. Services may orchestrate calls to it, but must not duplicate its business logic.

### Stage 8 — Calculation Engine

Calculation answers: **What does each strategy mathematically produce?** Reusable calculations quantify candidate strategies; reports and API handlers must not independently recreate them.

Examples include future value, required contribution/return, debt interest saved and portfolio/goal projections.

### Stage 9 — Scenario Engine

Scenario analysis asks: **What if conditions change?** Scenarios include baseline/what-if/customized assumptions such as lower/base/higher return, contribution levels, step-up rates, dates and return/volatility paths.

### Stage 10 — Probability / Uncertainty

Where implemented, this layer estimates outcome ranges/uncertainty and remains conceptually distinct from deterministic scenario calculation.

### Stage 11 — Optimization / Comparison

Optimization occurs after multiple strategies are generated and evaluated. It does not mean maximizing return. Comparison considers goal fit, cash-flow fit, liquidity, debt, portfolio, risk, flexibility, outcome quality and trade-offs.

### Stage 12 — Explainability

Explainability exposes why outcomes differ, including assumptions, evidence, consequences and trade-offs. Reports present this evidence but must not become an independent decision authority.

### Stage 13 — Decision Options / Decision Evaluation

Decision evaluation determines how candidate strategies perform against goals, financial state, constraints, priorities and trade-offs. A recommendation remains decision support.

**Strategy Recommendation ≠ Investor Decision.**

### Stage 14 — Investor Decision

The investor makes the final choice. The system may persist selected strategy/scenario/architecture/implementation parameters where supported.

### Stage 15 — Updated Financial State

After execution, the actual financial state becomes the next planning snapshot. The feedback loop is:

**Decision → Execution / Updated Data → Updated Financial State → Replanning**

### Stage 16 — Report

Reports present canonical planning outputs. Individual-goal reporting follows:

**Strategy Run → GoalReportService → Structured Goal Decision Report → PDF**

The report is a presentation layer over canonical calculation, scenario, comparison, decision and explainability outputs. It must not create an alternative business-logic path.

Two report scopes remain distinct:
1. **Individual Goal Decision Report** — one goal's financial position, calculation, feasibility/funding, strategies, scenarios, trade-offs, alternatives, assumptions, decision and provenance.
2. **Consolidated Financial Plan / Multi-Goal Report** — multiple goals, cross-goal allocation/conflicts, priorities, consolidated actions and overall plan outputs.

### Stage 17 — Investor Decision

The system provides decision support. The investor makes the final choice.

The system may persist selected strategy, scenario, architecture and implementation parameters. Therefore:

**Strategy Recommendation ≠ Investor Decision**

### Stage 18 — Updated Financial State

After execution, actual financial data becomes the next planning snapshot.

**Decision → Execution / Updated Data → Updated Financial State → Replanning**

Decision history should be preserved, and actual outcomes can be compared with the assumptions used by the strategy.

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