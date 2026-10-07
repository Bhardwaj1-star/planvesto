# Strategy Decision Tree

**Document Type:** Canonical Business Decision Document  
**Status:** Final Business Architecture  
**Scope:** Strategy Decision Tree / Real-Life Decision Cases

---

## 1. Purpose

This document defines the canonical Strategy Decision Tree for PlanVesto.

It determines:

- which strategy can apply to a financial situation;
- whether that strategy is viable under the investor's constraints;
- which strategy should be selected;
- which variant should be used;
- which techniques are required or conditional; and
- how the final solution is derived.

This is a **business decision document**, not an implementation specification. It is the benchmark against which the current code will later be audited.

---

## 2. Core Principle

The system must not select a strategy merely because a goal belongs to a particular category.

The decision is based on:

**Goal + Goal Situation + Financial State + Funding Position + Constraints + Whole-Plan Impact**

Therefore, the same goal can legitimately use different strategies in different situations.

Example: Education may require Progressive De-risking when it is several years away, Capital Preservation when the next payment is near, Debt Reduction when existing debt suppresses funding capacity, or Credit Utilisation when a responsible residual funding gap remains.

---

# 3. Canonical Strategy Decision Tree

| Step | Decision Layer | Purpose | Output |
|---|---|---|---|
| 1 | Canonical Goal | Identify the standardized goal | Canonical goal ID |
| 2 | Goal Context | Understand the actual requirement | Timeline, target, payment pattern, priority |
| 3 | Financial State | Understand the investor's position | Income, expenses, assets, liabilities, liquidity |
| 4 | Goal Funding / Feasibility | Determine whether and how the goal can be funded | Funding status, gap, capacity |
| 5 | Whole-Plan Impact | Check interaction with other goals/resources | Conflicts and trade-offs |
| 6 | Hard Constraints | Remove financially unacceptable paths | Constraint pass/fail |
| 7 | Strategy Applicability | Determine which strategies legitimately fit | Candidate strategies |
| 8 | Strategy Viability | Determine whether a candidate can actually work | Viable / Failed |
| 9 | Strategy Selection | Compare viable candidates | Selected strategy |
| 10 | Variant Selection | Select implementation architecture | Selected variant |
| 11 | Technique Selection | Identify required/conditional techniques | Technique set |
| 12 | Technique Conditions / Method | Determine how techniques operate | Method/policy |
| 13 | Solution | Produce the concrete financial solution | Recommended solution |
| 14 | Action | Translate solution into execution | Action plan |

---

# 4. Canonical Strategy Set

The Strategy Builder has four canonical strategies:

| Strategy | Core Financial Problem |
|---|---|
| **Progressive De-risking** | A future requirement needs gradual reduction of risk as the requirement approaches |
| **Capital Preservation** | Identified capital needs protection from loss or timing risk |
| **Debt Reduction** | Existing debt materially constrains cash flow, affordability, or goal funding |
| **Credit Utilisation** | A legitimate funding/timing gap may be responsibly financed |

### Important boundary

**Goal Funding is not a fifth Strategy Builder strategy.**

Goal Funding belongs to the **Goal Planner / Goal Funding / Feasibility layer**. Funding mechanisms such as contribution increases, SIPs, step-ups and lump-sum funding are not peer Strategy Builder strategies.

---

# 5. Strategy Applicability Rules

## 5.1 Progressive De-risking

**Purpose:** Gradually move from accumulation/growth toward greater protection as a meaningful future requirement approaches.

**Applicable when:**
- a meaningful future requirement exists;
- the requirement has a defined or reasonably identifiable horizon;
- capital is still in an accumulation/growth phase; and
- progressive protection can improve the probability of meeting the requirement.

**Not primary when:**
- the requirement is already immediate and protection is dominant;
- there is no meaningful future funding/protection transition; or
- another strategy clearly solves the dominant problem.

**Required inputs:** goal timeline, future target, current/projected funding, funding gap, payment structure, current capital/risk position.

---

## 5.2 Capital Preservation

