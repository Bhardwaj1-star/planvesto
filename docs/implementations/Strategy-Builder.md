# Strategy Builder — Implementation Contract

**Document type:** Implementation contract / coding-agent handoff  
**Scope:** Strategy Builder's target decision flow, canonical strategy and variant registry, technique policy, implementation proposal, stress/resilience, recommendation, and investor-adoption boundary.  
**Status:** Consolidated from the two designated references. This document describes the target contract; it does not claim the target is already implemented in code.

## 1. Design references

This contract is based on these two references:

1. Feature definition: [docs/feature/Strategy-Builder.md](../feature/Strategy-Builder.md)
2. Existing-feature code audit: [docs/existing features/Strategy-Builder/](../existing%20features/Strategy-Builder/)

The feature definition records the business model and its Real-Life Decision Case basis. The existing-feature folder records the inspected code, current runtime behavior, and documented gaps. The audit is not repeated here.

Where the audit describes existing runtime behavior that differs from the target contract, preserve the distinction between **current state** and **target behavior**. A code-audit finding does not, by itself, define target business behavior.

## Authority for coding agents — mandatory

When documents or legacy records disagree, implement this contract's target rules and use `docs/Real-Life Decision Cases/strategy-decision-tree.md` as the canonical Strategy taxonomy. Feature and case documents explain the business context; `docs/existing features/Strategy-Builder/` records observed current/legacy behavior and must not override the target contract.

The canonical Strategy Builder allowlist is exactly: **Progressive De-risking, Capital Preservation, Debt Reduction, and Credit Utilisation**. **Goal Funding is not a Strategy, candidate, Strategy variant, or fifth option.** It is Goal Planner / Goal Feasibility's funding-path domain.

Treat `strat-goal-funding`, any Goal Funding Strategy row, and its six historical options as legacy/current-state identifiers only. Do not expose or select them as Strategy Builder strategies in the target system. Do not silently rename them to one of the four canonical strategies. Before any code/data migration, map the legacy records by their actual meaning to Goal Planner funding-path concepts; do not delete or migrate records solely because their names contain “Goal Funding.”

## 2. Purpose and ownership

Strategy Builder prepares strategy alternatives for the investor from the investor's financial situation and goal context. It presents **exactly two Strategy options for each decision**. It does not make the final strategy choice on the investor's behalf; the investor reviews the alternatives and decides.

Goal Planner does **not** send a Strategy to Strategy Builder. Goal Planner's responsibility is to establish the goal-feasibility approach/result and related funding context. The connection between Goal Planner's feasibility output and Strategy Builder's strategy generation will be defined when the two features are connected later. Do not assume or implement a strategy-selection dependency from Goal Planner. A change to a funding path must first be evaluated in Goal Planner; it is not automatically a Strategy change.

### Canonical Strategy Builder strategies

Exactly these four strategies belong to Strategy Builder:

1. Progressive De-risking
2. Capital Preservation
3. Debt Reduction
4. Credit Utilisation

**Goal Funding is owned by Goal Planner / Goal Feasibility. It is not a fifth Strategy Builder strategy.** SIP, lump sum, step-up contributions, contribution escalation, and combinations of funding mechanisms remain in the Goal Planner funding domain unless an explicit business decision changes their ownership.

If no acceptable path exists, the result must explicitly say **No Acceptable Strategy / No Acceptable Path**. The requirement to present two options does not permit the system to claim that an unviable option is suitable, hide a failed viability check, or force the investor to adopt either option. Each displayed option must show its actual status and supporting reasons.

## 3. Target decision flow

The target flow is:

~~~text
Goal Context + Financial State
          +
Applicable Constraints
          ↓
Constraint / Safety Evaluation
          ↓
Generate Exactly Two Strategy Options
          ↓
Applicability / Viability Evaluation of Each Option
          ↓
For Each Option:
Strategy → Variant → Technique → Method / Policy
          ↓
Solution Proposal
          ↓
Relevant Stress / Resilience and Comparison
          ↓
Present Both Options + Evidence / Trade-offs to Investor
          ↓
Explicit Investor Decision / Adoption
          ↓
Accepted Plan
          ↓
Action Plan
          ↓
Execution
~~~

The target flow does **not** contain Scoring or a separate eight-eligibility-fits stage. References to scoring and eight fits in the existing-feature audit describe the audited current system and must not be treated as required target stages for this contract.

