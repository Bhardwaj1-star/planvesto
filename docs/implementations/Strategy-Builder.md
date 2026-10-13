# Strategy Builder — Financial Planner Guide

## 1. Purpose

Strategy Builder prepares two strategy options for an investor's financial situation, explains their suitability and trade-offs, and supports an informed investor decision. It does not automatically choose or adopt a strategy on the investor's behalf.

**Exactly four strategies belong to Strategy Builder:**
1. Progressive De-risking
2. Capital Preservation
3. Debt Reduction
4. Credit Utilisation

**Goal Funding is not a fifth strategy.** Goal Planner / Goal Feasibility owns goal requirements, feasibility, and funding paths such as SIP, lump sum, step-up contributions, and combinations of funding mechanisms.

If no option is acceptable, the correct outcome is **No Acceptable Strategy / No Acceptable Path**. The requirement to show two options never justifies presenting an unsuitable or unviable option as recommended.

## 2. How it fits into financial planning

| Component | Responsibility |
|---|---|
| Goal Planner | Establishes goal requirements, funding gap, feasibility, and funding-path context |
| Moneywheel | Supplies canonical financial measurements and their assumptions/availability |
| Constraint / Safety Evaluation | Identifies applicable hard constraints, warnings, preferences, conflicts, and missing evidence |
| Strategy Builder | Assesses strategy applicability and viability, develops two alternatives, selects variants/techniques, and prepares solution proposals |
| Investor decision / Accepted Plan | Makes a proposal active only after explicit investor acceptance |
| Action Plan | Converts the adopted plan into execution actions |

Goal Planner provides feasibility and funding context, not a preselected Strategy. The exact integration between Goal Planner and Strategy Builder must be defined separately; do not assume a dependency that has not been agreed.

## 3. Decision flow

1. Understand the goal and the investor's current financial situation.
2. Review relevant Goal Planner evidence and applicable constraints.
3. Generate exactly two options from the four canonical strategies.
4. Assess each option's applicability and viability separately.
5. For each valid option, identify the appropriate Variant, Technique, and Method/Policy.
6. Prepare a concrete investor-specific Solution proposal.
7. Evaluate relevant stress/resilience conditions and compare assumptions, risks, and trade-offs.
8. Present both options and the evidence honestly.
9. Let the investor decide whether to adopt a proposal.
10. After adoption, update the Accepted Plan and downstream Action Plan through the appropriate lifecycle.

Whole-Plan / Multi-Goal Impact is conditional: assess it when shared resources, competing goals, a new goal, or an existing Accepted Plan may be materially affected. It is not a mandatory step for every isolated decision.

## 4. Applicability, viability, and two-option presentation

These are different questions:

- **Applicability:** Does this strategy fit the type of problem and the investor's situation?
- **Viability:** Could the strategy actually work under the investor's financial conditions and applicable constraints?
- **Recommendation:** How should the options, evidence, and trade-offs be explained?
- **Adoption:** Has the investor explicitly accepted a proposal?

A strategy can be applicable but not viable. A warning or poor ratio is not automatically a hard blocker; use the approved rule for that condition and do not invent thresholds.

### Mandatory two-option rule

- Present exactly two Strategy options for each decision.
- Both options must come from the four canonical strategies; Goal Funding is excluded.
- Show each option's applicability/viability status and its supporting reasons.
- Compare benefits, limitations, risks, assumptions, and trade-offs where evidence is available.
- Do not invent scores, score weights, numerical ranking thresholds, or tie-breaking rules.
- If one or both options fail a check, still show two options but label the failed status honestly. Do not pretend a failed option is suitable or force the investor to accept either.
- If neither option is acceptable, state **No Acceptable Strategy / No Acceptable Path**.

### Credit Utilisation viability

