# Strategy Builder — Final Implementation Specification

**Document type:** Authoritative implementation specification  
**Scope:** Canonical Strategy Decision, Strategy/Variant/Technique selection, implementation architecture, stress/resilience, final recommendation and investor adoption boundaries  
**Status:** Consolidated from the Strategy Builder feature definition, existing-feature audit documents, and documented Real-Life Decision Cases. The target business model is separated from code-verified evidence; this document does not claim every target rule is implemented or that the business rules are frozen.  
**Existing-code evidence:** See `docs/existing features/Strategy-Builder/` and the code references in Section 12.

## 1. Purpose and ownership

Strategy Builder determines which canonical strategy is applicable and viable for a defined goal and financial context, selects a fitting variant and techniques, composes an implementation proposal, evaluates relevant trade-offs and resilience, and presents an explainable decision for the investor.

It consumes Goal Planner's goal-feasibility and funding context. It must not silently recalculate or redefine Goal Planner's funding feasibility as if that were Strategy Builder's own decision.

The four canonical Strategy Builder strategies are:
- **Progressive De-risking**
- **Capital Preservation**
- **Debt Reduction**
- **Credit Utilisation**

**Goal Funding is owned by Goal Planner / Goal Feasibility, not a fifth Strategy Builder strategy.** References in historical cases or audit material that label Goal Funding as a strategy are recorded source inconsistencies, not a reason to expand the canonical four-strategy set.

Strategy Builder must not force a recommendation when no candidate is acceptable. **No Acceptable Strategy / No Acceptable Path** is a valid decision outcome.

## 2. Inputs and outputs

### Inputs
- Defined goal or explicitly selected planning basket, including its requirements, target timing and relevant preferences.
- Current financial state and relevant assets, liabilities, cash flow, liquidity and debt information.
- Goal Planner's feasibility, funding-gap and funding-path evidence, including assumptions and limitations where available.
- Canonical constraint evaluation and the evidence needed for strategy applicability and eligibility.
- Selected scenario / changed assumptions for a What-If or stress evaluation.
- Existing Accepted Plan context when the decision is a plan-level change or may affect shared resources.
- Historical runs and versions for comparison and traceability; history alone is not current adoption state.

Missing or unavailable evidence must remain distinguishable from a failed check. Do not silently replace missing values with assumed financial facts.

### Outputs
- Canonical decision result and its status.
- Applicable strategy candidates, selected strategy or explicit no-acceptable-path result.
- Selected variant and technique-policy outcomes, including the reasons and evidence for required, conditional, optional, not-applicable or insufficient-input statuses.
- Architecture and investor-specific Solution proposal, with relevant assumptions, outcomes, trade-offs and constraints.
- Relevant stress/resilience and conditional whole-plan impact findings.
- Explainable recommendation, alternatives where justified, and persisted decision/run evidence.
- A proposed change remains a proposal until the investor explicitly adopts it through the accepted-plan lifecycle.

## 3. Canonical decision domains and separation of responsibilities

The documented target decision subsystem is:

1. Goal context and Goal Planner feasibility/funding evidence.
2. Hard-constraint and safety evaluation.
3. Strategy applicability.
4. Eight strategy eligibility fits.
5. Strategy selection.
6. Variant selection.
7. Technique selection and policy.
8. Architecture composition and Solution proposal.
9. Stress/resilience evaluation, with re-evaluation when required.
10. Final decision and recommendation.

These domains answer different questions and must not be collapsed into a single opaque score:

- **Hard constraints:** Is the situation permitted to proceed under the applicable validity/safety policy?
- **Applicability:** Should this strategy enter the candidate pool for this situation?
- **Eligibility / viability:** Can the candidate work under the actual financial conditions and available evidence?
- **Selection:** Which acceptable candidate is the appropriate choice under the defined decision policy?
- **Variant:** Which structural form of the selected strategy fits?
- **Technique:** Which reusable mechanisms does the Strategy + Variant require or permit?
- **Method/Policy:** How is a technique applied in this context?
- **Architecture:** How are the selected elements and dependencies composed?
- **Solution:** What concrete investor-specific implementation outcome is proposed?
- **Stress/resilience:** Does the proposed path remain acceptable under defined adverse or changed assumptions?
- **Recommendation:** How is the authoritative decision explained to the investor? Recommendation explains the decision; it must not silently create a second decision.