Whole-Plan / Multi-Goal Impact is conditional. It applies when the decision affects an existing Accepted Plan, shared resources, competing goals, a newly added goal, or another material cross-goal outcome. It is not a mandatory gate for every isolated individual-goal decision.

Investor Decision, Accepted Plan, Action Plan, and Execution are downstream lifecycle stages; they are not interchangeable with the Strategy Decision or recommendation.

## 4. Inputs and outputs

### Inputs

- Defined goal and the actual requirement, target, timing, and payment structure.
- Current financial state and relevant income, expenses, assets, liabilities, liquidity, debt, and cash-flow evidence.
- Goal Planner feasibility result, funding gap, funding-path evidence, assumptions, and known limitations. This is feasibility/funding context, not a Strategy supplied or selected by Goal Planner.
- Applicable constraints and their evaluation evidence.
- Information needed to evaluate strategy applicability and viability.
- Existing Accepted Plan and shared-resource context when the decision is plan-level or can materially affect other goals.
- Changed assumptions or scenario inputs for What-If and stress evaluation.
- Historical runs/versions for traceability and comparison. History alone does not prove current adoption.

Unavailable evidence must remain distinguishable from a failed check. Missing information must not be silently replaced with invented financial facts.

### Outputs

- An authoritative decision result and its status.
- **Exactly two Strategy options** presented to the investor, each with its own applicability/viability status and evidence/reasons.
- The variant and implementation proposal for each option where the option is viable and the required evidence exists; otherwise, an explicit status and reason such as Not Applicable, Not Viable, Insufficient Inputs, or No Acceptable Path.
- Technique policy results, including reasons for Required, Conditional, Optional, Not Applicable, or Insufficient Inputs.
- A concrete investor-specific Solution proposal for each option that can validly be prepared.
- Relevant assumptions, evidence, constraints, trade-offs, and stress/resilience findings.
- Conditional whole-plan impact findings when applicable.
- An explainable comparison and recommendation that does not misrepresent an option's status.
- A proposal/adoption state that remains separate from the active Accepted Plan.

## 5. Decision domains and boundaries

Each domain has a separate responsibility.

| Domain | Question it answers | Required boundary |
|---|---|---|
| Goal Planner feasibility/funding | What is the goal's funding/feasibility position? | Upstream evidence consumed by Strategy Builder; do not recalculate it as a Strategy Builder strategy |
| Constraint / Safety Evaluation | Which applicable restrictions or non-negotiable conditions govern the decision? | A diagnostic or warning is not automatically a hard blocker |
| Strategy Applicability | Can this strategy legitimately apply to this situation? | Applicability is not viability |
| Strategy Viability | Can the applicable candidate work under the actual financial conditions and constraints? | Failed viability must not be overridden merely to produce an answer |
| Strategy Alternative Generation | Which two Strategy options should be presented for this decision? | Exactly two options must be presented; no fixed scoring rule or score-based ranking. Show evidence and status for each; do not choose on the investor's behalf |
| Variant Selection | Which structural form of the selected strategy fits the situation? | Variant is subordinate to one of the four strategies |
| Technique Selection | Which reusable mechanisms are required or permitted by the selected Strategy + Variant? | Mapping is variant-specific; technique status must preserve the policy vocabulary |
| Method / Policy | How is a selected technique applied in this context? | A method is not a separate strategy or technique merely because it describes an operation |
| Solution | What concrete implementation outcome is proposed for this investor? | Solution must not merely duplicate a Variant or Technique under another label |
| Stress / Resilience | Does the proposed path remain acceptable under defined adverse or changed assumptions? | Reuses the canonical decision domains; it is not a separate competing decision engine |
| Recommendation | How is the authoritative decision explained to the investor? | Explains both options and their trade-offs; does not silently replace the decision authority |
| Investor Decision / Accepted Plan | Has the investor adopted the proposal into the active plan? | A recommendation, saved scenario, or history record is not proof of adoption |

## 6. Constraints, applicability, viability, and selection

### Constraints and safety

Evaluate applicable constraints before selecting a strategy. Preserve the meaning established by the governing policy for blockers, warnings, preferences, diagnostics, conflicts, and unavailable evidence.