Credit Utilisation is intended for a legitimate funding or timing gap; it is not a default answer to every shortfall. It should fail viability if a material gate fails, including:
- No genuine funding/timing gap exists.
- Reasonable own-resource funding has not been considered.
- Borrowing capacity is insufficient.
- EMI/repayment is unsustainable.
- Financing cost is not economically justified.
- There is no credible repayment path.
- An applicable hard financial constraint would be violated.

## 5. The four canonical strategies

### 5.1 Progressive De-risking

**Purpose:** Gradually move from accumulation/growth toward greater protection as a meaningful future requirement approaches.

Consider it when a future requirement and horizon are identifiable, capital is still accumulating, and gradual protection can improve the chance of meeting the requirement. It is not the primary strategy when the need is immediate and protection already dominates, no meaningful transition exists, or another strategy addresses the main problem more directly.

Relevant evidence: goal date and target, current/projected funding, funding gap, payment structure, and current capital/risk position.

### 5.2 Capital Preservation

**Purpose:** Protect identified capital when it becomes sensitive to loss because a requirement is near or otherwise needs protection.

Consider it when required capital is identifiable, capital loss could materially impair the goal, and protection matters more than additional growth for that capital. A future goal date alone is not sufficient reason to select it.

Relevant evidence: timeline, required and funded capital, payment dates, already-protected capital, and the consequence of capital loss.

### 5.3 Debt Reduction

**Purpose:** Reduce or restructure debt when it materially limits cash flow, affordability, resilience, or goal funding.

Consider it when material debt constrains the investor's position and reducing/restructuring it can improve that position. Debt alone does not prove this is the best strategy.

Relevant evidence: outstanding balance, debt cost, EMI/payment, tenure, prepayment terms, income, expenses, surplus, liquidity, and competing goals.

### 5.4 Credit Utilisation

**Purpose:** Address a legitimate funding or timing gap through responsible borrowing.

Use only after checking borrowing capacity, sustainable repayment, financing cost, a credible repayment path, and applicable constraints. Borrowing is not viable merely because it fills a gap; it may simply transfer or worsen an existing debt problem.

## 6. Canonical Strategy → Variant registry

The target business model defines 16 variants, four under each Strategy. These mappings describe intended business logic; their listing here does not prove that each is currently implemented in the live system.

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

## 7. Technique registry and policy

A **Technique** is a reusable implementation mechanism. Its use depends on the selected Strategy + Variant; it is not automatically required in every case.

| Technique | Primary purpose |
|---|---|
| Glide Path | Gradually change risk/capital positioning as a requirement approaches |
| Bucketing | Organize resources by timing or liability needs |
| Cash-flow Matching | Match future cash requirements with suitable resources/cash flows |
| Laddering | Stagger maturities/resources against multiple predictable requirements |
| Asset Earmarking | Deliberately reserve resources for a goal or protected capital pool |
| Goal Segmentation | Separate competing goal, debt, and resource requirements |
| Debt Repayment Prioritisation | Determine which debt receives repayment priority |
| Debt Cost Optimisation | Reduce or optimise effective debt cost |
| Debt Prepayment Optimisation | Assess whether available capital should be used for prepayment |
| EMI Capacity Analysis | Determine sustainable repayment capacity |
| Borrowing Capacity Analysis | Determine how much borrowing can responsibly be supported |
| Financing Cost Comparison | Assess whether borrowing is economically justified |

### Technique status meanings

- **Required:** The variant cannot be properly executed without it.
- **Conditional:** Use only when a defined condition exists.
- **Optional:** May help implementation but is not essential.
- **Not Applicable:** Does not fit the situation.
- **Insufficient Inputs:** Relevant, but required information is unavailable.

Not Applicable and Insufficient Inputs are different. Conditional does not mean always apply.

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

Additional boundaries:
- Laddering is conditional, especially when multiple predictable payment/maturity dates justify staggered maturities.
- Contribution Escalation belongs to Goal Planner's funding domain, not the core Strategy Decision Tree.
- Duration/Horizon Matching is a method/analysis, not a separate core technique.
- Tax-specific techniques are outside this core registry unless ownership is explicitly changed through a business decision.

