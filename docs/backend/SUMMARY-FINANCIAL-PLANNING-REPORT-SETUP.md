# Summary Financial Planning Report — Setup & Business Rules

## 1. Purpose

Define the setup, boundaries, and locked business rules for the **Summary Financial Planning Report**.

This document is the business/architecture contract for the report. It does not implement the report.

The report is an investor-facing translation layer. Its purpose is not to display calculations, ratios, formulas, or engine internals for their own sake. Its purpose is to help the investor understand:

- where they are now;
- where they want to go;
- what stands between their current position and those goals;
- what financial conditions need to improve;
- how goal funding needs to work;
- how investment allocation supports the path;
- what decisions/actions matter next.

## 2. Report Role

The report combines three jobs:

1. **Financial Health / Situation Summary** — explain the investor's current financial condition.
2. **Financial Planning Summary** — connect the current position to goals and investment position.
3. **Decision Summary** — translate the situation into relevant decisions and prioritized actions.

Core narrative:

**Current Situation → Goals → Gap & Feasibility → Financial Conditions to Improve → Goal Funding → Investment Allocation → Investor Context → Decision Points → Prioritized Actions**

The report is not a technical calculation report.

## 3. Authoritative Inputs

The report consumes outputs from exactly these four planning components:

1. **MoneyWheel**
   - Current financial situation and financial diagnosis.
2. **Risk Profiler**
   - Risk-related inputs/constraints used by downstream planning; Risk Profile is not a standalone investor-facing report section.
3. **Goal Engine**
   - Goal targets, timelines, funding position, gaps, required contributions, and feasibility-related outputs.
4. **Investment Engine**
   - Asset allocation and sub-asset allocation / investment-position outputs.

### Explicitly out of scope

The Summary Report does not depend on:

- Strategy Builder
- Strategy Engine
- Multi-Goal Orchestration
- Product Selection Engine
- Insurance Suitability Engine

**Strategy is not part of this report.**

## 4. Risk Architecture in the Report

Risk concepts must not be presented as a generic standalone **Risk Profile** section.

### Risk Required

Risk Required is fundamentally a goal requirement:

- it represents the return/risk mathematically required to accumulate/fund the goal;
- it should appear where relevant to goal feasibility and investment context;
- it is not presented as a separate risk-profile score.

### Risk Capacity

Risk Capacity is used as a **constraint/input** for planning and investment decisions.

The report should use its relevant constraints to explain how the investor's financial condition can limit or shape decisions. It should not turn Risk Capacity into a standalone score/profile display.

### Risk Tolerance

Risk Tolerance belongs to the **Behavioral Profile** and is relevant primarily to later implementation/product-selection decisions.

It is not a standalone section of this summary report.

### Risk Profile

There is therefore **no standalone Risk Profile section** in the Summary Financial Planning Report.

## 5. Investor-Facing Philosophy

The report must not force the investor to understand financial-planning jargon.

Internal concepts such as:

- ratios;
- formulas;
- calculation outputs;
- thresholds;
- risk dimensions;
- derived facts;

are primarily system inputs.

The investor-facing report should translate them into:

**Condition → Impact → Required Change → Decision/Action**

Technical metrics may be shown dynamically only when they materially help the investor understand a specific decision.

## 6. Report Structure

### A. Where You Stand

Start with a concise plain-language understanding of the investor's current financial position.

The Financial Snapshot is dynamic:

- do not show a fixed set of fields for every investor;
- show information that is financially material to the investor's planning state;
- include core financial position data and relevant derived metrics when they help explain the situation.

### B. Where You Want to Go

Show the investor's goals as destinations:

- goal;
- target;
- timeline;
- current funding position;
- funding gap / required contribution;
- feasibility/context.

The goal section must explain not only the destination but also the investor's current position relative to it.

### C. What Stands Between You and the Goal

Explain the conditions that materially affect progress toward the goals.

Prioritization must be **context-dependent**, considering factors such as:

- impact;
- urgency;
- feasibility;
- goal relevance.

Do not rank a problem simply because its numerical gap is largest.

