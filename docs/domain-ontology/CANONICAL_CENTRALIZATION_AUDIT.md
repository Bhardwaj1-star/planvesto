# Canonical Centralization Audit

## Purpose

This document defines the remaining work required to make Planvesto's domain vocabulary, business rules, decision authority, and API contracts canonically centralized.

The objective is not to make every file depend on one module. The objective is:

> Each business concept has one authoritative definition, one canonical vocabulary, one normalization path, and one clearly defined decision authority.

Compatibility aliases may remain where required for persisted legacy data, but they must not become competing business definitions.

## Current Architecture Principle

    Raw / Legacy Input
          ↓
    Canonical Normalization
          ↓
    Canonical Domain Model
          ↓
    Business Rules
          ↓
    Engine / Decision Layer
          ↓
    Authoritative Output
          ↓
    Persistence / API / UI

A downstream layer must consume canonical values rather than reimplementing normalization or business semantics.

# 1. Goal Taxonomy

Status: MOSTLY CANONICAL

### Current authority

- backend/rules/goals.py
  - GOAL_TYPE_ALIASES
  - CANONICAL_GOAL_NAMES
  - canonical_goal_type()
  - canonical_goal_name()
  - canonical_goal_priority()

### Required state

All goal-type normalization must pass through canonical_goal_type().

### Remaining work

- [ ] Replace direct GOAL_TYPE_ALIASES.get(...) usage in downstream engines with canonical_goal_type().
- [ ] Audit all raw goal_type comparisons.
- [ ] Audit frontend goal-type literals against the canonical backend taxonomy.
- [ ] Verify every legacy alias is either a compatibility alias or a valid canonical type.
- [ ] Resolve the documented conflict around passive_income, debt_repayment, and philanthropy before changing taxonomy.

Rule: No engine should maintain its own goal-type alias map.

# 2. Goal Name vs Goal Type

Status: CANONICAL DIRECTION ESTABLISHED

These must remain separate:

    goal_type = canonical domain category
    goal_name = investor's human-readable goal

Example:

    goal_type = education
    goal_name = Daughter MBA

Do not turn names such as Child Education into competing goal types.

### Audit

- [ ] Search for code that uses goal_name as a substitute for goal_type.
- [ ] Search for business rules branching on goal-name strings.
- [ ] Ensure reports/UI display the real goal_name while engines use canonical goal_type.

# 3. Goal Priority

Status: CANONICAL

Authority:

    rules/goals.py
        ↓
    canonical_goal_priority()
        ↓
    rules/multi_goal.py
        ↓
    get_priority_rank()

### Remaining audit

- [ ] Search for local priority maps.
- [ ] Search for numeric priority rankings outside get_priority_rank().
- [ ] Remove any remaining direct string ordering assumptions.

# 4. Funding Status

Status: CONFLICTING / REQUIRES DOMAIN SEPARATION

Current goal-level vocabulary:

    Shortfall
    On Track
    Overfunded

Current multi-goal allocation vocabulary:

    fully_funded
    partially_funded
    unfunded
    within_surplus
    surplus_shortfall
    requires_review

These may represent different semantic layers and should not be blindly merged.

### Required work

- [ ] Define GoalFundingStatus.
- [ ] Define AllocationFundingStatus.
- [ ] Document the semantic boundary.
- [ ] Rename ambiguous fields/types where required.
- [ ] Ensure APIs do not expose two different meanings under an indistinguishable funding_status contract.
- [ ] Audit frontend consumers.

Rule: Different domain meanings must not share an ambiguous canonical type merely because they use the same English word.

# 5. Feasibility Status

Status: CONFLICTING / REQUIRES DOMAIN SEPARATION

Current vocabularies include:

    feasible
    conditional
    infeasible

and:

    feasible
    constrained
    infeasible

### Required work

- [ ] Identify whether conditional and constrained are actually the same domain concept.
- [ ] If same: create one canonical vocabulary and migrate consumers.
- [ ] If different: create explicit domain-specific types.
- [ ] Audit Strategy Builder, allocation, orchestration, reports, and frontend API types.

Rule: Never silently equate two status values because their names appear similar.

# 6. Constraint Vocabulary