**Purpose:** Protect identified capital once it becomes protection-sensitive.

**Applicable when:**
- required capital is identifiable;
- the requirement is sufficiently close or protection-sensitive;
- capital loss could materially impair the goal; and
- protection is more important than additional growth for that capital.

**Not primary when:** the goal remains in a long accumulation phase or progressive transition is more appropriate.

**Required inputs:** timeline, required capital, current funding, payment dates, payment structure, capital already protected, consequence of capital loss.

---

## 5.3 Debt Reduction

**Purpose:** Reduce or restructure debt when liabilities materially reduce financial capacity, affordability, resilience, or goal funding.

**Applicable when:**
- material debt exists;
- debt servicing constrains cash flow or goal funding; and
- reducing/restructuring debt can materially improve the financial position.

**Not applicable when:** debt has no meaningful impact on the relevant decision or debt reduction does not materially improve the position.

**Required inputs:** outstanding balance, effective debt cost, EMI/payment, tenure, prepayment terms, income, expenses, surplus, competing goals.

---

## 5.4 Credit Utilisation

**Purpose:** Solve a legitimate funding or timing gap through responsible borrowing.

Credit is not automatically a solution for every funding gap.

**Candidate only when:**
1. a genuine funding/timing gap exists;
2. reasonable own-resource funding has been considered;
3. borrowing capacity is sufficient;
4. repayment is sustainable;
5. financing cost is economically justified; and
6. a credible repayment path exists.

### Mandatory viability gates

| Gate | Question |
|---|---|
| Funding Need | Is there a genuine funding/timing gap? |
| Own Resources | Have reasonable existing resources been considered? |
| Borrowing Capacity | Can the required amount be borrowed responsibly? |
| EMI Capacity | Can the repayment be sustained? |
| Financing Cost | Is borrowing economically justified? |
| Repayment Path | Is there a credible repayment path? |

Failure of a material gate means **Credit Utilisation = FAIL**.

---

# 6. Applicability vs Viability

These are separate decisions.

**Applicability:** Can this strategy legitimately apply to the situation?

**Viability:** Even if applicable, can it actually work for this investor under the current constraints?

Example: a genuine education funding gap can make Credit Utilisation applicable. If borrowing capacity is insufficient or EMI is unsustainable, Credit Utilisation fails viability and must not be recommended.

---

# 7. Strategy Variants

## Progressive De-risking

| Situation | Variant |
|---|---|
| Single future goal date | Goal-Date Glide Path |
| Multiple defined future payments | Payment-Tranche Glide Path |
| Recurring future requirement | Recurring-Cashflow Glide Path |
| Accumulation transitioning into recurring income | Income-Transition Glide Path |

## Capital Preservation

| Situation | Variant |
|---|---|
| Entire required capital needs protection | Full-Goal Preservation |
| Immediate/next payment needs protection | First-Payment Preservation |
| Repeating reserve requirement | Rolling Reserve Preservation |
| Only core/required capital needs protection | Protected-Core Preservation |

## Debt Reduction

| Situation | Variant |
|---|---|
| Debt creates a goal funding gap | Goal-Gap Debt Reduction |
| EMI burden suppresses cash-flow capacity | EMI-Relief Debt Reduction |
| Remaining debt/capital gap needs optimisation | Residual-Gap Debt Reduction |
| Debt and another goal must be coordinated | Goal-Linked Debt Reduction |

## Credit Utilisation

| Situation | Variant |
|---|---|
| Small residual funding gap | Residual-Gap Bridge |
| Defined portion intentionally financed | Partial-Goal Financing |
| Borrowing constrained by sustainable EMI | EMI-Cap Financing |
| Temporary timing mismatch | Timing-Bridge Financing |

---

# 8. Canonical Technique Set

A **Technique is not a Solution**.

The core Strategy Decision Tree technique set is:

| Technique | Primary Purpose |
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

### Reclassification boundaries

