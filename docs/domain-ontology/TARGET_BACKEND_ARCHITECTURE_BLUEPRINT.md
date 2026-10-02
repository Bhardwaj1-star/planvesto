# Planvesto Target Backend Architecture Blueprint

> Status: Target architecture derived from the code-first ontology, canonical domain model, rule, decision, state/event, knowledge-graph, and decision-trace audits.
>
> This is a refactoring blueprint. It does not authorize production-code changes by itself.

## 1. Objective

Reduce distributed business logic into a clear canonical backend without changing Planvesto's business meaning.

The target flow is:

```text
Financial Inputs
      ↓
Financial State
      ↓
Goals + Constraints + Investor Context
      ↓
Domain Rules / Assessments
      ↓
Knowledge: Strategy Definitions + Techniques + Components
      ↓
Applicability
      ↓
Strategy Architecture / Candidates
      ↓
Eligibility & Hard Gates
      ↓
Scenarios / Calculations
      ↓
Trade-offs / Multi-goal Allocation
      ↓
DecisionResult
      ↓
StrategyVersion
      ↓
ActionPlan
      ↓
Execution
      ↓
New FinancialState Snapshot
      ↺
Re-evaluation
```

## 2. Canonical Layers

### Domain Model
Owns business concepts and typed domain contracts.

Canonical concepts include PlanningUnit, FinancialState, Metric, MoneywheelResult, DefinedGoal, Constraint/Assessment, StrategyDefinition, TechniqueDefinition, StrategyComponent, StrategyArchitecture, EligibilityAssessment, Scenario, DecisionResult, StrategyRun, StrategyVersion, PrimaryStrategyState, ActionPlanItem and ActionDecisionRecord.

### Rules / Policy Layer
Owns explicit business rules and policy decisions. Rules must be named, typed, testable and have one authority. Separate hard gates from soft preferences.

### Knowledge Layer
Owns reusable financial knowledge: strategy definitions, techniques, components, compatibility and metadata. It must not contain investor-specific decisions.

### Decision Layer
Owns the decision pipeline:

`Applicability → Architecture → Eligibility → Adaptation → Scenario → Trade-off → Decision`.

`DecisionResult` is the sole authority for the recommendation. Ranking/display scores must not override hard feasibility or eligibility.

### Calculation / Simulation Layer
Owns deterministic financial calculations and, when later introduced, uncertainty/sensitivity simulation. Calculations must not decide business policy.

### Application / Orchestration Layer
Coordinates domain services, persistence and workflow. It should not duplicate domain rules.

### Persistence Layer
Stores canonical snapshots, versions, runs and execution/audit records. Persistence must not become a second business-rule layer.

## 3. Rule Architecture

Use one authoritative rule definition per business concept.

Rules should expose:

```text
Rule ID
Rule Version
Inputs
Condition
Severity / Gate Type
Assessment Output
Evidence
```

Standardize feasibility vocabulary to:

`PASS | CONDITIONAL | INFEASIBLE`

Do not allow alternate terms such as `constrained` to represent the same business state.

## 4. Decision Architecture

The decision engine should remain deterministic and explainable:

1. Retrieve applicable knowledge.
2. Compose candidate architectures.
3. Evaluate mandatory eligibility fits.
4. Generate required adaptations for conditional candidates.
5. Generate scenarios.
6. Evaluate multi-goal resource conflicts/trade-offs.
7. Produce `DecisionResult`.
8. Persist the run and provenance.
9. Commit only the selected strategy as `StrategyVersion`.

Hard constraints must gate candidates before preference/ranking logic. Ranking is comparative information, not decision authority.

## 5. State & Event Architecture

FinancialState is the canonical current-state snapshot and historical source of truth.

Relevant lifecycle events:

- financial input mutated
- goal defined/updated
- strategy run executed
- strategy selected
- strategy edited
- action status transitioned
- action completed

Critical invariant:

`ACTION_COMPLETED → new FinancialState snapshot → downstream invalidation/re-evaluation`.

The current implementation has a gap here: actual action state is recorded in action/audit data but does not yet become the canonical FinancialState snapshot.

## 6. Knowledge Graph Boundary

The knowledge graph is conceptual first; it does not require a graph database.

Core relationships:

```text
PlanningUnit → FinancialState
PlanningUnit → Goal
FinancialState → Metric / MoneywheelResult
Goal → Constraint Assessment
StrategyLibrary → StrategyDefinition / TechniqueDefinition / Component
Goal → StrategyArchitecture
StrategyArchitecture → EligibilityAssessment
EligibilityAssessment → DecisionResult
StrategyArchitecture → Scenario
StrategyRun → DecisionResult / Scenario
DecisionResult → StrategyVersion
StrategyVersion → ActionPlanItem
ActionPlanItem → ActionDecisionRecord
Action completion → FinancialState
```

Keep graph node definitions canonical under the domain model; do not duplicate domain contracts inside engines.

## 7. Decision Trace

Every decision should be explainable through an evidence chain:

`Input Snapshot → Rule Version → Calculation → Candidate → Eligibility → Scenario → Trade-off → DecisionResult → StrategyVersion → Action → Execution → New State`.

Required trace identifiers should be explicit rather than buried in generic metadata where practical.

Priority gaps identified by audit:

- StrategyRun needs explicit `financial_state_snapshot_id`.
- ActionPlanItem needs explicit `goal_id` where the action is goal-specific.
- Rule versions should be recorded consistently across rule families.
- Action completion must create/link a new FinancialState snapshot.

## 8. Canonical Ownership Rules

- One domain concept = one canonical model/contract.
- One business rule = one authoritative implementation.
- Engines calculate/evaluate; they do not redefine domain concepts.
- Services orchestrate; they do not duplicate rules.
- Catalogs describe reusable knowledge; they do not select for an investor.
- DecisionResult owns recommendation authority.
- FinancialState snapshot owns current financial-state truth.
- Versioned entities preserve historical decision context.

## 9. Known Consolidation Targets

The audits identified these concrete cleanup targets:

1. Consolidate duplicate `StrategyComponent` definitions.
2. Standardize feasibility vocabulary (`PASS | CONDITIONAL | INFEASIBLE`).
3. Consolidate duplicated priority-ranking concepts/rules under one authority.
4. Separate transient rule-assessment models from rule-engine implementation.
5. Make strategy-run → financial-state provenance explicit.
6. Make action-plan → goal provenance explicit where applicable.
7. Close action-completion → FinancialState feedback loop.
8. Record consistent rule-set versions in decision provenance.
9. Keep multi-goal allocation as a decision/trade-off concern rather than duplicating goal-priority rules.

## 10. What Not To Do Yet

Do not introduce microservices, Kafka/event infrastructure, a graph database, an external rule engine, or an AI-agent framework merely to implement this architecture.

First consolidate the existing Python backend around the canonical boundaries. Technology can be introduced later only where a concrete complexity or scale requirement justifies it.

Do not change Supabase schema as part of the ontology cleanup unless a separate schema migration is explicitly approved.

## 11. Refactoring Sequence

### Phase 1 — Canonical Contracts

Consolidate duplicate domain models, enums and value objects. Establish ownership without changing behavior.

### Phase 2 — Rule Consolidation

Move duplicated thresholds, priority rules and feasibility vocabulary behind authoritative rule contracts. Add/strengthen contract tests.

### Phase 3 — Decision Pipeline

Make applicability, architecture composition, eligibility, adaptation, scenario, trade-off and decision boundaries explicit and remove duplicated selection logic.

### Phase 4 — Provenance

Make snapshot/run/version/action identifiers explicit and establish the complete decision trace.

### Phase 5 — State Feedback

Close action completion → FinancialState snapshot → invalidation/re-evaluation.

### Phase 6 — Simplification

Remove obsolete wrappers, duplicate services, dead abstractions and pass-through layers only after behavior is protected by tests.

## 12. Acceptance Criteria

The refactor is successful when:

- Each canonical concept has one clear owner.
- Each business rule has one authoritative implementation.
- Strategy selection has one decision authority.
- Hard constraints cannot be overridden by ranking.
- A strategy decision can be traced back to its exact state, goal, rules, calculations and scenarios.
- A completed action produces an updated canonical financial state.
- Historical runs and strategy versions remain reproducible.
- Removing a module does not silently remove business logic because the same rule exists elsewhere.
- The resulting backend is simpler to understand without changing intended financial behavior.

## 13. Source Reports

This blueprint consolidates:

- `CODE_FIRST_DOMAIN_ONTOLOGY.md`
- `CANONICAL_DOMAIN_MODEL.md`
- `RULE_ENGINE_MODEL.md`
- `DECISION_MODEL.md`
- `STATE_EVENT_MODEL.md`
- `KNOWLEDGE_GRAPH_MODEL.md`
- `DECISION_TRACE_MODEL.md`
