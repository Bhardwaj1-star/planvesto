# 15 — Asset Mapping vs Asset Earmarking — Canonical Real-Life Decision Case

**Parent area:** `docs/Decision tree/Real-Life Decision Cases/`  
**Purpose:** Establish the business boundary between **Asset Mapping** and **Asset Earmarking** through real-life decision cases without modifying current-state/audit documents.  
**Status:** **CANONICAL BUSINESS DECISION DOCUMENT — NOT YET IMPLEMENTED IN CODE**

---

## 1. Why This Case Is Required

Asset Mapping and Asset Earmarking can look similar because both connect assets/resources with goals.

They answer different questions and therefore belong to different decision layers.

> **Asset Mapping = Which existing resources are associated with the goal for planning purposes?**

> **Asset Earmarking = Which resources should be intentionally reserved/protected for that goal as part of the selected strategy?**

They must not be treated as duplicate functions, duplicate techniques, or interchangeable names.

---

## 2. Canonical Boundary

| Dimension | Asset Mapping | Asset Earmarking |
|---|---|---|
| Primary question | What existing resources are mapped to this goal? | What resources should be intentionally reserved for this goal? |
| Decision layer | Goal Planning / Goal Funding / Feasibility | Strategy / Technique / Implementation Design |
| Timing | Before or during goal feasibility analysis | After a strategy/variant requires or benefits from earmarking |
| Nature | Planning association | Strategic allocation/protection decision |
| Purpose | Measure how mapped assets contribute to funding | Create a deliberate protected/assigned resource pool |
| Can exist without strategy selection? | Yes | Usually requires strategic/implementation context |
| Output | Mapped asset/resource and projected contribution | Earmarked/protected resource allocation |
| Ownership | Goal Planner | Strategy Builder / Technique layer |
| Example | Existing ₹10L mutual fund mapped to Education | ₹8L of suitable assets deliberately ring-fenced for Education's near-term payments |

---

## 3. Real-Life Case A — Existing Asset Mapped to a Goal

### Situation

An investor has an existing mutual fund portfolio worth ₹10 lakh.

They have an Education goal with a future funding requirement.

The investor says:

> "Consider this existing portfolio for my Education goal."

### Correct decision

The system performs **Asset Mapping**.

It records that the asset/resource is associated with the Education goal and projects the amount expected to contribute toward the goal.

### What it does NOT mean

The system has not yet decided that the entire portfolio must be protected, segregated, sold, or otherwise restricted.

### Decision chain

```Financial State
      ↓
Existing Asset
      ↓
Goal = Education
      ↓
ASSET MAPPING
      ↓
Projected Mapped Contribution
      ↓
Funding Gap / Feasibility
```

**Conclusion:** Asset Mapping belongs upstream of Strategy Decision.

---

## 4. Real-Life Case B — Strategy Requires Protected Capital

### Situation

The Education goal is approaching.

The selected strategy is:

**Capital Preservation → Protected-Core Preservation**

The strategy determines that a defined portion of the required education capital should be deliberately protected from unrelated use and inappropriate risk.

### Correct decision

The system may use **Asset Earmarking**.

The purpose is no longer merely to say that an asset contributes to Education.

The purpose is to establish:

> "This portion of capital is intentionally reserved for this goal."

### Decision chain

```
Goal Context
      ↓
Goal Feasibility
      ↓
Strategy Selection
      ↓
Capital Preservation
      ↓
Protected-Core Preservation
      ↓
ASSET EARMARKING
      ↓
Method / Policy
      ↓
Solution / Action
```

**Conclusion:** Asset Earmarking belongs downstream of strategic decisioning.

---

## 5. Real-Life Case C — Same Asset, Different Meaning

Suppose an investor owns ₹15 lakh in assets.

### Step 1 — Mapping

₹10 lakh is mapped to Education for planning.

This answers:

> How much of the existing resource is being considered for this goal?

### Step 2 — Earmarking

After strategy selection, ₹7 lakh is deliberately earmarked as protected Education capital.

This answers:

> How much of the resource should actually be reserved/protected for this goal?

Therefore:

**Mapped amount and earmarked amount do not have to be identical.**

A mapped asset can remain flexible while an earmarked portion becomes strategically protected.

---

## 6. Real-Life Case D — One Asset Mapped to Multiple Goals

An investor has a ₹20 lakh investment portfolio.

They have:

- Education
- Retirement
- Dream Home

The portfolio can be considered in the planning analysis of multiple goals, subject to the system's allocation rules.

This is **Asset Mapping**.

However, the system must not silently earmark the same capital as fully protected for multiple incompatible goals.

If strategic earmarking creates a conflict, the conflict must be surfaced and resolved through the appropriate planning/strategy decision.

### Rule

> **Mapping can represent planning consideration; earmarking creates an intentional commitment.**

---

## 7. Real-Life Case E — Goal Cancelled

An investor cancels the Education goal.

### Correct behavior

The system removes or invalidates the **goal mapping** associated with that goal according to the goal lifecycle.

It must not automatically delete the underlying asset from Financial State.

The asset remains an investor-owned financial resource and can be:

- remapped to another goal;
- left unallocated;
- considered for another strategy;
- retained as general portfolio capital.

