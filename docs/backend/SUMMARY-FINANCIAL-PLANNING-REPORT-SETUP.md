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

## 15. Client-Facing Report Architecture

The current Summary Report contract is an **internal aggregation contract**. It must not be passed directly to the PDF renderer.

The required architecture is:

```
Financial Data
     ↓
MoneyWheel / Risk Profiler / Goal Engine / Investment Engine
     ↓
Summary Financial Report Service
     ↓
SummaryReport
     ↓
Client Report Interpretation Layer
     ↓
ClientReport
     ↓
PDF Renderer
     ↓
Investor-facing Summary Financial Planning Report
```

### 15.1 SummaryReport vs ClientReport

**SummaryReport** is an internal, structured aggregation of authoritative engine outputs.

**ClientReport** is the investor-facing, presentation-ready interpretation of that data.

The two contracts must remain separate.

The ClientReport layer may:

- select relevant facts;
- group related facts;
- convert technical outputs into plain-language explanations;
- generate section narratives from authoritative facts/rules;
- prioritize observations and actions;
- determine whether a technical metric is decision-useful;
- preserve provenance and source ownership;
- omit irrelevant internal fields.

The ClientReport layer must not:

- recalculate financial metrics;
- create new financial rules;
- invent thresholds;
- invent recommendations;
- change authoritative engine outputs;
- expose raw internal engine objects by default;
- expose internal scores/metadata merely because they exist in the source model.

### 15.2 Required ClientReport Sections

The client-facing report must support the following narrative structure:

1. **Where You Stand**
   - personalized current financial position;
   - material financial facts;
   - relevant derived metrics only when decision-useful;
   - concise investor takeaway.

2. **Where You Want to Go**
   - goals;
   - target amount;
   - timeline;
   - current funding;
   - funding gap / required contribution;
   - feasibility/context;
   - goal-specific takeaway.

3. **What Stands Between You and Your Goals**
   - the conditions materially affecting progress;
   - goal relevance;
   - impact;
   - urgency;
   - feasibility;
   - cross-engine context where available.

4. **What Needs to Change**
   - condition;
   - impact on the relevant goal/decision;
   - required change;
   - supporting evidence/source.

5. **Goal Funding**
   - current funding;
   - required funding/contribution;
   - funding gap;
   - relevant assumptions/requirements;
   - feasibility context.

6. **Investment Position**
   - portfolio-level allocation;
   - sub-asset allocation when available and useful;
   - goal-specific allocation/sleeves only when materially useful;
   - explanation of the allocation's role in the financial path.

7. **Your Financial Context**
   - current situation;
   - goals;
   - required return where relevant;
   - investment position;
   - concise explanation of how these pieces interact.

8. **Decision Points**
   - decisions the investor needs to understand or make;
   - decision context;
   - relevant dependency or constraint.

9. **Key Observations**
   - cross-engine;
   - decision-relevant;
   - prioritized;
   - non-redundant;
   - evidence-backed.

10. **Prioritized Actions**
    - action;
    - reason;
    - affected goal/decision;
    - priority;
    - authoritative source;
    - no unsupported implementation advice.

11. **Your Financial Path**
    - concise synthesis of the current position;
    - destination;
    - major constraints;
    - funding/investment path;
    - immediate priorities.

### 15.3 Narrative Generation Rules

The ClientReport must be generated from structured facts, not hardcoded investor-specific text.

Narratives should follow:

**Fact → Context → Impact → Required Change → Decision/Action**

The system must be able to produce different narratives for different investors from the same report contract.

Investor names, values, goals, gaps, timelines, allocation, observations, and actions must all be populated dynamically from the authenticated planning state and authoritative engine outputs.

No Rahul-specific values, names, wording, thresholds, or conclusions may be embedded in production code.

### 15.4 Dynamic Section Selection

The report is not required to display every possible field.

For each section, the interpretation layer should decide:

- whether the section is applicable;
- which facts are materially relevant;
- which technical metrics add decision value;
- what should be emphasized;
- what can be omitted.