- **Contribution Escalation** belongs to the Goal Planner / Goal Funding layer, not the core Strategy Decision Tree.
- **Duration / Horizon Matching** is a decision/analysis method used to assess timing suitability, not a separate core technique.
- Tax-specific techniques such as Tax-Efficient Sequencing and Tax-Loss Harvesting should not be forced into the four-strategy decision tree; they belong to the appropriate investment/tax implementation layer unless a later business decision explicitly promotes them.

---

# 9. Technique Policy

| Classification | Meaning |
|---|---|
| **Required** | Variant cannot be properly executed without it |
| **Conditional** | Used only when a defined condition exists |
| **Optional** | May improve implementation but is not necessary |
| **Not Applicable** | Should not be used in the situation |
| **Insufficient Inputs** | Relevant, but required information is unavailable |

**Not Applicable ≠ Insufficient Inputs.**

---

# 10. Strategy → Variant → Technique Rules

## Progressive De-risking

| Variant | Required | Conditional |
|---|---|---|
| Goal-Date Glide Path | Glide Path | Bucketing, Cash-flow Matching |
| Payment-Tranche Glide Path | Glide Path, Cash-flow Matching | Bucketing |
| Recurring-Cashflow Glide Path | Bucketing, Cash-flow Matching | Glide Path |
| Income-Transition Glide Path | Glide Path, Bucketing | Cash-flow Matching |

## Capital Preservation

| Variant | Required | Conditional |
|---|---|---|
| Full-Goal Preservation | Bucketing, Asset Earmarking | Cash-flow Matching, Laddering |
| First-Payment Preservation | Cash-flow Matching, Bucketing | Asset Earmarking |
| Rolling Reserve Preservation | Bucketing, Cash-flow Matching | Laddering |
| Protected-Core Preservation | Asset Earmarking, Bucketing | Cash-flow Matching, Laddering |

**Laddering is conditional, not a default Capital Preservation technique.** It applies when multiple predictable maturity/payment dates justify staggered maturities.

## Debt Reduction

| Variant | Required | Conditional |
|---|---|---|
| Goal-Gap Debt Reduction | Goal Segmentation, Debt Repayment Prioritisation | Debt Cost Optimisation, Cash-flow Matching, Debt Prepayment Optimisation |
| EMI-Relief Debt Reduction | EMI Capacity Analysis, Debt Cost Optimisation | Debt Repayment Prioritisation, Debt Prepayment Optimisation |
| Residual-Gap Debt Reduction | Goal Segmentation, Cash-flow Matching | Debt Repayment Prioritisation, Debt Cost Optimisation, Debt Prepayment Optimisation |
| Goal-Linked Debt Reduction | Goal Segmentation, Cash-flow Matching | Debt Cost Optimisation, Debt Prepayment Optimisation |

## Credit Utilisation

| Variant | Required | Conditional |
|---|---|---|
| Residual-Gap Bridge | Borrowing Capacity Analysis, Financing Cost Comparison | Cash-flow Matching, EMI Capacity Analysis |
| Partial-Goal Financing | Financing Cost Comparison, Goal Segmentation | Borrowing Capacity Analysis, EMI Capacity Analysis |
| EMI-Cap Financing | EMI Capacity Analysis, Borrowing Capacity Analysis | Financing Cost Comparison |
| Timing-Bridge Financing | Cash-flow Matching, Financing Cost Comparison | Borrowing Capacity Analysis, EMI Capacity Analysis |

---

# 11. Hard Rejection Rules

### Credit Utilisation

Credit must fail when:
- borrowing capacity is insufficient;
- EMI is unsustainable;
- financing cost is unjustified;
- repayment path is undefined;
- borrowing merely transfers an existing debt problem into another form; or
- hard financial constraints are violated.

### Debt Reduction

Debt Reduction must not be selected merely because debt exists. It should be selected when debt reduction materially improves cash-flow capacity, goal funding, affordability, or resilience.

### Capital Preservation

Capital Preservation must not automatically be selected simply because a goal exists. It becomes primary when the capital has become protection-sensitive.

### Progressive De-risking

