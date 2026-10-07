# 04 — Strategy Selection: Current State & Recommendation

## 1. Purpose

This document records the current code-verified Strategy Selection decision flow and the recommended target contract for the PlanVesto Canonical Decision Engine.

This is a design/audit document only. Strategy-selection rules are not frozen and no refactor is authorized by this document.

Final business behavior will be frozen later through real-life cases.

## 2. Scope

This step answers one question:

> After applicability, hard constraints, and the eight eligibility fits have been evaluated, how does PlanVesto choose one strategy from the remaining candidates?

This document covers candidate strategy pool, eligibility precedence, decision scoring, ranking authority, recommendation authority, alternatives, current inconsistencies, and the target decision contract.

## 3. Current Five Canonical Strategies

1. Goal Funding — strat-goal-funding
2. Progressive De-risking — strat-progressive-de-risking
3. Capital Preservation — strat-capital-preservation
4. Debt Reduction — strat-debt-reduction
5. Credit Utilisation — strat-credit-utilisation

## 4. Current Selection Pipeline

Goal → Strategy Applicability → Candidate Strategies → Scenario Generation → Architecture Composition → Technique Execution → 8-Fit Eligibility Evaluation → Eligibility Gate → Decision Score → Best Strategy + Alternative → Ranking → Recommendation

Orchestration is in backend/engines/strategy/engine.py. The actual selection decision is performed by backend/engines/strategy/decision.py::evaluate_decision().

## 5. Current Selection Authority

Primary authority: backend/engines/strategy/decision.py. It evaluates architectures, evaluates the eight eligibility fits, determines PASS / CONDITIONAL / FAIL, prefers PASS candidates, uses CONDITIONAL candidates only when no PASS exists, calculates decision scores, selects the highest-scoring candidate, and returns alternatives.

Ranking is in backend/engines/strategy/ranking.py. It consumes DecisionResult; its composite scores are descriptive evidence rather than the authoritative decision.

Recommendation is in backend/engines/strategy/recommendation.py. It consumes DecisionResult and adds funding explanation, financial diagnostics as explanatory evidence, supporting-strategy explanation, and the selected variant.

## 6. Current Eligibility Precedence

PASS candidates form the first pool. CONDITIONAL candidates are used only if there are no PASS candidates. FAIL candidates are never recommended.

Therefore the current precedence is: PASS > CONDITIONAL > FAIL.

## 7. Current Decision Score

Current score components are Goal Fit Score, Horizon Fit Score, Funding Fit Score, Feasibility Score, Component Fit Score, and Technique Execution Score.

The score function lives in backend/rules/strategy_decision.py and is invoked by backend/engines/strategy/decision.py.

Current feasibility points are PASS = 15, CONDITIONAL = 8, FAIL = 0 / infeasible.

Goal-fit scoring currently gives points for canonical goal-type match, funding-characteristic match, long/near-term match, fixed-timeline match, and high-priority match.

### Critical canonicalization issue

backend/rules/strategy_decision.py still references stale strategy IDs such as strat-dynamic-accumulation, strat-calibrated-growth, strat-high-liquidity-flex, and strat-cap-preservation. These do not match the current five canonical strategy IDs.

Therefore this scoring module is not fully synchronized with the current strategy library and must be resolved before the scoring policy is frozen.

## 8. Current Strategy Selection Algorithm

For each candidate architecture the system:
1. Finds its primary canonical strategy.
2. Finds candidate scenarios.
3. Selects a baseline scenario.
4. Evaluates all eight eligibility fits.
5. Applies the hard-constraint/goal eligibility gate.
6. Determines overall eligibility status.
7. Calculates decision dimensions.
8. Calculates total decision score.
9. Stores evidence and rationale.

Then it collects PASS candidates, collects CONDITIONAL candidates, uses the PASS pool if any exist, otherwise uses the CONDITIONAL pool, sorts that pool by total decision score, chooses the first candidate, and chooses the next best candidate as an alternative.

For Goal Funding specifically, the current code evaluates every funding scenario and uses funding feasibility status before score/tie ordering.

## 9. Decision Score vs Ranking Score

There are two scoring concepts.

Decision score is used by evaluate_decision() to select the strategy. Ranking composite score is used by ranking.py as descriptive evidence and is ordered primarily by the authoritative DecisionResult order.

Recommendation: keep this separation only if intentional. The future canonical contract should clearly state: Decision score chooses the strategy; ranking scores explain/compare the decision.

## 10. Current Problems / Gaps

### Gap 1 — Scoring policy is stale
The scoring policy references strategy IDs from an older strategy model. Some branches therefore cannot apply to the current five canonical strategies.

### Gap 2 — Business scoring is not fully canonicalized
The decision engine executes scoring behavior while rules/strategy_decision.py contains score policy slots/constants. The policy and current strategy library are not fully aligned.

### Gap 3 — Architecture is composed before final strategy selection
The current flow composes architectures before evaluate_decision(). Technically, selection chooses the best architecture candidate whose primary strategy is attached to it, rather than selecting a strategy first and composing architecture afterward. This may be correct, but must be explicitly decided.

### Gap 4 — Technique execution participates in strategy score
Technique execution score can affect strategy selection, creating a potential Strategy → Architecture → Techniques → Technique Score → Strategy Selection dependency. The target architecture should decide whether technique readiness is a selection input, implementation-feasibility input, or post-selection evidence.