The existing audit identifies emergency-reserve, debt-burden/DTI, goal-validity, priority, and constraint-conflict behavior in current code. Those audit observations do not make every such signal a universal blocker. Do not invent new thresholds or change a diagnostic into a hard constraint without a source-defined rule.

### Applicability

Evaluate the canonical strategies against the actual situation. The system must still present exactly two Strategy options, but must not mislabel a strategy as applicable when its documented conditions do not fit. If an option is not applicable, display that status and the reason rather than concealing it or pretending it is viable.

### Viability

A candidate that is applicable must still be checked for whether it can work under actual conditions. Applicability does not prove viability.

For Credit Utilisation, the documented viability gates are:

- A genuine funding or timing gap exists.
- Reasonable own-resource funding has been considered.
- Borrowing capacity is sufficient.
- EMI/repayment is sustainable.
- Financing cost is economically justified.
- A credible repayment path exists.
- Applicable hard financial constraints are not violated.

Failure of a material Credit Utilisation viability gate means Credit Utilisation fails viability and must not be recommended.

### Strategy selection and two-option presentation

- Present **exactly two Strategy options for every decision**. This is a fixed presentation requirement, not a dynamic count.
- The options must come from the four canonical Strategy Builder strategies. Goal Funding is not a Strategy Builder option.
- Do not require the second option to prove that it is better than the first before displaying it. Show both options with comparable evidence, assumptions, benefits, limitations, risks, and trade-offs wherever that evidence is available.
- Do not automatically label one option “better” or declare a winner without comparable evidence and stated assumptions.
- Evaluate and display each option's applicability and viability honestly. An option that fails a check must be marked with the relevant status and reason; it must not be recommended as suitable.
- If fewer than two options are viable, still show exactly two Strategy options and clearly disclose the non-viable, non-applicable, or insufficient-input status. Do not invent a viable path or force acceptance. If no acceptable path exists, explicitly show **No Acceptable Strategy / No Acceptable Path**.
- The investor makes the final choice, subject to genuinely hard constraints. A recommendation is guidance, not automatic adoption.
- Do not invent score weights, numerical thresholds, score-based rankings, or fixed tie-breaking rules.
- The Goal Planner-to-Strategy Builder connection will be specified separately when those features are connected.

## 7. Strategy-specific applicability boundaries

### Progressive De-risking

**Purpose:** Gradually move from accumulation/growth toward greater protection as a meaningful future requirement approaches.

Applicable when:
- A meaningful future requirement exists.
- Its horizon is defined or reasonably identifiable.
- Capital is still in an accumulation/growth phase.
- Gradual protection can improve the probability of meeting the requirement.

It is not the primary strategy when the requirement is already immediate and protection dominates, no meaningful transition exists, or another strategy solves the dominant problem more directly.

Relevant evidence includes the goal timeline and target, current/projected funding, funding gap, payment structure, and current capital/risk position.

### Capital Preservation

**Purpose:** Protect identified capital once it becomes protection-sensitive.

Applicable when:
- Required capital is identifiable.
- The requirement is sufficiently close or otherwise protection-sensitive.
- Capital loss could materially impair the goal.
- Protecting that capital matters more than pursuing additional growth for it.

It is not selected merely because a goal exists or because the goal has a date in the future.

Relevant evidence includes timeline, required and currently funded capital, payment dates/structure, capital already protected, and the consequence of capital loss.

### Debt Reduction

**Purpose:** Reduce or restructure debt when liabilities materially reduce cash-flow capacity, affordability, resilience, or goal funding.

Applicable when:
- Material debt exists.
- Debt servicing constrains cash flow or goal funding.
- Reducing/restructuring the debt can materially improve the relevant financial position.

Debt is not, by itself, sufficient reason to select this strategy.

Relevant evidence includes outstanding balance, effective debt cost, EMI/payment, tenure, prepayment terms, income, expenses, surplus, and competing goals.

### Credit Utilisation

**Purpose:** Address a legitimate funding/timing gap through responsible borrowing.

It is not automatically a solution for every funding gap. Apply the viability gates in Section 6. Borrowing must fail viability when borrowing capacity is insufficient, repayment is unsustainable, financing cost is unjustified, a credible repayment path is absent, borrowing merely transfers an existing debt problem into another form, or an applicable hard financial constraint is violated.

