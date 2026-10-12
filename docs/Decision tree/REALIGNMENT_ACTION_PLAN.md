# Decision Tree — Short Alignment & Fix Plan

**Purpose:** One short working list for bringing the current code and docs in line with the Real-Life Decision Cases.  
**Business authority:** `docs/Decision tree/Real-Life Decision Cases/00-CANONICAL_SOURCE_OF_TRUTH.md`  
**Audit evidence:** `docs/Decision tree/Real-Life Decision Cases/SOURCE_OF_TRUTH_ALIGNMENT_AUDIT.md`  
**Status:** Plan only. No code is changed by this document.

## The target model

- **Goal Planner** decides goal feasibility and compares funding paths.
- **Strategy Builder** has four peer strategies: Progressive De-risking, Capital Preservation, Debt Reduction, Credit Utilisation.
- Decision order: feasibility/context → constraints → applicability → viability → strategy → variant → techniques → method/policy → solution → stress check → recommendation.
- Investor acceptance is required before a proposal changes the Accepted Plan or its active Action Plan.
- Whole-Plan Impact is needed only when shared resources or a material plan-level change requires it.
- No acceptable path is a valid result. Asset Mapping and Asset Earmarking are different.

## Fix list — do it in this order

| Priority | Where | What needs to change | Guardrail |
|---|---|---|---|
| **P0** | `backend/library/strategies/canonical.py`; `variants.py`; `backend/engines/strategy/scenario.py`, `decision.py`, `variant_selector.py`; `backend/library/strategies/solution_matrix.py` | Move Goal Funding out of the four-strategy Strategy Builder role and define its Goal Planner/feasibility contract. | **Do not just delete `strat-goal-funding`.** First trace API use, saved runs/versions, stored data and callers; write and test a migration. |
| **P0** | `backend/rules/strategy_decision.py` | Replace stale strategy-ID rules with approved canonical IDs and correct meanings. | Map each rule by meaning; do not do blind text replacements. Test every active strategy. |
| **P0** | `backend/engines/strategy/engine.py`; `backend/engines/strategy/recommendation.py` | Make the decision stages happen in the intended order. Keep candidate evaluation separate from running the chosen path; select the variant as an explicit decision stage. | A candidate technique run must not quietly become the selected implementation. Preserve hard-failure/decision-authority checks. |
| **P0** | Goal Planner ↔ Strategy Builder boundary and their tests | Define one feasibility-result format; Strategy Builder must consume it rather than calculate goal feasibility again. | Same inputs must not produce two conflicting feasibility answers. |
| **P1** | `backend/library/strategies/solution_matrix.py` and technique policy/mapping code | Enforce the same relationship everywhere: Strategy → Variant → Technique → Method/Policy → Solution → Action. | Keep entity types separate. Distinguish Required, Conditional, Optional, Not Applicable and Insufficient Inputs. |
| **P1** | `backend/engines/orchestration/engine.py`; `backend/rules/action_plan.py`; ActionPlanService | Finish the flow from combined-goal impact to investor-approved plan to concrete Action Plan. | A preview, rejected proposal or what-if must not create or overwrite active actions. |
| **P1** | Strategy/plan change and what-if lifecycle; related services/tests | Complete the loop: change → materiality/impact → targeted revalidation → investor Accept/Reject/Modify → update accepted plan only if accepted. | Recheck only affected goals/dependencies when possible. Preserve the old accepted plan on rejection. |
| **P1** | Strategy decision output and custom-strategy handling | Make “No Acceptable Path” a normal typed outcome; support investor-designed alternatives with explicit validation and origin. | Never force a recommendation just to fill an output. |
| **P1** | Asset Mapping / Asset Earmarking ownership and persistence | Keep mapping in Goal Planner; make earmarking a deliberate downstream reservation with conflict/release handling. | Cancelling a goal must not delete its underlying asset. Prevent the same money being reserved for competing goals. |
| **P1** | Hard constraints, advisory priorities and Money Wheel/ratio rules | Separate true blocking rules from signals that only influence ranking or explanation. | A ratio or score must not silently become a hard constraint. |
| **P2** | Other Decision Tree and architecture docs, including `docs/Decision tree/04-STRATEGY_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md`, `docs/architecture/strategy-matrix.md`, `docs/architecture/strategy-architecture-composition.md` | Mark outdated descriptions as historical/current-state or update them after code changes are verified. | Do not document target behaviour as already implemented. |
| **P2** | Tests, especially `backend/tests/test_strategy_decision_authority.py`, `test_canonical_strategies.py`, `test_goal_funding_strategy_builder.py`, `test_strategy_solution_matrix.py` | Update old five-strategy expectations and add coverage for the target boundaries and state transitions. | Tests must verify behaviour, not merely the presence of IDs or functions. |

## Decisions still needed — do not guess

1. Exact feasibility/optimization maths and financial assumptions.
2. Numerical materiality thresholds and when to revalidate.
3. Final hard-constraint catalogue and thresholds.
4. Stress/resilience scenarios and pass/fail policy.
5. Multi-goal priority weights and conflict-resolution rules.
6. Migration treatment for historical Goal Funding runs, versions and persisted data.

Until those are decided, keep the relevant policy configurable or explicitly marked open; do not invent values.

## Completion checks

- Only the four approved strategies appear as Strategy Builder peers; Goal Funding is handled by Goal Planner.
- No active decision rule depends on stale strategy IDs.
- The chosen strategy and variant are explicit before selected-path implementation is produced.
- Strategy/variant/technique/solution relationships are consistent and test-covered.
- Rejected proposals and what-ifs leave the Accepted Plan and active Action Plan unchanged.
- Material changes trigger targeted revalidation; unrelated goals are not needlessly rebuilt.
- Tests pass, and docs describe verified behaviour rather than intended behaviour.

**Working rule:** Fix one priority group at a time, add/update tests with each code change, and do not delete legacy paths until their callers and stored-data impact are accounted for.
