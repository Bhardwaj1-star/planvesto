# Strategy Builder Journey

**Document Type:** User Journey  
**Status:** CANONICAL DESIGN  
**Scope:** Goal Feasibility Handoff → Strategy Decision → Implementation Design → What-If / Stress → Recommendation → Investor Adoption

---

## 1. Main Journey

```
Reviewed Goal Feasibility + Financial State + Goal Context + Constraints
                              ↓
                    Constraint / Safety Check
                              ↓
                    Strategy Applicability
                              ↓
                       Candidate Viability
                              ↓
                       Strategy Selection
                              ↓
                       Variant Selection
                              ↓
                       Technique Selection
                              ↓
                       Method / Policy
                              ↓
                 Architecture + Solution Proposal
                              ↓
                  What-If / Scenario Comparison
                              ↓
                     Stress / Resilience
                              ↓
                  Decision & Recommendation
                              ↓
                 Investor Review / Decision
                    ┌─────────┼─────────┐
                    ↓         ↓         ↓
                  Accept    Modify     Reject
                    ↓         ↓         ↓
              Accepted Plan  Recheck   Existing Accepted
                    ↓       affected   Plan remains
                Action Plan  stages
                    ↓         ↓
                Execution  New Recommendation
```

This is the target journey. It does not claim that every step is already implemented in the current product.

---

## 2. Entry Point — Goal Planner Handoff

Strategy Builder starts after Goal Planner has supplied the relevant goal-feasibility and funding evidence.

```
Defined Goal + Financial State
          + Goal Feasibility / Funding Evidence
          + Relevant Constraints
                    ↓
             Strategy Builder
```

- Goal Planner owns goal requirements, funding mechanisms, funding calculations and goal-feasibility assessment.
- Strategy Builder uses that evidence to decide how the financial situation may be addressed through a strategy.
- Strategy Builder must not silently repeat or redefine Goal Planner's feasibility decision.
- If required evidence is missing, keep that uncertainty visible; do not invent financial inputs.

The detailed feasibility journey remains in `04-GOAL_FEASIBILITY_JOURNEY.md`.

---

## 3. Constraint and Strategy Decision

### System flow

```
Applicable Constraints / Safety Conditions
                    ↓
             Strategy Applicability
                    ↓
               Candidate Viability
                    ↓
              Strategy Selection
```

- Check the constraints and safety conditions relevant to the case.
- **Applicability:** does this strategy fit the situation?
- **Viability:** can it work under the actual financial conditions?
- Select only from candidates that pass the relevant checks.
- Distinguish a hard constraint from an advisory priority, a warning, a failed check and missing evidence.
- Do not invent numerical thresholds, score weights or tie-break rules that are not defined in the governing sources.

### Four canonical Strategy Builder strategies

1. Progressive De-risking
2. Capital Preservation
3. Debt Reduction
4. Credit Utilisation

**Goal Funding is not a fifth Strategy Builder strategy.** Goal Funding and its funding mechanisms remain in Goal Planner / Goal Feasibility.

### Valid decision outcomes

- An acceptable strategy is identified.
- No acceptable strategy/path qualifies under the current evidence and constraints.
- More evidence is needed before a reliable decision can be made.

The system must not force a strategy merely to produce an answer.

---

## 4. Variant, Technique and Implementation Design

After a strategy is selected:

```
Selected Strategy
       ↓
     Variant
       ↓
    Technique
       ↓
  Method / Policy
       ↓
Architecture Composition
       ↓
Concrete Solution Proposal
       ↓
Investor Review
```

- A **Strategy** is the high-level financial approach.
- A **Variant** is a structural form of that strategy.
- A **Technique** is a reusable mechanism selected because the Strategy + Variant calls for it.
- A **Method / Policy** defines how a technique is applied in the context.
- **Architecture** composes the selected elements and their dependencies.
- A **Solution** is the concrete implementation proposal for this investor; it must not merely rename a Variant or Technique.
- An **Action** is a concrete step derived from an accepted implementation. A proposal is not itself an Action Plan.