Applicability, viability, financial-health diagnostics, preferences, warnings and hard constraints are not interchangeable concepts. A financial-health signal is not automatically a universal blocker. Missing evidence must not silently become a hard failure.

## 4. Hard constraints and eight eligibility fits

### Hard constraints

The audit records existing constraint behavior around goal-positive horizon/target, critical emergency reserve, critical debt burden/DTI, discretionary-versus-essential priority and constraint-conflict governance. These are current audit findings, not permission to treat every signal as a universal blocker.

The canonical constraint result must preserve at least the distinction between:
- **PASS**
- **FAIL**
- **UNAVAILABLE / insufficient evidence**

Where the product distinguishes blockers, warnings and diagnostics, retain those meanings. Exact rule identities, scope, thresholds and missing-data behavior must be taken from the approved canonical policy; do not invent new thresholds in implementation.

### Eight eligibility fits

The canonical fit vocabulary is:
1. Cash-flow Fit
2. Liquidity Fit
3. Debt Fit
4. Asset Resource Fit
5. Risk Capacity Fit
6. Goal Constraint Fit
7. Multi-goal Conflict Fit
8. Implementation Fit

The existing audit records aggregate precedence as **FAIL > CONDITIONAL > PASS**. The business conditions behind every fit, symmetry of statuses, overlap with applicability/constraints and the complete treatment of unavailable inputs remain items to reconcile against the detailed audits and approved real-life cases. Do not treat the existence of a fit name or engine as proof that its policy is complete.

Multi-goal conflict/whole-plan impact is conditional on a plan-level decision, shared-resource conflict, new goal against an existing plan, or a material cross-goal effect. It is not an automatic mandatory gate for every isolated single-goal decision.

## 5. Strategy applicability and selection

### Canonical candidate set

Only the four canonical strategies in Section 1 belong to the Strategy Builder strategy set. Goal Funding mechanisms, including contribution planning/escalation, remain within Goal Planner / Goal Feasibility.

Applicability must determine whether a strategy belongs in the candidate pool. Viability then evaluates whether that candidate can work under the actual conditions. Do not use strategy selection to hide a failed hard constraint or to turn missing data into a favorable result.

### Strategy-specific boundaries

- **Progressive De-risking** is not selected merely because a goal has a future date. The documented rationale is a meaningful future requirement for which gradual changes in risk/capital positioning improve the chance of meeting it.
- **Capital Preservation** is not selected merely because a goal exists. It applies when some or all required capital has become protection-sensitive.
- **Debt Reduction** is not selected merely because the investor has debt. The decision must be tied to material effects on cash-flow capacity, goal funding, affordability or resilience.
- **Credit Utilisation** must be supported by borrowing capacity, sustainable EMI/repayment, justified financing cost and a credible repayment path. It must not simply transfer an existing debt problem into another form.

If every candidate fails applicability/viability or violates a genuine hard constraint, return a clear no-acceptable-path outcome rather than force a winner.

### Selection policy

The audit identifies a current PASS > CONDITIONAL > FAIL principle and composite scoring in the existing decision engine, but exact score weights, precedence, alternative-candidate policy and final selection conditions are not established here as frozen business rules. The implementation must use one authoritative selection policy, preserve reasons/evidence, and avoid duplicate selection logic in the recommendation layer. Do not invent weights or thresholds.

## 6. Canonical Strategy → Variant registry

These are the documented target variants and their situation mapping. The mapping is not proof that each variant is reachable or implemented in the current runtime.

### Progressive De-risking
| Situation | Variant |
|---|---|
| Single future goal date | Goal-Date Glide Path |
| Multiple defined future payments | Payment-Tranche Glide Path |
| Recurring future requirement | Recurring-Cashflow Glide Path |
| Accumulation transitioning into recurring income | Income-Transition Glide Path |

### Capital Preservation
| Situation | Variant |
|---|---|
| Entire required capital needs protection | Full-Goal Preservation |
| Immediate/next payment needs protection | First-Payment Preservation |
| Repeating reserve requirement | Rolling Reserve Preservation |
| Only core/required capital needs protection | Protected-Core Preservation |

### Debt Reduction
| Situation | Variant |
|---|---|
| Debt creates a goal funding gap | Goal-Gap Debt Reduction |
| EMI burden suppresses cash-flow capacity | EMI-Relief Debt Reduction |
| Remaining debt/capital gap needs optimisation | Residual-Gap Debt Reduction |
| Debt and another goal must be coordinated | Goal-Linked Debt Reduction |

