# Strategy Builder — Audit Index

## Purpose

This folder organizes the existing Strategy Builder audit for the **existing feature inventory**. The detailed Decision Engine audit is stored in this Strategy-Builder folder; source audit content is preserved.

## Audit source map

| Order | Audit area | Existing source document | Main code authority recorded by the audit |
|---|---|---|---|
| 00 | Consolidated design and navigation | [Decision Engine Design Summary](00-DECISION_ENGINE_DESIGN_SUMMARY.md) | End-to-end flow and nine decision domains |
| 00.5 | Cross-cutting reverification and gaps | [Cross-Cutting Reverification & Gap Audit](00.5-CROSS_CUTTING_REVERIFICATION_AND_GAP_AUDIT.md) | Duplicate authorities, legacy IDs, runtime order, dependencies |
| 00.6 | Rule ownership decisions | [KEEP / MERGE / REPLACE / REMOVE / NEW Audit](00.6-RULE_OWNERSHIP_KEEP_MERGE_REPLACE_REMOVE_NEW_AUDIT.md) | Rule ownership and migration decisions |
| 01 | Strategy applicability | [Step 01](01-STRATEGY_APPLICABILITY_CURRENT_STATE_AND_RECOMMENDATION.md) | `backend/engines/strategy/applicability.py`, StrategyRuleEngine |
| 02 | Hard constraints | [Step 02](02-HARD_CONSTRAINTS_CURRENT_STATE_AND_RECOMMENDATION.md) | `backend/engines/constraints/*`, ConstraintAggregator |
| 03 | Eight eligibility fits | [Step 03](03-8_ELIGIBILITY_FITS_CURRENT_STATE_AND_RECOMMENDATION.md) | `backend/rules/eligibility.py`, `backend/engines/strategy/eligibility.py` |
| 04 | Strategy selection | [Step 04](04-STRATEGY_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md) | `backend/engines/strategy/decision.py`, `backend/rules/strategy_decision.py` |
| 05 | Variant selection | [Step 05](05-22-VARIANT_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md) | `backend/library/strategies/variants.py`, `backend/engines/strategy/variant_selector.py` |
| 06 | Technique selection | [Step 06](06-TECHNIQUE_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md) | `backend/library/strategies/techniques_canonical.py`, technique engine |
| 07 | Architecture composition | [Step 07](07-ARCHITECTURE_COMPOSITION_CURRENT_STATE_AND_RECOMMENDATION.md) | `backend/engines/strategy/composition.py` |
| 08 | Stress and resilience | [Step 08](08-STRESS_RESILIENCE_CURRENT_STATE_AND_RECOMMENDATION.md) | `backend/engines/strategy/scenario.py`; formal stress gate remains incomplete per audit |
| 09 | Final decision and recommendation | [Step 09](09-FINAL_DECISION_AND_RECOMMENDATION_CURRENT_STATE_AND_RECOMMENDATION.md) | `DecisionResult` and recommendation layer |

## Canonical business boundary

- The documents describe current code, gaps, and a proposed target. They do **not** establish that the target flow is already implemented.
- The target flow is a design proposal; rules are not frozen for V1.
- Goal Funding and goal-funding feasibility belong to Goal Planner; do not treat Goal Funding as a fifth Strategy Builder strategy in the canonical target model.
- Strategy → Variant → Technique → Method/Policy → Architecture → Solution → Action.
- Technique is not Solution; Recommendation, Investor Decision, Accepted Plan, Action Plan, and Execution are distinct lifecycle states.
- Applicability is not viability. A failed standard-candidate set may legitimately result in no acceptable strategy.
- The cross-cutting and rule-ownership audits are supporting audit documents, not additional decision stages.

## Audit limitations preserved

The source audit explicitly identifies unresolved issues, including legacy strategy identifiers, split rule ownership, the current runtime order differing from the target order, variant selection occurring inside recommendation, incomplete formal stress/resilience gating, and investor-priority ownership. These remain unresolved until verified and deliberately changed; this index does not claim they are fixed.

## Relationship to the existing feature overview

The broader feature overview remains at `docs/feature/Strategy-Builder.md`. This index is the navigation layer for the detailed Strategy Builder decision audit; it does not replace the source audit documents or the feature overview.