### Investor sees

- What the proposed approach would involve.
- Relevant resources, timing, cash flow, debt, liquidity and dependencies where evidence is available.
- Important assumptions, constraints and trade-offs.
- The practical changes required by the proposed implementation.

The system proposes and explains the design. It does not silently execute changes or make the proposal an accepted plan.

---

## 5. What-If / Scenario Journey

```
Current Baseline / Proposed Solution
                 ↓
          Investor asks “What if?”
                 ↓
       Change an input or assumption
                 ↓
         Recalculate affected results
                 ↓
          Compare with baseline
                 ↓
           Investor reviews
             ┌───┴───┐
             ↓       ↓
          Keep      Consider
          current   revised path
```

Possible changes documented for this journey include:
- Goal date.
- Contribution amount.
- Asset mapping.
- Strategy or implementation choice.
- Execution action.

The comparison shows the current and scenario positions, material differences and relevant trade-offs where supported by data.

A scenario, saved comparison or historical run is **not** an accepted plan. The active Accepted Plan must remain separate until the investor explicitly adopts a revised path.

---

## 6. Stress / Resilience

```
Proposed Solution
       ↓
Relevant Stress / Resilience Tests
       ↓
Identify Pressure Points
       ↓
Show Impact and Limitations
       ↓
Investor reviews acceptability
```

The system may show relevant effects on:
- Goal funding.
- Affordability and cash flow.
- Liquidity and debt/EMI obligations.
- Goal timing or other affected goals, where relevant evidence exists.

Stress / resilience tests the proposed path under defined adverse or changed assumptions. It is distinct from strategy applicability, viability and ordinary scenario comparison.

- Show material weaknesses and assumptions.
- Do not present stress results as guaranteed forecasts.
- Do not silently change the investor's plan because a stress test shows pressure.
- Exact stress cases and thresholds must come from governing rules; do not invent them.

---

## 7. Decision and Recommendation

```
Goal / Financial Evidence
          +
Strategy + Implementation Proposal
          +
What-If / Stress Findings
          ↓
     Decision Synthesis
          ↓
       Recommendation
          ↓
     Investor Review
```

The investor is shown, where supported:
- Recommended path and why it fits.
- Relevant constraints and assumptions.
- Main trade-offs and pressure points.
- Alternatives, when relevant.
- Why no acceptable path was found, if that is the result.

Recommendation is decision support. It does not itself select a new active plan or imply investor acceptance.

---

## 8. Investor Decision and Adoption

```
Recommendation
      ↓
Investor chooses
  ┌───┼────┐
  ↓   ↓    ↓
Accept Modify Reject
  ↓   ↓    ↓
Accepted  Revisit  Existing Accepted
Plan     affected  Plan remains
         stages
```

### Accept
- The investor explicitly adopts the proposed path.
- The adopted path becomes the Accepted Plan.
- Relevant actions can then be represented in the Action Plan and move into execution.

### Modify
- Return to the affected planning, strategy, implementation or scenario stage.
- Recalculate the affected outputs.
- Produce a new recommendation for investor review.
- Do not treat the modified proposal as accepted before the investor decides.

### Reject
- Do not replace the current Accepted Plan with the rejected proposal.
- If no acceptable proposal remains, preserve that outcome; do not manufacture a recommendation.

---

## 9. Investor-Designed Path

If the investor wants to propose their own approach:
- Keep it separate from the four canonical Strategy Builder strategies unless the source rules explicitly classify it otherwise.
- Evaluate it against applicable constraints, feasibility/funding evidence, relevant impacts and resilience.
- Explain numerical consequences and trade-offs where evidence supports them.
- Investor-designed does not automatically mean viable, safe or accepted.
- It becomes the active path only after the investor explicitly adopts it.

