# Action Plan Journey

**Document Type:** Feature User Journey  
**Status:** CANONICAL DESIGN  
**Position:** After Investor Decision / Accepted Plan and before real-world execution  
**Scope:** Accepted path → Action generation and review → Investor execution decisions → Progress and impact tracking → Adopted-change reconciliation

## 1. Position in the Product Lifecycle

```text
Onboarding
  → Financial State
  → Goal Planner / Goal Feasibility
  → Strategy Builder
  → Investor Decision / Adoption
  → Accepted Plan
  → Action Plan
  → Execution
```

Action Plan begins from the currently adopted path. A recommendation, proposed solution, or What-If scenario alone must not activate actions.

## 2. Main User Journey

```text
Current Accepted Plan + Relevant Financial Context
                      ↓
          Identify Required Actions
                      ↓
      Generate / Reconcile Action List
                      ↓
      Investor Reviews Action Details
                      ↓
       Investor Confirms / Changes
          Practical Execution Details
                      ↓
             Execute Actions
                      ↓
       Record Status and Progress
                      ↓
      Assess Planned vs Actual Impact
                      ↓
     Material Change or New Decision?
          ├─ No → Continue tracking
          └─ Yes → Impact Analysis
                    → Targeted Revalidation,
                      where required
                    → Investor Decision
                    → Accepted Plan changes?
                       ├─ No → Keep current plan/actions
                       └─ Yes → Reconcile future actions
                                 and preserve history
```

## 3. Stage-by-Stage Journey

### Stage 1 — Enter from the Accepted Plan

**Investor**
- Reaches Action Plan after adopting a financial path.
- Reviews the actions required to implement that path.

**System**
- Identifies the current Accepted Plan and its adopted decision/version.
- Uses relevant Financial State, goal-feasibility/funding context, constraints, accepted implementation details, current actions, and prior action history.
- Keeps unaccepted proposals and What-If scenarios separate from active actions.

**Output**
- A planning context tied to the currently adopted path.

### Stage 2 — Identify and prepare actions

**System**
- Determines the actions implied by the accepted financial path.
- Links each action to its relevant goal or plan and, where applicable, the selected strategy/implementation.
- May derive actions from goal-funding changes, debt repayment/restructuring, EMI or cash-flow changes, cross-goal resource allocation, or strategy implementation.
- Reconciles against existing active actions so repeated processing does not blindly duplicate actions.
- Does not invent an amount, deadline, priority, source, destination, order, or dependency when the accepted decision does not define it.

**Investor sees**
- Goal-linked actions and, where appropriate, plan-level actions.
- Each action's purpose and relationship to the Accepted Plan.
- Amount, timing, priority, order, dependencies, source/destination and expected impact where those details are supported.
- Action status and any unavailable details that need clarification.

### Stage 3 — Review and decide how to execute

**Investor**
- Reviews the proposed action details.
- Confirms practical execution or changes practical execution details where supported.
- Can decide not to proceed with an action or explore an alternative; an exploration is not automatically an adopted plan change.

**System**
- Records the investor's action decision and execution details supported by the product contract.
- Keeps the distinction between action-level execution decisions and a change to the overall Accepted Plan.
- Does not silently change the accepted strategy or goal-feasibility result.

**Output**
- Action decisions and execution parameters associated with the accepted path, subject to the product's supported status contract.

### Stage 4 — Execute and track progress

**Investor**
- Carries out actions and records progress or completion where the product supports it.

**System**
- Tracks action status and execution history.
- Preserves completed actions as historical records.
- Distinguishes action completion from achievement of the expected financial outcome.

**Investor sees**
- Current action status and progress.
- Planned impact and actual impact/variance only where evidence and calculation support them.

### Stage 5 — Assess execution and financial impact

**Trigger**
- An execution detail changes, actual results differ from expectations, or relevant Financial State / goal information changes.