## 8. Strategy-to-solution hierarchy

Preserve this hierarchy:

**Strategy → Variant → Technique → Method/Policy → Solution → Action**

- **Strategy:** High-level financial responsibility selected for the situation.
- **Variant:** Structural form of that strategy.
- **Technique:** Reusable mechanism required or permitted by the Strategy + Variant.
- **Method/Policy:** Contextual rule for applying a technique.
- **Solution:** Concrete investor-specific implementation proposal.
- **Action:** Executable step derived from an adopted implementation and represented in the Action Plan.

A Technique is not a Solution, and a Solution must not merely duplicate a Variant or Technique under another label.

Asset Mapping is Goal Planner evidence associating an asset with a goal. Asset Earmarking is a deliberate reservation/protection technique. Mapping alone does not reserve or lock an asset.

## 9. Comparison, Opportunity Cost, and stress/resilience

Compare the two options on a consistent baseline and explain the evidence available for:
- Goal outcome and funding result.
- Contribution requirements and timing.
- Liquidity and resource use.
- Debt cost and repayment effects.
- Risk/protection assumptions.
- Competing-goal or shared-resource effects when material.
- Key assumptions, limitations, and missing evidence.

**Opportunity Cost** helps explain the material benefit given up by choosing one path instead of another. It is not a standalone rule that automatically selects a strategy. Do not declare an option better without comparable evidence and stated assumptions.

**Stress/resilience** checks whether a proposed path remains acceptable under defined adverse or changed assumptions. It is distinct from applicability, viability, and whole-plan impact. Use established rules and thresholds; do not invent them. If stress findings undermine a path, reconsider it through the same decision authority rather than creating a separate recommendation engine.

## 10. Whole-plan impact and revalidation

Check whole-plan impact only when the decision may materially affect shared resources, competing goals, a new goal, or an existing Accepted Plan. Identify affected goals, shared-resource conflicts, before/after outcomes where available, and decisions that need revalidation.

A material change may require targeted recalculation/revalidation; it does not automatically require rebuilding or replacing the entire plan. Do not rebuild unrelated decisions.

## 11. What-If and investor adoption

A What-If scenario compares changed assumptions with a known baseline. A saved scenario, recommendation, or historical run is not proof that the investor adopted it.

Keep these states separate:
- Proposed Strategy / Solution
- Investor Decision
- Accepted Plan
- Action Plan
- Execution

Only explicit investor acceptance makes the proposal active. Re-evaluate a strategy if a change materially affects applicability, viability, constraints, or outcome. An investor-designed path may be assessed separately where supported, but must not be automatically treated as safe, viable, accepted, or renamed as one of the four canonical strategies.

## 12. Required explanation to the investor

For each decision, explain:
1. The goal and relevant financial situation.
2. Goal Planner funding/feasibility evidence used.
3. Applicable constraints and their outcomes.
4. Both Strategy options and each one's applicability/viability status.
5. Why a candidate failed viability, if applicable.
6. The evidence, assumptions, benefits, risks, and trade-offs for each option.
7. The selected Variant, technique statuses, and methods/policies for each valid proposal.
8. The concrete Solution proposal.
9. Relevant stress/resilience and whole-plan impact findings.
10. The recommendation and whether the investor has adopted it.

A recommendation is not an Accepted Plan, and historical output is not necessarily the current decision state.

## 13. Important limitations

- The four-strategy allowlist is authoritative; Goal Funding and its funding mechanisms belong to Goal Planner.
- Exactly two options must be presented, but neither must be misrepresented as suitable.
- Do not introduce scoring, score weights, score-based rankings, or a separate eight-eligibility-fits stage.
- Do not invent thresholds, viability rules, stress criteria, or tie-breakers that have not been defined.
- Do not automatically choose or adopt a strategy, change goal priority, earmark assets, or overwrite an Accepted Plan.
- This guide describes the intended business model; it does not prove that every workflow is currently implemented in the live system.