### Credit Utilisation
| Situation | Variant |
|---|---|
| Small residual funding gap | Residual-Gap Bridge |
| Defined portion intentionally financed | Partial-Goal Financing |
| Borrowing constrained by sustainable EMI | EMI-Cap Financing |
| Temporary timing mismatch | Timing-Bridge Financing |

Variant selection must be an identifiable decision domain with explicit candidate applicability, conditions and precedence. The audits identify selection logic outside the centralized definitions, implicit precedence, missing-input effects and reachability gaps. Those current-state findings require verification; do not silently assume all 16 target variants are active in runtime.

## 7. Canonical techniques and variant-to-technique policy

A Technique is a reusable mechanism selected because the Strategy + Variant requires or permits it. Technique selection must be variant-aware and must preserve the policy status for each technique:
- **Required**
- **Conditional**
- **Optional**
- **Not Applicable**
- **Insufficient Inputs**

Not Applicable and Insufficient Inputs are not equivalent. Conditional does not mean always apply. Do not infer a technique's status solely from a strategy-level mapping when the canonical mapping is variant-specific.

### Technique registry

| Technique | Primary purpose |
|---|---|
| Glide Path | Gradually change risk/capital positioning as a requirement approaches |
| Bucketing | Organize capital/resources by time or liability needs |
| Cash-flow Matching | Match future cash requirements with appropriate resources/cash flows |
| Laddering | Stagger maturities/resources against multiple predictable requirements |
| Asset Earmarking | Designate resources for a specific goal/protected capital pool |
| Goal Segmentation | Separate competing goal/debt/resource requirements |
| Debt Repayment Prioritisation | Determine which debt receives repayment priority |
| Debt Cost Optimisation | Reduce or optimise effective debt cost |
| Debt Prepayment Optimisation | Determine whether available capital should be used for prepayment |
| EMI Capacity Analysis | Determine sustainable repayment capacity |
| Borrowing Capacity Analysis | Determine how much borrowing can responsibly be supported |
| Financing Cost Comparison | Determine whether borrowing is economically justified |

### Variant-to-technique policy matrix

| Strategy / Variant | Required techniques | Conditional techniques |
|---|---|---|
| Progressive De-risking — Goal-Date Glide Path | Glide Path | Bucketing, Cash-flow Matching |
| Progressive De-risking — Payment-Tranche Glide Path | Glide Path, Cash-flow Matching | Bucketing |
| Progressive De-risking — Recurring-Cashflow Glide Path | Bucketing, Cash-flow Matching | Glide Path |
| Progressive De-risking — Income-Transition Glide Path | Glide Path, Bucketing | Cash-flow Matching |
| Capital Preservation — Full-Goal Preservation | Bucketing, Asset Earmarking | Cash-flow Matching, Laddering |
| Capital Preservation — First-Payment Preservation | Cash-flow Matching, Bucketing | Asset Earmarking |
| Capital Preservation — Rolling Reserve Preservation | Bucketing, Cash-flow Matching | Laddering |
| Capital Preservation — Protected-Core Preservation | Asset Earmarking, Bucketing | Cash-flow Matching, Laddering |
| Debt Reduction — Goal-Gap Debt Reduction | Goal Segmentation, Debt Repayment Prioritisation | Debt Cost Optimisation, Cash-flow Matching, Debt Prepayment Optimisation |
| Debt Reduction — EMI-Relief Debt Reduction | EMI Capacity Analysis, Debt Cost Optimisation | Debt Repayment Prioritisation, Debt Prepayment Optimisation |
| Debt Reduction — Residual-Gap Debt Reduction | Goal Segmentation, Cash-flow Matching | Debt Repayment Prioritisation, Debt Cost Optimisation, Debt Prepayment Optimisation |
| Debt Reduction — Goal-Linked Debt Reduction | Goal Segmentation, Cash-flow Matching | Debt Cost Optimisation, Debt Prepayment Optimisation |
| Credit Utilisation — Residual-Gap Bridge | Borrowing Capacity Analysis, Financing Cost Comparison | Cash-flow Matching, EMI Capacity Analysis |
| Credit Utilisation — Partial-Goal Financing | Financing Cost Comparison, Goal Segmentation | Borrowing Capacity Analysis, EMI Capacity Analysis |
| Credit Utilisation — EMI-Cap Financing | EMI Capacity Analysis, Borrowing Capacity Analysis | Financing Cost Comparison |
| Credit Utilisation — Timing-Bridge Financing | Cash-flow Matching, Financing Cost Comparison | Borrowing Capacity Analysis, EMI Capacity Analysis |