## 8. Canonical Strategy → Variant registry

The target registry contains 16 variants: four under each canonical Strategy Builder strategy.

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

These are target business mappings. Their presence in this registry does not prove that every variant is reachable or implemented in the current runtime. Goal Funding's historical six options are Goal Planner funding paths, not Strategy Builder variants.

## 9. Canonical technique registry

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

### Technique policy statuses

| Status | Meaning |
|---|---|
| Required | The variant cannot be properly executed without it |
| Conditional | Used only when a defined condition exists |
| Optional | May improve implementation but is not necessary |
| Not Applicable | Should not be used in this situation |
| Insufficient Inputs | Relevant, but required information is unavailable |

**Not Applicable and Insufficient Inputs are different states.** Conditional does not mean always apply.

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

Additional policy boundaries:
- Laddering is conditional, not a default Capital Preservation technique. It applies when multiple predictable maturity/payment dates justify staggered maturities.
- Contribution Escalation belongs to Goal Planner / Goal Funding, not the core Strategy Decision Tree.
- Duration / Horizon Matching is a method/analysis, not a separate core technique.
- Tax-specific techniques such as Tax-Efficient Sequencing and Tax-Loss Harvesting are not part of this core four-strategy technique registry; they belong to the appropriate investment/tax implementation layer unless a later business decision explicitly changes that boundary.

## 10. Solution and Action

Preserve the following hierarchy:

~~~text
Strategy
  → Variant
  → Technique
  → Method / Policy
  → Solution
  → Action
~~~

- **Strategy:** High-level financial responsibility selected for the situation.
- **Variant:** Structural form of the selected strategy.
- **Technique:** Reusable mechanism required or permitted by the Strategy + Variant.
- **Method / Policy:** Contextual rule for applying a technique.
- **Solution:** Concrete investor-specific implementation outcome based on the selected path and actual financial inputs.
- **Action:** Executable step derived from the accepted implementation and represented in the Action Plan.

A Technique is not a Solution. A Solution must not merely duplicate a Variant or Technique under a different label.

Asset Mapping is upstream Goal Planner feasibility evidence. Asset Earmarking is a Strategy Builder technique used when the selected path requires deliberate reservation/protection. They are different concepts and must not be aliases.

Prepare the Solution after the Strategy, Variant, Technique, and Method / Policy decisions. The existing-feature audit records additional composition logic in the current runtime; that is current-state implementation evidence, not a separate required target decision level.

## 11. Opportunity cost and implementation comparison

Goal Planner owns goal feasibility and funding-path context. Strategy Builder consumes that context and compares the two presented Strategy options where the required evidence exists.

Relevant comparison dimensions recorded by the feature definition include:
- Goal outcome and funding result.
- Required contribution and timing.
- Liquidity and resource use.
- Debt cost and repayment effects.
- Risk/protection assumptions.
- Competing-goal or shared-resource impact when relevant.

Do not declare one option better without comparable evidence and stated assumptions. The feature definition records that current runtime pass-through of Opportunity Cost evidence and its effect on strategy selection remain unverified. Do not claim those behaviors are already implemented.

## 12. Stress, resilience, and revalidation

Stress / Resilience is evaluated after the implementation proposal in the target flow.

- It tests whether the selected path remains acceptable under defined adverse or changed assumptions.
- It is distinct from Strategy Applicability, Strategy Viability, and Whole-Plan Impact.
- It reuses the canonical decision domains; it must not create a competing recommendation engine.
- If stress findings invalidate the candidate or selected path, the decision must be reconsidered through the canonical decision authority.
- Stress results, warnings, failure conditions, thresholds, and missing-input behavior must follow an explicit source-defined rule; do not invent them.

Whole-Plan / Multi-Goal Impact is evaluated only when the decision is plan-level or a material cross-goal effect exists. A material change can trigger targeted revalidation of affected decisions; it does not automatically require replacing the entire plan.

The existing-feature audit records that formal stress/resilience gating and re-selection policy are not fully established in current runtime. This contract describes the target responsibility, not verified runtime behavior.

## 13. What-If, investor adoption, and plan lifecycle

A What-If scenario is an alternative evaluated against a known baseline. Where supported, retain the baseline, changed inputs/assumptions, projected outcomes, and validation status.