A section may be reduced or marked incomplete when authoritative data is unavailable.

The renderer must not make business decisions about relevance. Relevance and narrative selection belong to the ClientReport interpretation layer.

### 15.5 Provenance

Every material observation, action, and interpreted condition should preserve its authoritative source where practical.

Examples:

- MoneyWheel;
- Risk Profiler;
- Goal Engine;
- Investment Engine.

Provenance is for system traceability and auditability. Internal source names, scores, rule IDs, and implementation metadata should not automatically appear in the investor-facing PDF.

### 15.6 No Raw Engine Dump

The PDF renderer must not use generic serialization such as:

- dumping a complete engine result dictionary/object;
- printing raw ratio objects;
- printing internal source/relevance/priority metadata as client content;
- printing a generic risk-profile object;
- printing arbitrary Investment Engine key/value pairs.

The renderer should receive ClientReport content that is already selected, interpreted, and presentation-ready.

### 15.7 ClientReport Contract Requirements

The ClientReport model should support, at minimum:

- report metadata;
- investor identity/display information;
- report date/version where available;
- executive/current-position narrative;
- dynamic financial snapshot;
- goal summaries;
- goal funding narratives;
- financial conditions;
- required changes;
- investment position;
- investor context;
- decision points;
- key observations;
- prioritized actions;
- financial path/conclusion;
- missing-data notices;
- provenance/audit metadata.

The contract should distinguish:

- **fact** — authoritative value/output;
- **interpretation** — explanation of what the fact means in context;
- **decision point** — decision arising from the current state;
- **action** — supported next step;
- **missing data** — unavailable input that limits assessment.

### 15.8 Renderer Responsibility

The PDF renderer is a presentation component only.

It should:

- receive ClientReport;
- render the defined sections;
- format numbers, dates, tables, and narratives;
- handle pagination;
- handle missing/partial sections gracefully;
- produce a professional investor-facing PDF.

It should not:

- call financial engines;
- calculate ratios;
- infer feasibility;
- create observations/actions;
- decide priorities;
- translate raw engine structures;
- contain investor-specific business logic.

## 16. Technical Components

Planned backend components:

- Summary Financial Report Service
- Summary Report Model / schema
- Summary PDF Renderer
- Summary Report API endpoints
- Automated tests

Existing PDF/download infrastructure may be reused where appropriate, but the summary report must have its own clear contract.

## 17. Proposed API Surface

### JSON

`GET /api/financial-planning/summary?planning_unit_id={id}`

Returns the structured Summary Financial Planning Report.

### PDF

`GET /api/financial-planning/summary.pdf?planning_unit_id={id}`

Returns the downloadable PDF.

Exact route naming can be finalized during implementation.

## 18. Definition of Done

The Summary Financial Planning Report is ready when:

1. The four authoritative engines provide the required inputs.
2. A stable internal SummaryReport contract exists.
3. The report service consumes those four outputs without duplicating engine calculations.
4. A separate ClientReport interpretation contract exists.
5. SummaryReport is transformed into ClientReport before PDF rendering.
6. ClientReport contains the required investor-facing sections.
7. Investor-specific content is generated dynamically from the planning state; no Rahul/example data is hardcoded.
8. No report-layer financial calculations duplicate engine logic.
9. No unsupported financial rules, thresholds, recommendations, or business meaning are invented by the interpretation layer.
10. Raw engine objects are not dumped into the client-facing PDF.
11. Observations and actions preserve authoritative provenance.
12. Missing/partial data is represented explicitly and does not cause fabricated content.
13. Technical metrics are shown only when decision-useful and in context.
14. JSON report generation works.
15. PDF generation works from ClientReport.
16. PDF download works through an authenticated API.
17. Renderer tests verify section rendering, pagination, formatting, and partial-data handling.
18. Interpretation tests verify normal, partial-data, missing-data, and unsupported-rule scenarios.
19. The same architecture can generate materially different reports for different investors from their actual planning state.
20. Multi-Goal Orchestration and Strategy Builder are not required for this report.