Laddering is conditional, not a default Capital Preservation technique; use it where multiple predictable maturity/payment dates justify staggered maturities.

### Taxonomy exclusions and boundaries
- Contribution Escalation belongs to Goal Planner / Goal Funding, not the core Strategy Decision Tree.
- Duration / Horizon Matching is a method/analysis, not a separate core technique.
- Tax-specific techniques such as Tax-Efficient Sequencing and Tax-Loss Harvesting are not forced into this four-strategy decision tree; they remain in the appropriate downstream investment/tax implementation layer unless a later explicit business decision changes that ownership.
- Asset Mapping records an asset-goal relationship. Asset Earmarking is a strategic designation/protection technique and is not equivalent to mapping.
- A Technique is not a Solution. A Solution must not merely duplicate a Variant or Technique under another label.

## 8. Architecture, Solution and opportunity-cost comparison

Architecture composes the selected Strategy, Variant, technique choices, methods/policies and their dependencies into a coherent implementation proposal. Architecture and Solution are separate concepts:
- **Architecture:** the composed structure of selected elements and dependencies.
- **Solution:** the concrete investor-specific implementation outcome proposed within that structure.
- **Action:** a concrete step derived from an accepted implementation.

The Solution proposal may compare resource use, contributions, timing, liquidity, debt effects, risk assumptions and competing-goal consequences where relevant evidence exists. Do not declare an alternative better without comparable evidence and explicit assumptions.

Goal Planner owns goal funding feasibility and funding-path context. Strategy Builder consumes that context and evaluates execution strategies and meaningful implementation alternatives; it must not silently redefine the upstream feasibility result. Opportunity-cost concepts can inform comparisons, but current runtime pass-through, calculation ownership and decision impact must be verified rather than assumed.

The existing audit reports that architecture is currently composed before final strategy selection in at least one runtime path, creating possible circular influence (Strategy → Architecture → Technique/score → Strategy). The target policy must have one clear selection authority and a coherent downstream architecture composition. Preserve existing architecture identity requirements documented by the audit unless an explicit approved change says otherwise.

### Asset earmarking
Earmarking requires an explicit strategic reason. The same asset must not be silently treated as fully earmarked for competing goals. A mapped asset may later be earmarked, partially earmarked, released or reassigned. Cancelling a goal must not delete the underlying asset. Earmarking capital does not itself select an investment product; product selection remains a separate downstream decision.

## 9. Stress / resilience and conditional revalidation

Stress/resilience evaluates whether the proposed path remains acceptable under defined adverse or changed assumptions, including relevant funding, liquidity, debt/EMI and goal-timing effects. It is distinct from:
- base-case applicability;
- base-case viability;
- whole-plan impact analysis;
- What-If scenario exploration.

The target decision model reuses the same canonical constraint, eligibility, strategy, variant and architecture rules under stressed inputs rather than creating a separate recommendation system. If stress findings invalidate the current candidate, the decision must be reconsidered through the canonical decision authority.

The audit records baseline and sensitivity-scenario capability but identifies gaps in canonical stress taxonomy, correlated stress cases, formal resilience classification, stability testing and stress-triggered re-selection. Categories such as Robust / Conditional / Fragile were proposed in audit material but are not treated here as frozen labels. Exact scenarios, thresholds, classification and warning/blocking behavior remain to be confirmed against approved business rules.

Material execution or financial-state changes require impact analysis and targeted revalidation of affected decisions. Do not re-evaluate or replace the entire plan automatically when only a local change is material. Whole-Plan / Multi-Goal Impact is invoked when the decision affects competing goals/shared resources or otherwise has a material cross-goal effect.

## 10. What-If, investor decision and plan lifecycle

A What-If scenario is an alternative evaluated against a known baseline. Where supported, retain the baseline, changed inputs/assumptions, projected outcomes and validation status. Exploring or saving a scenario must not mutate the active Accepted Plan.

Keep these states distinct:
1. Decision/run generated.
2. Scenario saved or edited.
3. Recommendation presented.
4. Investor accepts, rejects or modifies the proposal.
5. Accepted Plan updated only after explicit adoption.
6. Action Plan created/updated from the accepted implementation.
7. Actions executed and execution status recorded.