Progressive De-risking must not automatically be selected simply because a goal has a future date. It requires a meaningful future requirement where gradual risk reduction improves the probability of meeting that requirement.

---

# 12. No Acceptable Strategy

The Decision Tree must support a legitimate outcome where no strategy is acceptable.

```
Candidate Strategies
        ↓
Applicability
        ↓
Viability
        ↓
All Candidates Fail
        ↓
NO ACCEPTABLE STRATEGY
```

This is **not a system error**.

Possible next decisions include changing the goal timeline, increasing funding, reducing the target, reducing debt, changing goal priority, changing the funding structure, or accepting that the goal is currently infeasible.

The system must never force a strategy merely to produce a recommendation.

---

# 13. Goal-Specific Situation Logic

The following rules demonstrate how the same strategy framework is applied differently according to the actual situation.

| Goal | Situation | Strategy | Variant |
|---|---|---|---|
| Retirement | Long accumulation horizon | Progressive De-risking | Goal-Date Glide Path |
| Retirement | Required retirement capital needs protection | Capital Preservation | Protected-Core Preservation |
| Retirement | Income transition | Progressive De-risking | Income-Transition Glide Path |
| Retirement | Debt suppresses retirement funding | Debt Reduction | EMI-Relief Debt Reduction |
| Marriage | Several years away | Progressive De-risking | Goal-Date Glide Path |
| Marriage | Capital ready and date near | Capital Preservation | Full-Goal Preservation |
| Marriage | Multiple scheduled payments | Progressive De-risking | Payment-Tranche Glide Path |
| Marriage | Existing debt suppresses funding | Debt Reduction | Goal-Gap Debt Reduction |
| Vehicle | Purchase several years away | Progressive De-risking | Goal-Date Glide Path |
| Vehicle | Purchase near and capital ready | Capital Preservation | Full-Goal Preservation |
| Vehicle | Existing EMI affects affordability | Debt Reduction | EMI-Relief Debt Reduction |
| Vehicle | Partial financing justified | Credit Utilisation | Partial-Goal Financing |
| Dream Home | Down-payment accumulation | Progressive De-risking | Goal-Date Glide Path |
| Dream Home | Purchase approaching, core capital ready | Capital Preservation | Protected-Core Preservation |
| Dream Home | Existing debt reduces affordability | Debt Reduction | EMI-Relief Debt Reduction |
| Dream Home | Defined financing requirement | Credit Utilisation | Partial-Goal Financing |
| Dream Home | Gap too large / EMI unsustainable | No acceptable path | — |
| Education | Long education horizon | Progressive De-risking | Goal-Date Glide Path |
| Education | Staged education payments | Progressive De-risking | Payment-Tranche Glide Path |
| Education | Next tuition payment near | Capital Preservation | First-Payment Preservation |
| Education | Core capital needs protection | Capital Preservation | Protected-Core Preservation |
| Education | Responsible residual gap | Credit Utilisation | Residual-Gap Bridge |
| Education | Defined portion intentionally financed | Credit Utilisation | Partial-Goal Financing |
| Education | Existing debt suppresses funding | Debt Reduction | Goal-Gap Debt Reduction |
| Vacation | Future accumulation | Progressive De-risking | Goal-Date Glide Path |
| Vacation | Near-term and funds available | Capital Preservation | Full-Goal Preservation |
| Vacation | Recurring requirement | Progressive De-risking | Recurring-Cashflow Glide Path |
| Vacation | Existing debt creates pressure | Debt Reduction | EMI-Relief Debt Reduction |
| Vacation | Financing unaffordable | No acceptable path | — |
| Debt Freedom | High-cost debt priority | Debt Reduction | Goal-Gap Debt Reduction |
| Debt Freedom | EMI burden too high | Debt Reduction | EMI-Relief Debt Reduction |
| Debt Freedom | Multiple debts need ordering | Debt Reduction | Goal-Gap / Goal-Linked |
| Debt Freedom | Debt payoff competes with another goal | Debt Reduction | Goal-Linked Debt Reduction |
| Debt Freedom | New expensive borrowing required | No acceptable Credit path | — |
| Wealth Creation | Long-term accumulation | Progressive De-risking | Goal-Date Glide Path |
| Wealth Creation | Target approaching | Capital Preservation | Protected-Core Preservation |
| Wealth Creation | High-cost debt suppresses accumulation | Debt Reduction | Goal-Gap Debt Reduction |
| Wealth Creation | Defined leverage with sustainable repayment | Credit Utilisation | EMI-Cap Financing |
| FIRE / Passive Income | Long accumulation | Progressive De-risking | Income-Transition Glide Path |
| FIRE / Passive Income | Target approaching | Capital Preservation | Protected-Core Preservation |
| FIRE / Passive Income | Passive-income transition | Progressive De-risking | Income-Transition Glide Path |
| FIRE / Passive Income | Debt reduces passive-income cash flow | Debt Reduction | EMI-Relief Debt Reduction |
| FIRE / Passive Income | Recurring withdrawals started | Capital Preservation | Rolling Reserve Preservation |
| FIRE / Passive Income | Unsustainable borrowing required | No acceptable path | — |
| Others | Fixed future requirement | Progressive De-risking | Goal-Date Glide Path |
| Others | Immediate capital requirement | Capital Preservation | Full-Goal Preservation |
| Others | Debt materially constrains objective | Debt Reduction | Goal-Gap Debt Reduction |
| Others | Sustainable residual gap | Credit Utilisation | Residual-Gap Bridge |
| Others | No strategy satisfies constraints | No acceptable strategy | — |

