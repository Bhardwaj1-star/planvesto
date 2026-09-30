# Ontology → Implementation Mapping

## Purpose

Map the canonical Planvesto ontology to the existing backend implementation before any production-code refactor.

This document is an implementation map, not a new ontology. Existing code remains authoritative evidence; canonical ontology remains the target semantic model.

## Mapping Rules

- One canonical concept must have one clear domain owner.
- Existing classes/functions may implement more than one concept temporarily; mark this as `SPLIT_REQUIRED`.
- Multiple implementations of one concept are `CONSOLIDATE`.
- Code with no canonical semantic role is `REMOVE_CANDIDATE` only after dependency verification.
- Do not change behavior during mapping.

## Status Vocabulary

`DIRECT` — existing implementation maps cleanly.

`PARTIAL` — implementation covers only part of the canonical concept.

`DUPLICATE` — multiple implementations represent the same concept.

`SPLIT_REQUIRED` — one implementation currently mixes multiple concepts.

`MISSING` — canonical concept has no adequate implementation.

`IMPLICIT` — concept exists only through procedural logic/data structures.

## Target Mapping Matrix

| Canonical Concept | Current Implementation Evidence | Status | Canonical Owner | Refactor Direction |
|---|---|---|---|---|
| PlanningUnit | Existing investor/planning-context models and services | PARTIAL | Domain planning model | Consolidate planning context |
| FinancialState | Existing financial-state/models + calculations | PARTIAL | Financial State domain | Establish one state contract |
| FinancialMetric | Existing calculation/metric helpers | PARTIAL | Metric/value layer | Consolidate derived metrics |
| InvestorProfile | Existing risk/profile inputs | PARTIAL | Investor/Profile domain | Separate profile context from state |
| Goal | Existing goal models/services | DIRECT/PARTIAL | Goal domain | Keep one canonical goal contract |
| GoalFunding | Existing goal projection/funding calculations | PARTIAL | Goal planning | Extract funding state from generic goal logic |
| Constraint | Existing rule/constraint models and checks | PARTIAL/DUPLICATE | Constraint/Policy domain | Consolidate constraint authority |
| MoneywheelAssessment | Existing Moneywheel implementation | DIRECT/PARTIAL | Diagnostics domain | Keep diagnostics as assessment, not state |
| FinancialMetric / Moneywheel Indicator | Existing Moneywheel ratio functions | DIRECT | Metric layer | Standardize metric contracts and formulas |
| StrategyDefinition | Existing strategy/catalog definitions | PARTIAL | Knowledge layer | Separate reusable knowledge from investor decisions |
| StrategyFamily | Existing strategy categorization | PARTIAL | Knowledge layer | Consolidate taxonomy |
| TechniqueDefinition | Existing technique concepts | PARTIAL | Knowledge layer | Separate techniques from strategies |
| StrategyComponent | Multiple existing definitions | DUPLICATE | Knowledge layer | Consolidate to one canonical component model |
| StrategyArchitecture | Existing strategy composition structures | PARTIAL | Strategy domain | Make composition explicit |
| EligibilityAssessment | Existing eligibility/rule evaluation | PARTIAL | Evaluation domain | Standardize PASS/CONDITIONAL/INFEASIBLE |
| Scenario | Existing scenario/projection logic | PARTIAL | Simulation domain | Separate assumptions/calculation from decision |
| TradeOff | Existing priority/allocation logic | IMPLICIT/DUPLICATE | Decision domain | Make trade-off evaluation explicit |
| Decision | Existing strategy selection/orchestration | PARTIAL | Decision domain | Establish one decision authority |
| StrategyRun | Existing strategy execution/run context | PARTIAL | Decision domain | Make state snapshot + rule versions explicit |
| StrategyVersion | Existing selected strategy/version concepts | PARTIAL | Strategy lifecycle | Separate decision result from committed version |
| ActionPlan | Existing planning/action structures | PARTIAL | Execution domain | Make implementation output explicit |
| Action | Existing action/audit structures | PARTIAL | Execution domain | Link action to goal/version and lifecycle |
| FinancialStateSnapshot | Existing snapshots/history where available | PARTIAL/MISSING | State history | Make decision provenance explicit |
| Rule / Policy | Existing rule modules/services | DUPLICATE/PARTIAL | Rule layer | One authoritative rule contract |
| RuleAssessment | Existing rule evaluation outputs | PARTIAL | Rule layer | Standardize assessment evidence |
| Event | Existing workflow/audit/event-like records | IMPLICIT | Event/state layer | Define only events with real domain meaning |
| DecisionTrace | Existing audit/provenance metadata | PARTIAL/MISSING | Trace layer | Build explicit trace chain |

## Critical Consolidation Targets

### 1. StrategyComponent

The audits identify duplicate component representations. Consolidate them before adding new strategy abstractions.

### 2. Feasibility Vocabulary

Use one canonical result vocabulary:

`PASS | CONDITIONAL | INFEASIBLE`

Do not maintain parallel terms for the same semantic result.

### 3. Priority / Ranking

Multiple priority/ranking concepts must not independently decide strategy selection. Establish one decision-layer authority for preference ordering and multi-goal trade-offs.

### 4. Rule Authority

Thresholds and business conditions currently distributed across rules/services/calculations must map to one named rule authority. Calculation functions may calculate; they must not silently redefine policy.

### 5. Decision Provenance

Every StrategyRun must be attributable to a FinancialState snapshot, goal/context, rule-set version, calculations/scenarios and resulting Decision.

### 6. Action → State Feedback

Completed actions must eventually produce/link a new FinancialState snapshot and trigger appropriate re-evaluation. Until implemented, mark this relationship as `MISSING/IMPLICIT`, not as already solved.

## Refactoring Order

1. Freeze canonical ontology.
2. Freeze ownership of each concept.
3. Consolidate duplicate domain contracts.
4. Consolidate rule authority.
5. Separate knowledge from investor-specific decisions.
6. Make Decision the single selection authority.
7. Make StrategyRun and DecisionTrace provenance explicit.
8. Close Action → FinancialState feedback loop.
9. Remove obsolete implementations only after tests prove no semantic loss.

## Guardrail

This mapping does **not** authorize production changes. Before each refactor, verify the exact current file/class/function and its callers against the repository at that point in time.
