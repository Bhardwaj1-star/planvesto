# Concepts Outside Existing Feature Documents — Concept Register

**Document Type:** Cross-Feature Business Concept Register  
**Status:** Working analysis; business boundaries proposed, not an implementation audit  
**Scope:** Concepts evidenced by the Real-Life Decision Cases that do not fit cleanly within the current 10 feature documents  
**Purpose:** Identify uncovered or cross-feature business concepts before creating new feature specifications or changing code.

---

## 1. Why This Register Exists

The existing feature documents describe these product areas: Action Plan, Budgeting, Dashboard, Goal Planner, History, Investor Diary, Moneywheel, Profile, Reports Center and Strategy Builder.

The Real-Life Decision Cases describe broader decision and plan lifecycles that cross these feature boundaries. This register separates:

1. Potential standalone capability — may warrant a dedicated product capability or workspace.
2. Shared domain lifecycle/rule — should be defined once and used by multiple features; it does not automatically require a new UI feature.
3. Taxonomy or decision rule — a canonical business concept, not a user-facing feature by itself.
4. Existing feature responsibility — already has a natural owner and should not be duplicated as a new feature.

This is a business-document comparison. It does **not** establish whether any concept is absent from the code, database, API or UI.

## 2. Interpretation Rules

The current feature documents are treated as feature registers, not as proof that every described capability is implemented. “Not clearly owned” means the reviewed feature-document set does not define a clear primary owner and lifecycle boundary.

Do not infer that a concept is absent from code, that documentation proves implementation, or that a missing standalone document proves the capability does not exist. Do not create a screen, service, table or code module solely because a concept is listed here.

## 3. Concept Register

| ID | Canonical concept | Classification | Initial disposition |
|---|---|---|---|
| CFC-01 | Implementation Design Layer | Potential standalone/shared capability | Define boundary first |
| CFC-02 | Impact Analysis and Whole-Plan Simulation | Shared cross-feature capability | Separate from individual-goal strategy decisions |
| CFC-03 | What-If / Scenario Workspace | Potential workspace or sub-capability | Consider as part of Implementation Design |
| CFC-04 | Stress / Resilience Evaluation | Shared decision capability | Define inputs, tests, outputs and failure semantics |
| CFC-05 | Investor Decision and Accepted Plan Lifecycle | Shared domain lifecycle | Define authoritative states and transitions |
| CFC-06 | Investor-Designed Strategy Mode | Strategy Builder mode / exceptional path | Define controlled path when no standard strategy is acceptable |
| CFC-07 | Constraint and Safety Evaluation | Shared decision rule | Define canonical constraint contract |
| CFC-08 | Materiality Check and Targeted Revalidation | Shared change-management rule | Define when and what to revalidate |
| CFC-09 | Debt Economics and Financing Analysis | Shared analysis capability | Define ownership and reuse |
| CFC-10 | Technique Policy Registry | Canonical decision metadata | Maintain technique status separately |
| CFC-11 | Decision Hierarchy and Object Boundaries | Canonical taxonomy | Shared domain vocabulary, not a UI feature |
| CFC-12 | Asset Mapping vs Asset Earmarking | Cross-feature domain distinction | Preserve separate meanings and lifecycle stages |

Priority here means business-boundary clarification, not implementation order.

---

## 4. Candidate Capabilities

### CFC-01 — Implementation Design Layer

**Classification:** Potential standalone/shared capability  
**Primary source evidence:** Case 4, Better Path Strategy and Implementation; Case 7, New Goal Against Existing Plan; canonical Strategy Decision Tree.

**Business problem**

Selecting a strategy does not by itself determine a workable implementation. An investor may need to test concrete changes using actual financial values and compare projected consequences before deciding whether to adopt a path.

**Proposed responsibility**

- Translate a selected strategy and variant into concrete implementation alternatives.
- Model relevant changes such as resource use, asset liquidation, contributions, timing, liquidity, debt repayment or financing, and effects on other goals.
- Show assumptions, projected outcomes, constraints and trade-offs for each alternative.
- Return implementation candidates and their effects to the decision/adoption lifecycle.

**Boundary**

- Strategy Decision chooses and justifies the strategy/variant and identifies techniques.
- Implementation Design works out concrete alternatives using the chosen path and financial data.
- A technique is not itself the resulting solution.
- A proposed implementation is not an Accepted Plan until the investor explicitly adopts it through the relevant lifecycle.
- Action Plan represents execution work derived from an adopted plan; it is not a synonym for implementation design.