**Retirement and FIRE / Passive Income remain separate canonical goals.**

---

# 14. Technique ≠ Solution

The canonical hierarchy is:

```
Strategy
   ↓
Variant
   ↓
Technique
   ↓
Method / Policy
   ↓
Solution
   ↓
Action
```

Example:

**Progressive De-risking**  
→ **Payment-Tranche Glide Path**  
→ **Cash-flow Matching**  
→ match future liabilities with appropriate resources  
→ protect the next defined education payments using suitable liquid/low-risk resources  
→ execute the required funding/asset changes.

A technique must never be renamed or treated as a solution merely because it produces an implementation outcome.

---

# 15. Decision Output Contract

Every completed decision should be able to explain:

1. What is the goal?
2. What is the actual financial situation?
3. What funding/feasibility problem exists?
4. Which constraints apply?
5. Which strategies are applicable?
6. Which candidates fail viability and why?
7. Why was the selected strategy chosen?
8. Why was the variant selected?
9. Which techniques are required?
10. Which techniques are conditional and why?
11. What concrete solution results?
12. What actions are required?

This makes the recommendation explainable and auditable.

---

# 16. Final Canonical Flow

```
CANONICAL GOAL
      ↓
GOAL CONTEXT
      ↓
FINANCIAL STATE
      ↓
GOAL FUNDING / FEASIBILITY
      ↓
WHOLE-PLAN IMPACT
      ↓
HARD CONSTRAINTS
      ↓
STRATEGY APPLICABILITY
      ↓
┌─────────────────────────────┐
│ Progressive De-risking      │
│ Capital Preservation        │
│ Debt Reduction              │
│ Credit Utilisation          │
└─────────────────────────────┘
      ↓
STRATEGY VIABILITY
      ↓
STRATEGY SELECTION
      ↓
VARIANT SELECTION
      ↓
TECHNIQUE SELECTION
      ↓
TECHNIQUE CONDITIONS / METHOD
      ↓
SOLUTION
      ↓
ACTION
```

---

# 17. Canonical Decision Principle

The Strategy Decision Tree does **not** answer:

> “Which strategy belongs to this goal?”

It answers:

> **“Given this goal, this investor, this financial state, this funding situation, and these constraints, which strategy is applicable, viable, and most appropriate—and how should it be implemented?”**

This document is the canonical business reference for the Strategy Decision Tree. Existing implementation must be audited against this reference before code changes are made.