**System**
- Assesses the impact on the relevant goal and financial position.
- Considers cash flow, liquidity, debt, funding feasibility, and other goals when relevant to the change.
- Revalidates affected goals/strategies only when the change is material and the dependency requires it.
- Uses Whole-Plan / Multi-Goal Impact when the decision is plan-level or there is a material cross-goal effect; it is not an automatic mandatory stage for every individual action.

**Investor sees**
- The expected consequences and affected decisions where the system can support that analysis.
- Alternatives as proposals, separate from the active plan.

### Stage 6 — Adopt or reject a revised path

**Investor**
- Reviews the impact and any alternatives.
- Decides whether to retain the current path or adopt a revised one.

**System**
- If the revised path is rejected or remains a What-If, keeps the current Accepted Plan and active Action Plan unchanged.
- If the revised path is explicitly adopted, updates the relevant Accepted Plan and reconciles the future actions.
- Adds actions required by the adopted change, revises or deactivates actions that no longer apply according to the supported lifecycle, preserves unaffected actions, and retains completed-action history.

**Output**
- An Action Plan aligned with the current Accepted Plan, with prior execution history preserved.

## 4. What Each Action Must Communicate

Where the accepted decision defines the information, an action should show:

- What needs to be done and why.
- Related goal and/or plan.
- Relationship to the Accepted Plan and selected implementation, where applicable.
- Amount and timing/deadline.
- Priority, order and dependencies.
- Source and destination, where applicable.
- Current status and recorded investor decision.
- Planned impact and actual impact/variance, where supported.
- Relevant revalidation trigger, where defined.

Missing details must not be fabricated. Exact mandatory fields depend on the action/data contract.

## 5. Action Sources and Scope

Action Plan is not limited to tasks generated by Strategy Builder. Actions can arise from an accepted path involving:

- Goal funding or Goal Feasibility-related changes.
- Debt repayment, prepayment, restructuring, or EMI/cash-flow changes.
- Accepted resource allocation across multiple goals.
- Selected strategy, variant, technique, method/policy, and implementation design.
- Investor-adopted execution changes that alter future required actions.

These are conditional sources, not automatic action templates. An action must be supported by the accepted path and its evidence.

## 6. Boundaries and Safety Rules

- **Goal Planner / Goal Feasibility** determines goal requirements, funding gaps, and feasible funding paths; Action Plan does not independently redo feasibility.
- **Strategy Builder** selects/designs a strategy and implementation; Action Plan does not select a strategy.
- **Investor Decision / Accepted Plan** determines which proposed path becomes active.
- **Action Plan** translates the adopted path into actions and tracks execution.
- A generated recommendation or What-If is not an instruction and must not overwrite active actions.
- Completing an action does not prove that the goal or expected financial outcome was achieved.
- Do not force an Action Plan for a path the investor has not adopted.
- Preserve completed-action history and avoid changing unrelated actions without a supported dependency.

## 7. Inputs and Outputs

**Inputs**
- Current Accepted Plan and adopted decision/version.
- Current authoritative Financial State.
- Relevant goals, Goal Feasibility/funding context and constraints.
- Accepted implementation details and execution parameters, where applicable.
- Existing active actions, action decisions and completed-action history.
- Baseline and planned-impact evidence, where required.

**Outputs**
- Goal-linked and, where appropriate, plan-level actions.
- Action details and their relationship to the Accepted Plan.
- Action decisions, status and execution progress.
- Planned impact and actual-impact/variance evidence, where supported.
- Reconciled future actions after an adopted plan change, with historical actions preserved.

## 8. Known Unresolved Details

The source documents do not yet freeze:
- The complete action-generation rules for every goal-funding, debt, cash-flow, multi-goal and strategy path.
- Exact mandatory fields, status labels and status transitions.
- Exact materiality thresholds and targeted-revalidation triggers.
- The full investor-acceptance state contract for every path.
- The exact rule for revising, deactivating or replacing old active actions after an adopted change.
- The complete reminder, due-date and dependency behavior.

These remain unresolved; this journey does not claim that they are implemented or settled.