### Gap 5 — Variant selection is downstream
The strategy is selected first and VariantSelector selects the variant later during recommendation. This is conceptually clean and should be explicitly preserved in the future contract.

### Gap 6 — Alternative strategy output is narrow
Current decision logic returns one alternative architecture. The future product contract may need primary strategy, ordered alternatives, and reasons each alternative was not selected.

## 11. Recommended Target Strategy Selection Contract

After applicability, hard constraints, and the eight fits:

1. Build the eligible strategy pool: remove applicability FAIL, hard-constraint FAIL, and eligibility FAIL; retain PASS and CONDITIONAL.
2. Apply precedence: PASS pool first. If at least one PASS exists, do not use CONDITIONAL strategies for the primary recommendation. If no PASS exists, use CONDITIONAL candidates. If none remain, return No Viable Strategy.
3. Score only within the selected pool using a canonical, strategy-ID-aligned policy.
4. Select the primary strategy as the highest canonical decision score.
5. Return ordered alternatives with strategy ID, score, eligibility status, and reason not selected.
6. Continue downstream: Variant → Technique → Architecture → Stress/Resilience → Final Recommendation.

## 12. Recommended Decision Formula

Strategy Selection = Eligibility Pool → Precedence → Decision Score → Primary + Alternatives

Not simply Raw Composite Score.

This protects the system from recommending a numerically attractive but conditionally/unsafely eligible strategy over a fully viable strategy.

## 13. Recommended Rule Ownership

| Responsibility | Recommended authority |
|---|---|
| Strategy identity | backend/library/strategies/canonical.py |
| Applicability | Canonical Strategy Applicability rules |
| Hard constraints | Canonical Constraint rules |
| Eight eligibility fits | Canonical Strategy Eligibility rules |
| Selection precedence | Canonical Strategy Selection rules |
| Decision score dimensions | Canonical Strategy Selection policy |
| Decision execution | Decision Engine |
| Ranking/evidence | Ranking layer |
| Recommendation wording | Recommendation layer |
| Variant selection | Variant Selection rules |

Core principle: The Decision Engine executes the selection policy; it should not invent selection rules.

## 14. Recommended Future Decision Object

The future canonical result should conceptually contain: candidate_strategies, eligibility_status, eligibility_fit_results, selection_pool, decision_scores, primary_strategy, alternative_strategies, selection_rationale, constraints, and decision_version.

This makes the decision auditable. An investor should be able to answer: Why was this strategy selected instead of the other four?

## 15. Real-Life Validation Cases Before Freezing

Validate at least:
1. Only one PASS strategy.
2. Multiple PASS strategies.
3. One PASS with several CONDITIONAL strategies.
4. No PASS but multiple CONDITIONAL strategies.
5. All strategies FAIL.
6. Higher score but CONDITIONAL vs lower score but PASS.
7. Same score between two PASS strategies.
8. Different goal types with same financial state.
9. Different horizons for the same goal.
10. Shortfall vs On Track vs Overfunded.
11. High-priority vs normal-priority goal.
12. Debt pressure changing the candidate pool.
13. Liquidity shortage changing eligibility.
14. Risk-capacity mismatch changing eligibility.
15. Technique unavailable for one candidate.
16. Architecture composition changing candidate evidence.
17. Multiple supporting strategies.
18. Goal Funding with multiple funding variants.

For every case record: Inputs → Applicable strategies → Hard constraints → 8-fit results → Selection pool → Scores → Primary → Alternatives → Reason.

## 16. What Should NOT Be Frozen Yet

Do not freeze solely from current code: exact score weights, exact score ranges, whether technique execution should influence strategy selection, whether architecture should be composed before or after strategy selection, exact tie-breaking beyond deterministic behavior, number of alternatives shown to the investor, whether CONDITIONAL strategies should ever compete directly with PASS strategies, whether investor priorities should influence selection score, and final strategy-selection thresholds.

## 17. Current vs Recommended Summary

| Area | Current state | Recommendation |
|---|---|---|
| Strategy IDs | Five canonical IDs | Preserve |
| Selection authority | decision.py | Make Canonical Decision Engine authority |
| Eligibility precedence | PASS > CONDITIONAL > FAIL | Validate then freeze |
| Decision score | Exists | Re-align completely with five canonical strategies |
| Ranking | Uses DecisionResult authority | Preserve as evidence/comparison |
| Recommendation | Consumes DecisionResult | Preserve downstream role |
| Score policy | Partly stale | Replace/align before implementation |
| Architecture dependency | Composed before final selection | Decide explicitly |
| Technique score | Can influence selection | Validate whether this belongs here |
| Alternatives | One primary + limited alternative | Expand only if product requires |
| Auditability | Evidence exists | Formalize canonical decision record |

## 18. Decision Status

CURRENT STATUS: DOCUMENTED — NOT FROZEN

The repository already has a real strategy-selection authority in evaluate_decision(). The major issue is not that selection is missing; it is that the selection policy is partly split and the scoring rules are not fully synchronized with the current five canonical strategies.

The next step is to validate this selection behavior with real-life cases before freezing it.

Next step: Step 5 — 22 Variant Selection: Current State & Recommendation.