### D. What Needs to Change

Financial conditions are interpreted only in relation to a goal, constraint, or decision.

No ratio/metric is inherently labelled "good" or "bad."

The report should follow:

**Condition → Impact → Required Change**

For example, the report may explain that a financial condition is affecting a goal and therefore needs improvement, without treating the underlying ratio as a universal score.

### E. Goal Funding

Show what funding is required to move from the current position toward the goal.

The report should connect:

- current funding;
- funding gap;
- required contribution/funding requirement;
- feasibility;
- relevant financial conditions.

### F. Investment Position

Investment Engine outputs should be presented as part of the investor's financial path.

The report may include:

- asset allocation;
- sub-asset allocation;
- goal-related allocation/sleeves where context requires them.

The default architecture is **context-dependent hybrid**:

- portfolio-level allocation is primary;
- goal-specific allocation/sleeves may be shown when goal horizon, funding requirement, liquidity needs, or other relevant constraints make them materially useful.

Allocation should be explained in **decision-context language**, not merely as percentages.

The investor should understand the role the allocation plays in supporting the financial plan.

### G. Investor Context

After investment allocation, the report should provide context by connecting:

- current financial situation;
- goals;
- required return where relevant;
- investment allocation.

The purpose is to explain what the allocation means for this particular investor, rather than teaching generic investment theory.

### H. Decision Points

After providing context, identify the important decisions that arise from the investor's situation and plan.

### I. Key Observations

Key Observations are only for **cross-engine, decision-relevant insights**.

They should:

- combine information from multiple authoritative outputs where appropriate;
- be prioritized by relevance;
- avoid repeating a single engine's raw output;
- never invent conclusions unsupported by engine outputs/rules.

### J. Key Actions

Key Actions are:

- prioritized;
- decision-oriented;
- derived from the available authoritative outputs.

The report should present:

**Investor Context → Decision Points → Prioritized Actions**

## 7. Interpretation Rules

### Goal-driven interpretation

A metric or ratio has no standalone "good/bad" meaning in this report.

It becomes relevant when it materially affects:

- a goal;
- a financial constraint;
- a planning decision;
- an investment decision.

### Authoritative decision logic

The report must not invent new financial rules.

When a condition leads to a required change or action, that conclusion must be supported by the relevant engine output, canonical financial fact, or established business rule.

### Layer-dependent responsibility

The report must preserve the responsibility of each planning layer:

- **Financial condition:** identify what needs to change.
- **Goal funding:** identify the funding requirement.
- **Investment Engine:** determine how investment allocation supports the plan.
- **Product/implementation:** belongs to a separate later layer and is not implemented by this report.

The report can be guided and specific where calculations/rules justify specificity, but it must not invent implementation recommendations.

## 8. Language & Technical Detail

The report is primarily investor-facing and plain-language.

Technical terms are **dynamic**:

- hide them when they add no decision value;
- show them when they materially help explain a decision;
- when shown, place them in context rather than presenting them as isolated scores.

The report should explain the investor's condition, not expose the internal calculation machinery.

## 9. Missing / Insufficient Data

Missing data must never be invented.

The report should:

1. continue using available information;
2. clearly identify incomplete/unavailable assessments;
3. explain, where material, what missing information prevents the system from assessing or deciding.

Partial reports are valid outputs.

## 10. Report Presentation

The report should use:

**Narrative + structured sections + personalized prioritization.**

It should not be a generic dashboard.

The information order should adapt to the investor's situation so that the most relevant information appears first and less relevant information is secondary.

The opening should establish:

**Where You Stand → Where You Want to Go → What Stands Between You and the Goal**

The conclusion should establish:

**Your Financial Path → Prioritized Decisions / Actions**

## 11. High-Level Data Flow

```
Financial Data
     ↓
MoneyWheel
Risk Profiler
Goal Engine
Investment Engine
     ↓
Summary Financial Report Service
     ↓
Summary Report Model
     ↓
PDF Renderer
     ↓
Downloadable Summary Financial Planning Report
```

The report layer must consume authoritative engine outputs. It must not independently recreate financial calculations.