---

## 10. Whole-Plan Impact and Revalidation

Whole-Plan / Multi-Goal Impact is conditional, not a mandatory step for every isolated goal decision.

Use the separate whole-plan journey when a new goal or material decision affects multiple goals, shared resources, competing priorities or the existing plan. Show the effects on affected goals and resource trade-offs where evidence is available.

When a material change occurs after adoption:

```
Accepted Plan + Material Change
              ↓
         Impact Analysis
              ↓
     Identify Affected Areas
              ↓
       Targeted Revalidation
          ┌───┴───┐
          ↓       ↓
       Still     No longer
       valid     valid
          ↓       ↓
      Continue   Revisit affected
                 planning / strategy
                      ↓
               New Recommendation
                      ↓
               Investor Adoption
```

Revalidate affected parts of the plan; do not rebuild unrelated parts without cause. The separate documents `14-REVALIDATION_JOURNEY.md` and `19-MULTI_GOAL_WHOLE_PLAN_JOURNEY.md` remain the shared journeys for these cross-cutting situations.

---

## 11. Strategy Builder Journey Outputs

| Stage | Output |
|---|---|
| Entry / evidence check | Goal context, financial state, feasibility evidence and missing inputs |
| Constraint / safety check | Relevant restrictions, warnings, failed checks or unknowns |
| Strategy decision | Selected strategy or No Acceptable Strategy / Path |
| Variant and technique design | Selected structural form and relevant mechanisms |
| Implementation design | Architecture and investor-specific Solution proposal |
| What-If | Baseline comparison and scenario differences |
| Stress / resilience | Pressure points, effects and assumptions |
| Recommendation | Explained proposed path, trade-offs and alternatives where relevant |
| Investor decision | Accept / Modify / Reject |
| Adoption | Accepted Plan only after explicit investor decision |
| Action / execution | Actions derived from the accepted implementation |

These are target journey outputs; this table is not a claim that every output is already available in runtime.

---

## 12. User Journey Boundaries

- **Goal Planner / Goal Feasibility:** owns goal funding and feasibility; supplies evidence to Strategy Builder.
- **Strategy Builder:** owns the strategy decision and the strategy-side implementation proposal.
- **What-If:** compares a changed scenario with a baseline; does not itself adopt it.
- **Stress / Resilience:** evaluates the proposed path under defined adverse assumptions; does not silently alter the plan.
- **Decision / Recommendation:** explains the proposed path; it is not investor adoption.
- **Investor Adoption:** records the explicit Accept / Modify / Reject decision.
- **Accepted Plan:** represents the adopted path.
- **Action Plan / Execution:** follow adoption; they are not interchangeable with a strategy or recommendation.
- **Revalidation / Whole-Plan Impact:** are conditional shared journeys for material changes and cross-goal effects.

---

## 13. Core Rules

1. Use the reviewed Goal Planner feasibility/funding evidence; do not repeat its calculation inside Strategy Builder.
2. Keep exactly four canonical strategies: Progressive De-risking, Capital Preservation, Debt Reduction and Credit Utilisation.
3. Do not treat Goal Funding, SIP, lump sum or contribution escalation as a fifth Strategy Builder strategy.
4. Distinguish strategy applicability from candidate viability.
5. Do not invent thresholds, score weights, tie-break rules or unsupported financial facts.
6. No Acceptable Strategy / Path and Insufficient Inputs are valid outcomes when supported by the evidence.
7. Keep Strategy, Variant, Technique, Method / Policy, Architecture, Solution and Action distinct.
8. Keep scenarios, recommendations and historical runs separate from the active Accepted Plan.
9. Investor acceptance must be explicit; the system must not silently change the plan or execute a proposal.
10. Apply Whole-Plan Impact and Revalidation when relevant; do not treat them as mandatory gates for every isolated decision.
11. This document describes the target user journey, not proof that each step is already implemented in code.