**Inputs to define:** selected strategy/variant, technique policy, current financial state, goal requirements, existing Accepted Plan where applicable, constraints, assumptions and relevant resource/debt data.

**Outputs to define:** comparable implementation alternatives, projected effects, feasibility/constraint results, assumptions, unresolved inputs and a recommendation for investor review.

**Open questions:** Is this a dedicated workspace, a shared capability used by Strategy Builder and Goal Planner, or both? Which calculations are authoritative versus illustrative? How are assumptions and alternatives versioned? Which changes require whole-plan impact analysis?

**Disposition:** Define the business contract before deciding whether this deserves a new top-level feature.

### CFC-02 — Impact Analysis and Whole-Plan Simulation

**Classification:** Shared cross-feature capability  
**Primary source evidence:** Cases 3, 7, 9, 10 and 11; canonical Strategy Decision Tree, Whole-Plan Impact Boundary.

**Business problem**

A change affecting one goal may have consequences for other goals, shared resources, cash flow, debt or an existing Accepted Plan. The system needs to distinguish local goal impact from material plan-level impact.

**Proposed responsibility**

- Assess direct impact on the affected goal.
- Determine whether the change materially affects other goals or the overall plan.
- Evaluate resource conflicts, priorities, funding trade-offs and plan-level consequences when needed.
- Identify which decisions require revalidation instead of rerunning every decision indiscriminately.
- Explain material effects and uncertainty.

**Boundary**

Whole-Plan Impact is **conditional**, not a mandatory stage in every individual-goal Strategy Decision. It applies when cross-goal dependencies, an existing Accepted Plan or a material plan-level change make it relevant.

Goal-level impact and whole-plan impact must be identifiable as different scopes. A local change must not silently be treated as a whole-plan change, and a material cross-goal change must not be ignored merely because it began in one feature.

**Trigger examples:** a new goal competes for existing resources; a surplus or contribution assumption changes materially; debt changes funding capacity for other goals; a scenario changes a resource relied on by an Accepted Plan; execution materially diverges from plan assumptions.

**Outputs to define:** affected goals and plan components, materiality decision, impact summary, assumptions, recommended revalidation targets, and whether investor review is needed.

**Open questions:** What constitutes material impact for each change type? Which thresholds are configurable versus hard constraints? How is uncertainty represented? Which capability owns the canonical result?

**Disposition:** Treat as a shared capability/domain contract, not necessarily a separate screen.

### CFC-03 — What-If / Scenario Workspace

**Classification:** Potential workspace or sub-capability  
**Primary source evidence:** Cases 7, 9, 10 and 11; Action Plan and Strategy Builder feature registers.

**Business problem**

Investors need to explore alternatives without unintentionally changing the active Accepted Plan.

**Proposed responsibility**

- Create an isolated scenario from a known baseline.
- Apply proposed changes and compare projected outcomes against that baseline.
- Allow a scenario to be revised, rejected or submitted for investor decision.
- Preserve the distinction between scenario state, recommendation state and adopted plan state.
- Send relevant changes to Impact Analysis and targeted revalidation.

**Boundary**

A scenario is exploratory/proposed state. It does not become the active Accepted Plan merely because it was calculated, displayed, saved or used to generate a report. Adoption must be an explicit lifecycle transition. Until adoption, the current Accepted Plan remains authoritative for active execution.

**Relationship to CFC-01:** Scenario exploration may be a workspace within the Implementation Design Layer rather than an independent feature. Settle the business contract before deciding navigation or architecture.

**Outputs to define:** scenario baseline, changed assumptions/values, projected results, comparison, validation status, decision status and adoption outcome.

**Open questions:** Are scenarios immutable snapshots, editable working copies, or both? What if the baseline Accepted Plan changes while a scenario is open? How are rejected/superseded scenarios retained? Can a scenario be adopted before required validations pass?

**Disposition:** Define lifecycle and isolation guarantees first; do not create a separate feature solely because What-If is a distinct term.

### CFC-04 — Stress / Resilience Evaluation

**Classification:** Shared decision capability  
**Primary source evidence:** Stage 12 of the canonical Strategy Decision Tree; cases involving changed financial state and plan revalidation.

**Business problem**

A path that works under one set of assumptions may fail when assumptions deteriorate. The canonical decision tree explicitly includes Stress / Resilience, but this comparison does not establish a complete business contract for that stage.

**Proposed responsibility**

- Test a proposed path against defined adverse or changed assumptions.
- Assess whether constraints, funding needs, repayment capacity, liquidity and goal timing remain acceptable.
- Identify the assumptions or conditions under which a path fails.
- Return a resilience result to inform the decision and investor explanation.