Status: CANONICAL MODEL EXISTS; RULE OWNERSHIP NEEDS CLEANUP

Canonical model:

    backend/engines/constraints/models.py
    CanonicalConstraint
    ConstraintSet
    ConstraintCheckResult

Current architecture:

    Financial Fact / Metric
            ↓
    Diagnostic Evidence
            ↓
    Goal-specific Business Rule
            ↓
    Constraint Result
            ↓
    Planning Effect

### Required work

- [ ] Ensure financial ratio status never becomes a hard planning constraint merely because it is critical.
- [ ] Ensure hard effects originate from explicit goal-specific constraint rules.
- [ ] Audit every adapter into CanonicalConstraint.
- [ ] Remove duplicated constraint semantics from legacy adapters where safe.

# 7. Constraint Thresholds

Status: DUPLICATED / REQUIRES CENTRALIZATION

Examples include emergency reserve, debt-to-income, savings, and other Moneywheel / financial-health thresholds.

Current ownership is spread across:

    backend/rules/constraints.py
    backend/rules/moneywheel.py
    backend/engines/constraints/evaluator.py

### Required state

    Canonical Threshold Definition
              ↓
         Moneywheel
              ↓
      Constraint Evaluator
              ↓
     Financial Diagnostics
              ↓
       Strategy Decision

### Required work

- [ ] Identify every threshold definition.
- [ ] Select the authoritative owner for each threshold.
- [ ] Replace duplicated literals with imports/references.
- [ ] Keep compatibility aliases only where necessary.
- [ ] Add tests proving all consumers use the same threshold.

# 8. Moneywheel Domain

Status: CANONICAL CONTRACT ESTABLISHED

Current backend contract:

### 9 ratios

    savings_rate
    liquid_asset_ratio
    debt_to_income_ratio
    leverage_ratio
    financial_asset_ratio
    insurance_coverage_ratio
    goal_funding_ratio
    future_funding_ratio
    required_rate_of_return

### 2 rules

    expense_coverage
    emergency_coverage

### Required work

- [x] Backend canonical ratio contract.
- [x] Legacy snapshot normalization.
- [x] Frontend aligned to 9 ratios + 2 rules.
- [ ] Audit remaining legacy aliases in rules/moneywheel.py.
- [ ] Ensure aliases are compatibility-only and cannot become new canonical output.
- [ ] Ensure thresholds are sourced from the canonical rule layer.

# 9. Strategy Library

Status: CANONICAL

Required authority:

    Strategy Registry
          ↓
    Strategy Definition
          ↓
    Strategy ID
          ↓
    Strategy Architecture

### Required work

- [ ] Search for hardcoded strategy IDs outside the canonical registry.
- [ ] Search for duplicated strategy metadata.
- [ ] Search for frontend strategy names that are not API-derived.
- [ ] Ensure strategy IDs never depend on display names.

# 10. Technique Library

Status: CANONICAL DIRECTION; AUDIT REQUIRED

Techniques such as progressive de-risking, bucketing, laddering, and glide path must remain techniques, not strategy identities.

### Required work

- [ ] Audit technique IDs.
- [ ] Remove hardcoded technique names outside the canonical technique registry.
- [ ] Verify Strategy Architecture stores techniques as composition data.
- [ ] Ensure technique changes do not change canonical architecture identity.

# 11. Solution Library

Status: AUDIT REQUIRED

### Required work

- [ ] Identify canonical solution IDs.
- [ ] Find duplicate solution definitions.
- [ ] Find hardcoded solution names in engines/UI.
- [ ] Ensure solution metadata comes from the library.
- [ ] Keep product selection separate from strategy identity.

# 12. Strategy Architecture Identity

Status: CANONICAL

Authority: canonical_architecture_id(goal_id, primary_strategy_id)

Identity must be independent of supporting strategies, techniques, solutions, and implementation parameters.

### Required work

- [x] Deterministic architecture identity.
- [x] Composition-independent identity.
- [x] Legacy architecture normalization.
- [ ] Audit all architecture ID generation for alternate implementations.

Rule: Only the canonical architecture identity function may generate architecture IDs.

# 13. Strategy Recommendation Authority

Status: CANONICAL