A What-If scenario, saved scenario, generated recommendation, or historical run does not itself change the active Accepted Plan.

~~~text
Accepted Plan
    ↓
Execution Change / What-If
    ↓
Impact Analysis
    ↓
Targeted Revalidation of Affected Decisions
    ↓
Investor Decision
    ↓
Updated Accepted Plan (only after adoption)
    ↓
Updated Action Plan
    ↓
Execution
~~~

Re-evaluate a Strategy Decision when a change materially affects its applicability, viability, applicable constraints, or outcome. A local execution change does not automatically mean the canonical strategy has changed.

An investor-designed path may be captured and evaluated separately when the product permits it. It is not automatically safe, viable, or accepted, and it must not be relabelled as one of the four canonical strategies. It becomes active only through explicit Investor Decision / Accepted Plan adoption.

## 14. Decision output and explanation

A completed decision must preserve enough evidence to explain:

1. The goal and actual financial situation.
2. Goal Planner feasibility/funding evidence used.
3. Applicable constraints and their outcomes.
4. The two Strategy options presented and each option's applicability/viability status.
5. Which applicable candidates failed viability and why.
6. The selected strategy and the evidence supporting the selection, or why no acceptable path exists.
7. The selected variant and its situation mapping.
8. Required and conditional techniques and their policy reasons.
9. The methods/policies used.
10. The concrete Solution proposal.
11. Relevant assumptions, trade-offs, stress/resilience results, and conditional whole-plan impact.
12. The recommendation and whether the investor has adopted it.

A recommendation must not be treated as an Accepted Plan. A historical run must not be treated as the current decision state.

## 15. Existing code and implementation status

The existing-feature audit folder is the source for code-backed current-state findings and identifies relevant backend/frontend modules. Use those findings to distinguish existing behavior from target behavior; do not treat the audit's proposed target language as proof that the target is already implemented.

The current audit records unresolved differences including:
- Legacy strategy identifiers and Goal Funding references in current-state code.
- Current runtime ordering that differs from the target decision flow.
- Split or overlapping rule ownership in the existing decision path.
- Variant selection occurring inside recommendation in the audited runtime.
- Current runtime composition and technique execution influencing the decision path.
- Incomplete formal stress/resilience gating and re-selection behavior.
- Unverified scenario isolation, persistence, investor adoption, and active-plan updates.
- Inconsistent current runtime use of the term Solution across strategy records.

These are audit findings, not claims that a fix has been implemented by this document.

### Required target-state distinction

- The target Strategy Builder has four strategies, not five.
- Goal Funding and its contribution/funding mechanisms remain owned by Goal Planner / Goal Feasibility.
- The target flow has no separate eight-eligibility-fits stage.
- **Every decision presents exactly two Strategy options.** This is mandatory; do not use a dynamic option count.
- Each option's applicability, viability, evidence, assumptions, and trade-offs must be shown honestly. Showing an option does not mean endorsing it.
- The target sequence evaluates and presents the two options for investor review; for each valid implementation, Strategy → Variant → Technique / Method leads to a concrete Solution proposal.
- Goal Planner supplies goal-feasibility/funding context, not a Strategy. The integration between its feasibility output and Strategy Builder is a later connection and must not be assumed here.
- Stress / Resilience and conditional Whole-Plan Impact remain distinct responsibilities.
- Decision / Recommendation, Investor Decision, Accepted Plan, Action Plan, and Execution remain separate lifecycle states.
- No Acceptable Strategy / No Acceptable Path is a valid result.

Exact score weights, selection tie-breaks, numerical thresholds, stress taxonomy, materiality thresholds, and any runtime behavior not established by the two references must not be invented in implementation.

## Notes

### Scoring and 8 Eligibility Fits — Remove Completely

- **Scoring has no role in the Strategy Builder system.** Do not use a scoring model, score components, score totals, weights, thresholds, or score-based ranking to generate, order, select, or influence the strategy alternatives.
- **The 8 Eligibility Fits have no role in the Strategy Builder system.** Remove them completely; they must not exist as a separate stage, gate, evaluation, or decision input.
- Neither Scoring nor the 8 Eligibility Fits may be used by the frontend, backend, recommendation flow, or any other part of the system.
- Treat both as removed from the target system—not as pending features, optional checks, legacy fallbacks, or alternate decision paths.