**Boundary**

Stress / Resilience tests robustness of a selected path. It is not interchangeable with strategy applicability, strategy viability, general impact analysis or a technique. The precise relationship and sequence between viability checks and stress testing must be specified in the canonical decision contract.

**Inputs and outputs to define:** scenarios/shocks, baseline assumptions, metrics, pass/fail/conditional results, severity, affected goals, limitations and rationale.

**Open questions:** Which stress cases are mandatory per strategy/variant? Which results are rejection gates versus warnings? How should missing inputs differ from a failed test? How are assumptions and results versioned?

**Disposition:** The canonical flow calls for this business capability; its UI and technical implementation remain unverified.

### CFC-05 — Investor Decision and Accepted Plan Lifecycle

**Classification:** Shared domain lifecycle  
**Primary source evidence:** Cases 4 and 7–12; canonical lifecycle at the end of the Strategy Decision Tree; Action Plan feature register.

**Business problem**

A system-generated recommendation, investor choice, Accepted Plan and Action Plan are different objects/states. Treating them as interchangeable can activate work that the investor has not accepted or overwrite an existing plan with an exploratory scenario.

**Proposed lifecycle**

1. A decision/recommendation is produced.
2. The investor reviews and accepts, rejects, defers or requests changes, as supported by the eventual policy.
3. An Accepted Plan is created or updated only after the required adoption transition.
4. An Action Plan is generated or reconciled from the adopted plan.
5. Execution changes or What-If exploration may trigger impact analysis and targeted revalidation.
6. A revised recommendation requires a new investor decision before the active Accepted Plan changes.

**Boundary**

- Recommendation is not investor acceptance.
- A saved scenario is not an Accepted Plan.
- An Accepted Plan is not the same as its Action Plan.
- Completed actions remain historical if the active plan later changes.
- A rejected or unaccepted path must not be presented as an adopted plan.
- “No acceptable strategy” must not be bypassed merely to generate an Action Plan.

**States and transitions to define:** recommendation status, investor decision status, accepted-plan version/status, active versus superseded plan, action-plan reconciliation status and audit/history requirements.

**Open questions:** Which transitions require explicit investor action? Can acceptance be partial or conditional? How are plan versions superseded or rolled back? What happens to in-progress actions when a plan changes? Which events must be retained for auditability?

**Disposition:** Define as a shared domain lifecycle. A new UI feature is not implied.

### CFC-06 — Investor-Designed Strategy Mode

**Classification:** Strategy Builder mode / exceptional decision path  
**Primary source evidence:** Case 12, No Acceptable Path and Investor-Designed Strategy.

**Business problem**

If no standard strategy satisfies the investor's constraints, the product should not force one. An investor may wish to propose a different path for evaluation.

**Proposed responsibility**

- Make “no acceptable standard strategy” explicit.
- Permit an investor-proposed path where product policy allows.
- Capture assumptions, resources, sequence and intended outcomes.
- Subject the proposal to relevant constraints, viability checks, impact analysis and stress/resilience evaluation.
- Keep the proposal unaccepted until explicit adoption through the Accepted Plan lifecycle.

**Boundary**

Investor-designed does not mean automatically safe, feasible, approved or exempt from validation. This mode must not disguise a failed standard strategy as a successful canonical strategy or change the canonical four-strategy set without a separate business decision.

**Outputs to define:** investor-proposed path, validation results, unresolved risks/constraints, comparison with standard paths where possible, and explicit accepted/rejected/deferred status.

**Open questions:** Which elements can investors configure freely? Which constraints are non-negotiable? Can a proposal be saved with incomplete inputs? What explanation is required when it fails?

**Disposition:** Prefer a controlled mode within Strategy Builder/Implementation Design unless product research demonstrates the need for a separate feature.

---

## 5. Shared Rules and Domain Contracts

### CFC-07 — Constraint and Safety Evaluation

**Classification:** Shared decision rule

The canonical Strategy Decision Tree places Constraint / Safety Evaluation before strategy applicability and viability. It defines the allowed or restricted decision space.

The contract should identify hard constraints versus preferences; blocking conditions versus warnings; constraints that apply globally versus to one goal or strategy; how a failed constraint affects candidate strategies; and how missing data is represented without being mistaken for a passed check.

This is not a synonym for viability. Constraints define what is permitted or restricted; viability evaluates whether an otherwise applicable candidate can work under relevant conditions.

**Primary source:** canonical Strategy Decision Tree, decision stages and strategy rejection rules.