The authoritative recommendation is the Strategy Decision output: recommended_strategy_id, recommended_scenario_id, and recommended_architecture.

### Required work

- [ ] Search for UI/service logic that uses ranking position as recommendation authority.
- [ ] Search for is_latest or latest-run logic influencing strategy decisions.
- [ ] Search for fallback recommendation logic outside the decision engine.

Rule: Ranking is evidence. Recommendation is decision output.

# 14. Strategy Run vs StrategyVersion

Status: CANONICAL DIRECTION

Required authority:

    Strategy Run
        = evaluation/history

    StrategyVersion
        = finalized implementation authority

### Required work

- [ ] Search all report endpoints for latest-run dependency.
- [ ] Search all Action Plan endpoints for latest-run dependency.
- [ ] Search all UI flows for is_latest decision logic.
- [ ] Verify only finalized StrategyVersion can become source of truth for Report + Action Plan.

# 15. Implementation Parameters

Status: CANONICAL DIRECTION

Required model:

    Strategy
       ↓
    Architecture
       ↓
    Implementation Parameters
       ↓
    StrategyVersion

### Required work

- [ ] Audit implementation parameter keys per strategy.
- [ ] Ensure parameters are strategy-specific.
- [ ] Remove generic parameter assumptions from frontend.
- [ ] Ensure finalized parameters are immutable through StrategyVersion.
- [ ] Ensure report/action plan consume the finalized snapshot.

# 16. Eligibility

Status: PARTIALLY CENTRALIZED

Canonical status model exists: PASS, CONDITIONAL, FAIL.

### Remaining issue

Some eligibility code directly consumes goal aliases rather than using the canonical normalization function.

### Required work

- [ ] Replace direct alias-map access with canonical normalization.
- [ ] Audit all eligibility status literals.
- [ ] Ensure eligibility is not reconstructed independently by frontend.
- [ ] Ensure hard constraints and eligibility remain distinct concepts.

# 17. Decision Roles

Status: CANONICAL MODEL; LOCATION CLEANUP REQUIRED

Canonical roles include:

    HARD_CONSTRAINT
    ELIGIBILITY
    RANKING_INPUT
    RECOMMENDATION_ONLY
    ARCHITECTURE_CONSTRAINT
    EXPLANATORY_EVIDENCE

### Required work

- [ ] Move domain ownership of DecisionRole to the canonical domain-model layer if appropriate.
- [ ] Remove duplicate role definitions.
- [ ] Ensure every rule has exactly one authority role.
- [ ] Audit role interpretation across Rule Engine and Constraint Engine.

# 18. Financial Metrics

Status: AUDIT REQUIRED

For every financial metric, identify:

    Metric ID
    Formula
    Input contract
    Unit
    Status classification
    Threshold
    Owner
    Consumers

### Audit specifically for

- [ ] duplicate formulas
- [ ] duplicate metric IDs
- [ ] inconsistent units
- [ ] percentage vs decimal mismatches
- [ ] scalar vs structured financial-state values
- [ ] duplicated classifications
- [ ] duplicated thresholds

# 19. Financial State Shape

Status: REQUIRES CONTRACT AUDIT

A recent production failure demonstrated the risk of total_liabilities arriving as a structured object while downstream decision logic expected a scalar.

### Required work

- [ ] Define canonical financial-state value representation.
- [ ] Centralize scalar extraction/normalization.
- [ ] Audit all engines consuming financial state.
- [ ] Reject local ad-hoc extraction logic.
- [ ] Add contract tests for structured and scalar legacy representations.

# 20. Action Plan

Status: CANONICAL USER-JOURNEY DIRECTION

Required flow:

    Goal
      ↓
    Selected StrategyVersion
      ↓
    Action Plan
      ↓
    Execution Points
      ↓
    Status
      ↓
    Progress

### Required work

- [ ] Ensure selected StrategyVersion is the only source of action-plan authority.
- [ ] Ensure no latest StrategyRun dependency remains.
- [ ] Keep missing actions explicit.
- [ ] Keep cancelled actions explicit as skipped/cancelled rather than silently deleting them.
- [ ] Audit action-status vocabulary against the backend canonical model.

# 21. Report

Status: CANONICAL DIRECTION

Required flow:

    Goal
      ↓
    Selected StrategyVersion
      ↓
    Goal Report