## 12. Architecture Rules

1. No financial calculation is duplicated inside the report layer.
2. MoneyWheel remains responsible for financial-situation diagnosis.
3. Risk-related financial constraints are consumed from the authoritative risk architecture; the report does not create a separate Risk Profile presentation.
4. Goal Engine remains responsible for goal calculations.
5. Investment Engine remains responsible for allocation outputs.
6. Strategy Builder / Strategy Engine are outside this report.
7. The report is an aggregation, interpretation, and presentation layer, not a replacement decision engine.
8. Missing or unavailable data must be explicit.
9. No values, rules, recommendations, or business meaning may be invented by the report layer.
10. Important outputs should preserve provenance where practical.
11. Report generation should be deterministic for the same planning state and engine outputs.
12. Detailed-report requirements remain separate.

## 13. Business Rules — Locked

The following decisions are locked:

- Report purpose = financial situation + planning position + decision/action summary.
- Financial Snapshot = dynamic, personalized information rather than a fixed field list.
- Financial Situation = objective diagnosis + financial story.
- Goals = target + timeline + funding position + gap/required funding + feasibility/context.
- Financial conditions are interpreted only in relation to goals, constraints, or decisions.
- No metric/ratio is inherently good or bad.
- Interpretation pattern = Condition → Impact → Required Change.
- Actions/conclusions must be supported by authoritative engine/rule outputs.
- No standalone Risk Profile section.
- Risk Required = goal requirement.
- Risk Capacity = planning/investment constraint.
- Risk Tolerance = Behavioral Profile / later product-selection context.
- Investment allocation = context-dependent hybrid: portfolio-level by default, goal-specific sleeves where materially required.
- Investment explanation = decision context, not technical percentage display alone.
- Investor Context = current situation + goals + required return where relevant + investment allocation.
- Key Observations = cross-engine, decision-relevant, prioritized insights.
- Key Actions = prioritized decisions/actions.
- Prioritization = context-dependent using impact, urgency, feasibility, and goal relevance.
- Technical metrics/jargon = dynamic and shown only when decision-useful.
- Missing data = explicit; partial report continues where possible.
- Report structure = narrative + structured sections + personalized prioritization.
- Opening = Where You Stand → Where You Want to Go → What Stands Between You and the Goal.
- Conclusion = Financial Path → Prioritized Decisions/Actions.
- Strategy Builder / Strategy Engine = excluded.

## 14. Remaining Rules to Decide

The following are still intentionally open and should be decided one at a time:

- Exact MoneyWheel outputs that qualify as decision-useful evidence.
- Exact cross-engine observation rules.
- Exact goal-feasibility presentation rules.
- Exact Investment Engine outputs/fields to consume.
- Exact prioritization algorithm for observations/actions.
- Data-quality/confidence presentation.
- Status labels.
- Exact PDF presentation rules.
- Exact API/report contract details.

## 15. Technical Components

Planned backend components:

- Summary Financial Report Service
- Summary Report Model / schema
- Summary PDF Renderer
- Summary Report API endpoints
- Automated tests

Existing PDF/download infrastructure may be reused where appropriate, but the summary report must have its own clear contract.

## 16. Proposed API Surface

### JSON

`GET /api/financial-planning/summary?planning_unit_id={id}`

Returns the structured Summary Financial Planning Report.

### PDF

`GET /api/financial-planning/summary.pdf?planning_unit_id={id}`

Returns the downloadable PDF.

Exact route naming can be finalized during implementation.

## 17. Definition of Done

The Summary Financial Planning Report is ready when:

1. The four authoritative engines provide the required inputs.
2. A stable summary report contract exists.
3. The report service consumes those four outputs.
4. No report-layer financial calculations duplicate engine logic.
5. Investor-facing interpretation follows the locked business rules.
6. JSON report generation works.
7. PDF generation works.
8. PDF download works through an authenticated API.
9. Tests cover normal, partial-data, missing-data, and failure scenarios.
10. Multi-Goal Orchestration and Strategy Builder are not required for this report.