### CFC-08 — Materiality Check and Targeted Revalidation

**Classification:** Shared change-management rule

A changed input does not automatically require every decision to be rerun. The system needs a materiality check and a dependency-aware revalidation policy.

The contract should define what changed and which decisions depend on it; whether the change is immaterial, locally material or plan-level material; which goal/strategy/variant/technique/solution outputs become stale; when whole-plan impact analysis is needed; which outputs remain valid; and how stale results are labelled until revalidation completes.

This connects Impact Analysis, What-If, Accepted Plan lifecycle and Action Plan reconciliation. It is not a new user-facing feature by default.

**Primary source:** Cases 5, 6, 9, 10 and 11.

### CFC-09 — Debt Economics and Financing Analysis

**Classification:** Shared analysis capability / domain rule

Debt-related decisions require more than the existence of debt or a funding gap. Relevant analysis can include effective debt cost, repayment burden, prepayment terms, EMI capacity, borrowing capacity, financing cost and a credible repayment path.

This analysis supports Debt Reduction and Credit Utilisation and may affect Goal Planner feasibility, Budgeting and plan-level impact. Ownership should be defined so features consume consistent outputs rather than independently inventing conflicting calculations.

This register does not prescribe a standalone debt feature. It records a shared calculation/decision responsibility whose technical owner is unverified.

**Primary source:** canonical Strategy Decision Tree, Debt Reduction and Credit Utilisation gates; relevant multi-goal and plan-change cases.

### CFC-10 — Technique Policy Registry

**Classification:** Canonical decision metadata

Technique selection needs explicit policy statuses:

| Status | Meaning |
|---|---|
| Required | The variant cannot be properly executed without it |
| Conditional | Used only when a defined condition exists |
| Optional | May improve implementation but is not necessary |
| Not Applicable | Should not be used in the situation |
| Insufficient Inputs | Relevant, but required information is unavailable |

**Not Applicable is not the same as Insufficient Inputs.**

The registry should define the mapping between strategy, variant, technique, condition, required inputs, method/policy and expected output. This is a canonical rules/data contract, not automatically a user-facing feature.

**Primary source:** canonical Strategy Decision Tree, Canonical Technique Set, Technique Policy and Strategy-to-Variant-to-Technique Rules.

### CFC-11 — Decision Hierarchy and Object Boundaries

**Classification:** Canonical taxonomy

The documented hierarchy is:

**Strategy → Variant → Technique → Method / Policy → Solution → Action**

The current runtime may use internal composition structures, but Architecture is not a separate required level in the target business flow. The investor-facing proposal is the Solution, built from the selected Strategy, Variant, Technique and Method/Policy. Do not create a separate Architecture decision stage unless a future business requirement proves it necessary.

- **Strategy:** broad approach to the financial problem.
- **Variant:** situation-specific form of a strategy.
- **Technique:** implementation approach selected under a policy.
- **Method / Policy:** operating logic or conditions for applying a technique.
- **Architecture:** structure of the concrete implementation; exact boundary needs canonical definition.
- **Solution:** the concrete proposed arrangement that results.
- **Action:** an executable step derived from an adopted plan.

A technique must not be relabelled as a solution simply because it contributes to the implementation outcome.

**Primary source:** canonical Strategy Decision Tree, Technique ≠ Solution, Decision Output Contract and Final Canonical Flow.

### CFC-12 — Asset Mapping vs Asset Earmarking

**Classification:** Cross-feature domain distinction

**Asset Mapping**
- Belongs upstream in Goal Planner / Goal Funding / Feasibility.
- Associates resources with goals for planning and analysis.
- Helps reveal funding coverage, conflicts and potential resource use.
- Does not itself mean a resource is committed, protected or sufficient to make a goal feasible.

**Asset Earmarking**
- Is a strategic/implementation choice to designate or reserve resources for a particular goal or protected capital pool.
- May follow feasibility and strategy decisions.
- Does not by itself constitute product selection, execution or proof that the goal is funded.

The two concepts must not be merged merely because both connect assets/resources with goals.

**Primary source:** canonical Asset Mapping vs Asset Earmarking decision case and Strategy Decision Tree.

---

## 6. Concepts Not to Promote to New Features by Default

These are important but are not automatically standalone product features:

- **Applicability vs Viability:** separate decision gates within Strategy Decision.
- **No Acceptable Strategy:** a valid decision outcome, not a new feature or system error.
- **Goal Funding:** belongs to Goal Planner / Goal Funding / Feasibility, not a fifth Strategy Builder strategy.
- **Contribution Escalation:** belongs to Goal Planner / Goal Funding.
- **Duration / Horizon Matching:** an analysis method, not a separate core technique.
- **Investor adoption:** a lifecycle transition, not proof that a recommendation was accepted just because it was displayed.
- **Whole-Plan Impact:** conditional plan-level analysis, not a mandatory gate in every individual-goal decision.
- **Tax-specific techniques:** do not force them into the canonical four-strategy tree; assign them to the appropriate investment/tax implementation layer unless a separate business decision changes that boundary.

---

## 7. Source-to-Concept Traceability

| Reference source | Concepts evidenced |
|---|---|
| strategy-decision-tree.md | CFC-01, CFC-02, CFC-04, CFC-05, CFC-07, CFC-09, CFC-10, CFC-11, CFC-12 |
| 03-CASE_3_MULTI_GOAL_FEASIBILITY_AND_ACTION_PLAN.md | CFC-02, CFC-08, CFC-09 |
| 04-CASE_4_BETTER_PATH_STRATEGY_AND_IMPLEMENTATION.md | CFC-01, CFC-05, CFC-06 |
| 05-CASE_5_PLAN_ADAPTATION_AFTER_FINANCIAL_STATE_CHANGE.md | CFC-02, CFC-08 |
| 06-CASE_6_GOAL_INTENT_CHANGE_AND_RECALCULATION.md | CFC-02, CFC-08 |
| 07-CASE_7_NEW_GOAL_AGAINST_EXISTING_PLAN.md | CFC-01, CFC-02, CFC-03, CFC-05 |
| 08-CASE_8_INVESTOR_STRATEGY_CHANGE_AND_MULTI_STRATEGY_PLAN.md | CFC-05, CFC-06 |
| 09-CASE_9_EXECUTION_PLAN_WHAT_IF_AND_IMPACT_GUIDANCE.md | CFC-02, CFC-03, CFC-05, CFC-08 |
| 10-CASE_10_EXECUTION_CHANGE_TRIGGERING_STRATEGY_REEVALUATION.md | CFC-02, CFC-03, CFC-05, CFC-08 |
| 11-CASE_11_ITERATIVE_STRATEGY_EXECUTION_AND_REVALIDATION.md | CFC-02, CFC-03, CFC-05, CFC-08 |
| 12-CASE_12_NO_ACCEPTABLE_PATH_AND_INVESTOR_DESIGNED_STRATEGY.md | CFC-05, CFC-06 |
| 15-CANONICAL_ASSET_MAPPING_VS_ASSET_EARMARKING_DECISION_CASE.md | CFC-12 |

Traceability records supporting source documents. Exact subsection-level line references can be added if a later audit requires them.

---

## 8. Recommended Definition Order

Before writing new feature specifications or implementing code, resolve the business boundaries in this order:

1. **CFC-05 — Investor Decision and Accepted Plan Lifecycle.** Establish authoritative states and adoption transitions.
2. **CFC-01 — Implementation Design Layer.** Establish the boundary between selected strategy, concrete alternatives, solution and Action Plan.
3. **CFC-02 — Impact Analysis and Whole-Plan Simulation.** Establish local versus plan-level impact and outputs.
4. **CFC-08 — Materiality Check and Targeted Revalidation.** Establish dependency and invalidation rules.
5. **CFC-03 — What-If / Scenario Workspace.** Define isolation, comparison and adoption using the above lifecycle.
6. **CFC-04 and CFC-07 — Stress / Resilience and Constraint / Safety.** Define checks, gates, failure results and missing-input behavior.
7. **CFC-06 — Investor-Designed Strategy Mode.** Define the exceptional path after “No Acceptable Strategy.”
8. **CFC-09 to CFC-12.** Finalize shared calculation ownership, technique policy metadata and canonical terminology.

This is a recommended business-definition order, not an implementation roadmap or claim about existing code.

---

## 9. Audit Status and Next Step

**Status: Not yet code-verified.**

A future audit must independently determine for every concept:
- whether it exists in code, UI, API, persistence and tests;
- whether it is implemented fully, partially, duplicated, obsolete or only documented;
- whether runtime behavior matches the canonical business contract;
- whether the concept has an authoritative owner and a single source of truth.

Do not delete, refactor or create technical modules solely on the basis of this register.

**Immediate next step:** review and approve the business boundaries for CFC-05, CFC-01 and CFC-02. Then decide whether each warrants a separate feature document, a shared domain specification, or an update to an existing feature document.