### Canonical rule

> **Cancel Goal ≠ Cancel Asset.**

If the asset was previously earmarked, the system must additionally determine whether that earmarking should be released.

---

## 8. Real-Life Case F — Earmarked Asset Is Not Automatically a Product Recommendation

Earmarking does not mean:

> "Buy product X."

For example, an Education strategy may determine that ₹5 lakh needs to be protected for a near-term payment.

The decision is:

> Reserve/protect ₹5 lakh for the Education requirement.

The actual investment/product implementation is a separate downstream decision subject to the relevant product, risk, liquidity, tax, and regulatory rules.

Therefore:

**Asset Earmarking ≠ Product Selection.**

---

## 9. Real-Life Case G — Mapping Does Not Guarantee Feasibility

An asset can be mapped to a goal while the goal remains infeasible.

Example:

- Future Education requirement: ₹25 lakh
- Projected mapped assets: ₹8 lakh
- Remaining funding requirement: ₹17 lakh

Mapping only identifies the resource contribution.

It does not make the goal feasible.

The system must continue to evaluate:

- future contributions;
- funding gap;
- affordability;
- timeline;
- constraints;
- alternative feasible paths.

### Rule

> **Asset Mapping is evidence for feasibility; it is not feasibility itself.**

---

## 10. Real-Life Case H — Earmarking Can Be a Technique

Within the canonical decision hierarchy:

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

**Asset Earmarking** can operate as a Technique when the selected strategy/variant requires intentional designation or protection of resources.

Example:

```
Capital Preservation
   ↓
Protected-Core Preservation
   ↓
Asset Earmarking
   ↓
Define protected capital boundary
   ↓
Protected Education capital solution
   ↓
Execute required asset/resource changes
```

This does not turn Asset Mapping into a Technique.

---

## 11. Decision Ownership

| Decision | Canonical Owner |
|---|---|
| What assets/resources exist? | Financial State / Portfolio Data |
| Which assets are associated with a goal for planning? | Goal Planner / Goal Asset Mapping |
| What is the projected contribution of mapped resources? | Goal Planning / Asset Projection |
| What is the funding gap? | Goal Funding / Feasibility |
| Should resources be intentionally reserved/protected? | Strategy Decision / Selected Technique |
| How much should be earmarked? | Strategy / Method / Policy |
| What concrete implementation should be performed? | Architecture / Solution / Action |
| What investor action is finally accepted? | Investor Decision / Accepted Plan |

---

## 12. Canonical Decision Rules

### Rule 1
**Asset Mapping must happen before it is possible to correctly assess the contribution of existing resources to goal feasibility.**

### Rule 2
**Asset Earmarking must not be used merely as another name for Asset Mapping.**

### Rule 3
**Asset Mapping does not imply that an asset is permanently committed to a goal.**

### Rule 4
**Asset Earmarking is a deliberate strategic/implementation decision and must have an explicit reason.**

### Rule 5
**Cancelling a goal does not delete the underlying asset.**

### Rule 6
**A mapped asset may later be earmarked, partially earmarked, released, or reassigned.**

### Rule 7
**The same asset cannot be silently treated as fully earmarked for mutually competing goals.**

### Rule 8
**Earmarking does not itself select an investment product.**

### Rule 9
**Mapping contributes evidence to funding/feasibility analysis but does not guarantee feasibility.**

### Rule 10
**The system must preserve the distinction between planning association and strategic commitment.**

---

## 13. Canonical Relationship to the Decision Tree

Asset Mapping sits upstream:

```
Financial State
      ↓
Goal Context
      ↓
Asset Mapping
      ↓
Asset Projection
      ↓
Funding Gap
      ↓
Goal Feasibility
      ↓
Strategy Applicability
      ↓
Strategy Viability
      ↓
Strategy Selection
```

Asset Earmarking sits downstream when justified by the selected strategic path:

```
Strategy
   ↓
Variant
   ↓
Technique
   ↓
Asset Earmarking
   ↓
Method / Policy
   ↓
Architecture / Solution
   ↓
Action
```

This resolves the apparent overlap without collapsing the two functions.

---

## 14. Canonical User Journey

### User-facing journey

```
Investor adds/owns an asset
        ↓
Financial State records asset
        ↓
Investor creates/selects a goal
        ↓
Goal Planner asks which existing resources should be considered
        ↓
Asset Mapping
        ↓
Projected contribution shown
        ↓
Goal funding gap / feasibility shown
        ↓
Strategy Builder evaluates applicable strategies
        ↓
Selected Strategy + Variant
        ↓
Technique Selection
        ↓
If required: Asset Earmarking
        ↓
Method / Policy
        ↓
Solution
        ↓
Investor reviews decision
        ↓
Accept / Reject / Modify
        ↓
Accepted Plan
        ↓
Action Plan
        ↓
Execution
```

---

## 15. Final Canonical Statement

> **Asset Mapping tells the system what existing resources are being considered for a goal. Asset Earmarking tells the system what resources should intentionally be reserved or protected for that goal as part of an accepted strategic path.**

They are related, but they are **not duplicates, not aliases, and not the same decision**.

This document is the target business definition for future reconciliation against the current implementation. Existing current-state and audit documents remain unchanged.