### Required work

- [ ] Ensure every goal uses the same report contract.
- [ ] Ensure goal-specific values populate the generic report structure.
- [ ] Remove legacy latest-run report dependencies.
- [ ] Keep legacy routes only as compatibility wrappers.
- [ ] Ensure PDF and API report sources resolve to the same StrategyVersion authority.

# 22. Frontend ↔ Backend Domain Contracts

Status: AUDIT REQUIRED

Frontend may have TypeScript representations of backend types, but it must not become a second business-rule authority.

Audit all frontend goal types, priorities, funding statuses, feasibility statuses, eligibility statuses, strategy IDs, scenario IDs, action statuses, Moneywheel ratios/rules, and report types.

Rule:

    Backend = domain/business authority
    Frontend = presentation/API consumer

Frontend should not invent a competing canonical vocabulary.

# 23. Legacy Aliases

Status: REQUIRED COMPATIBILITY LAYER

Legacy aliases are allowed for persisted historical data, backward-compatible APIs, and old snapshots.

Required direction:

    Legacy Alias
        ↓
    Canonical Value

### Required work

- [ ] Inventory all aliases.
- [ ] Mark each alias as compatibility-only.
- [ ] Remove aliases that are no longer required.
- [ ] Ensure canonical outputs never emit legacy identifiers.

# 24. Hardcoded Domain Strings

Status: AUDIT REQUIRED

Search the repository for hardcoded goal types, strategy IDs, technique IDs, solution IDs, priority values, status values, constraint IDs, Moneywheel ratio IDs, scenario types, action statuses, and report types.

Classify each occurrence as:

    CANONICAL REFERENCE
    UI LABEL
    TEST FIXTURE
    COMPATIBILITY ALIAS
    BUSINESS LOGIC LEAK

Only BUSINESS LOGIC LEAK requires immediate architectural cleanup.

# 25. Documentation Synchronization

Status: REQUIRED

The domain ontology documentation contains some historical findings that no longer match the current implementation.

### Required work

- [ ] Refresh docs/domain-ontology/CODE_FIRST_DOMAIN_ONTOLOGY.md.
- [ ] Mark resolved findings as resolved.
- [ ] Remove obsolete architecture descriptions.
- [ ] Document the final canonical authority for every major domain concept.
- [ ] Keep this audit document as the outstanding-work tracker.

# Canonicalization Completion Criteria

The system should be considered canonically centralized when:

1. Every major business concept has one authoritative definition.
2. Every legacy representation maps to exactly one canonical representation.
3. No downstream engine reimplements normalization.
4. No two domain layers use the same field name for different semantics without explicit naming.
5. Thresholds have one authoritative owner.
6. Strategy IDs have one authoritative registry.
7. Architecture IDs have one authoritative generator.
8. Recommendation has one authoritative decision source.
9. StrategyVersion has one authoritative finalized state.
10. Report and Action Plan consume StrategyVersion rather than history.
11. Frontend consumes backend domain contracts rather than inventing business rules.
12. Legacy compatibility code cannot become a competing source of truth.
13. Tests enforce canonicalization at the boundaries.
14. Documentation matches the actual code architecture.

# Recommended Audit Order

Do not refactor everything at once.

    1. Goal taxonomy
           ↓
    2. Status vocabularies
       - Funding
       - Feasibility
       - Eligibility
           ↓
    3. Constraint definitions
           ↓
    4. Threshold ownership
           ↓
    5. Financial metrics
           ↓
    6. Financial State contract
           ↓
    7. Strategy / Technique / Solution registries
           ↓
    8. Decision authority
           ↓
    9. StrategyVersion authority
           ↓
    10. Frontend API contracts
           ↓
    11. Legacy aliases
           ↓
    12. Documentation synchronization

## Important

This document is an audit and worklist, not permission to modify every item immediately.

For each item:

    Audit
      ↓
    Identify authority
      ↓
    Identify duplicates/conflicts
      ↓
    Define canonical semantics
      ↓
    Add regression tests
      ↓
    Refactor
      ↓
    Verify CI

No schema migration or frontend redesign should be introduced merely to achieve canonicalization unless a separate business decision explicitly requires it.