A historical run, version, recommendation or saved scenario does not prove current adoption. If the investor rejects every proposal, the existing Accepted Plan and Action Plan remain unchanged. If the investor adopts a revised path, update only the affected accepted implementation and relevant actions; completed actions remain history while active/future actions may be revised.

An investor-designed path may be captured as a separate proposal when the product policy permits it. Evaluate it against constraints, feasibility/funding context, relevant whole-plan impact and resilience; explain its numerical consequences and distinguish assumptions from guarantees. It is not automatically safe, viable or accepted and must not be relabelled as one of the four canonical strategies. It becomes active only through explicit investor adoption.

A complete financial plan can contain multiple coordinated strategies across different goals/financial requirements. Two alternatives shown for one decision do not limit the entire plan to two strategies.

## 11. Real-life case coverage and decision boundaries

The documented cases establish these requirements:
- **Cases 1–2:** Goal Funding ownership; Strategy Builder consumes Goal Planner feasibility and evaluates execution choice, including debt/EMI, financing cost, preservation of productive assets and long-term effects where relevant.
- **Cases 3–4:** separate strategy/implementation proposal from investor acceptance and Action Plan; compare current and alternative paths using explicit assumptions, contributions, timing, liquidity, risk and other-goal effects.
- **Cases 5–8:** respond to changed financial state, changed goal intent and new/competing goals; distinguish advisory priorities from genuine hard constraints; investor choice must not silently replace the active plan before adoption.
- **Cases 9–11:** What-If isolation, impact analysis, targeted revalidation and iterative updates; a changed execution/funding input does not automatically mean the canonical strategy changed.
- **Case 12:** no acceptable standard path and investor-designed proposal handling; no forced recommendation.
- **Case 15:** Asset Mapping versus Asset Earmarking, protection rationale, shared-resource conflicts and downstream product-selection boundary.

The source material contains explicit terminology conflicts, including some case bodies calling Goal Funding a strategy while the canonical decision-tree definition excludes it. The canonical four-strategy model in this specification preserves Goal Funding as a Goal Planner / Goal Feasibility responsibility; the historical conflict is not silently rewritten as runtime evidence.

Illustrative numbers in real-life cases (including the example 18% debt cost, goal amounts, contributions or return assumptions) are case inputs only. They are not default thresholds, promised returns or general rules.

## 12. Existing code evidence and routes

### Code references identified by the feature/audit documents
- Frontend: `frontend/app/investor/strategy-builder/page.tsx`
- Strategy API: `backend/api/strategy.py`
- Strategy edit API: `backend/api/strategy_edit.py`
- Strategy version API: `backend/api/strategy_version.py`
- Strategy engine: `backend/engines/strategies` and related strategy engine modules.
- Detailed current-state audit: `docs/existing features/Strategy-Builder/`

### Supporting routes
- Strategy comparison: `/investor/strategy-comparison`
- Strategy edit: `/investor/strategy-edit`
- Strategy history: `/investor/strategy-history`
- Strategy scenarios: `/investor/strategy-scenarios`

These references identify areas to inspect; they do not by themselves prove exact runtime order, complete persistence, scenario isolation, investor acceptance behavior or deployment status.

## 13. Unverified implementation facts

The source audits and feature definition leave the following points unverified or not frozen:
- Exact applicability conditions and AND/OR semantics, horizon boundaries and missing-data behavior.
- Canonical hard-constraint identities, thresholds, scope and the distinction between blockers, warnings and diagnostics.
- Full business conditions and status behavior for all eight eligibility fits.
- Strategy-selection precedence, score weights and alternative-candidate policy.
- Reachability and exact runtime selection conditions for every target variant.
- Variant-specific technique selection, combination/exclusion rules and missing-input behavior.
- Exact architecture composition order and how circular selection influence is prevented.
- Complete and consistent Solution meaning in registry/runtime.
- Opportunity-cost calculation ownership, evidence pass-through and effect on decisions.
- Stress taxonomy, resilience labels, thresholds and re-selection behavior.
- Materiality and targeted-invalidation rules for cross-goal/plan-level changes.
- Scenario persistence/isolation and explicit acceptance-to-Accepted-Plan/Action-Plan update behavior.
- Which target business rules are active in runtime versus documented only.

Keep code-verified current behavior, target business requirements and unresolved decisions explicitly separate. Do not infer implementation from a registry entry, UI route, historical snapshot or design document.
