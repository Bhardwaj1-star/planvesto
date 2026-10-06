# Strategy Variants Architecture

## Purpose

This document defines the Strategy Variant layer for Planvesto.

A Variant is an implementation/funding architecture inside a Strategy. It is not a technique, component, or product solution.

### Architecture hierarchy

**Strategy → Variant → Report Architecture → Scenario → Actions**

- **Strategy:** the high-level strategic intent.
- **Variant:** the way that strategy is structured for a particular funding/protection/liability situation.
- **Report Architecture:** the sections, schedules, buckets, transitions, and calculations shown in the client report.
- **Scenario:** a quantified what-if or alternative path.
- **Actions:** concrete implementation steps.

Techniques such as Bucketing, Laddering, Cash-flow Matching, Asset Earmarking, and Goal Segmentation remain separate from Variants.

---

## Variant Design Principles

1. A Variant must change the architecture of the strategy, not merely rename a technique.
2. Variants must be mutually distinguishable by the funding/protection pattern they solve.
3. The same Variant can apply to multiple goal types when the underlying architecture is the same.
4. SIP, Lumpsum, Step-up SIP, Bucketing, Laddering, and similar mechanisms are not Variants; they remain techniques/components/solutions in the Strategy Architecture Matrix.
5. A report should expose the Variant because it explains why the implementation is structured that way.
6. Where a Variant is derived from recurring patterns in the client plans rather than explicitly named in a source report, it should be treated as an architecture label, not as a source-plan term.

---

## 1. Progressive De-risking

**Strategic intent:** Protect achieved goal funding as the goal approaches while preserving appropriate growth opportunity earlier in the horizon.

| Variant | When it applies | Core architecture | Typical report output |
|---|---|---|---|
| Goal-Date Glide Path | Single fixed goal/payment date | Growth → Stabilisation → Liquid as the goal date approaches | Goal-date funding schedule + de-risking timeline |
| Payment-Tranche Glide Path | Multi-year or multi-payment goal | Protect the next payment tranche while later tranches retain growth exposure | Tranche-wise corpus + protection/de-risking schedule |
| Recurring-Cashflow Glide Path | Recurring withdrawals or repeating goals | Protect next cycle → withdraw → rebuild/refill next cycle | Recurring cashflow plan + refill schedule |
| Income-Transition Glide Path | Retirement / passive-income transition | Near-term reserve + intermediate bucket + long-term growth bucket | Accumulation → transition → distribution architecture |

### Source-plan grounding

- Education plans use staged de-risking for future tuition payments and progressively move the amount required for upcoming payments toward safer/liquid assets.
- Vacation plans use a recurring cycle: protect the next trip bucket, withdraw for the trip, then rebuild the next bucket.
- Retirement plans use a transition architecture with near-term, intermediate, and long-term buckets and progressive safety as retirement approaches.
- Wedding and home plans use goal-date de-risking toward the required purchase/payment date.

---

## 2. Capital Preservation

**Strategic intent:** Prioritise preservation and predictability of required capital when the relevant capital requirement is near-term or high priority.

| Variant | When it applies | Core architecture | Typical report output |
|---|---|---|---|
| Full-Goal Preservation | The full required amount must be protected for a near-term/high-priority goal | Preserve the complete required target | Capital-protection plan + liquidity schedule |
| First-Payment Preservation | A goal has multiple future payments | Preserve only the imminent payment requirement; later requirements can retain more growth opportunity | Payment-wise liquidity/protection plan |
| Rolling Reserve Preservation | The goal repeats over time | Maintain a protected next-cycle reserve → use it → rebuild the reserve | Rolling reserve + withdrawal/rebuild schedule |
| Protected-Core Preservation | Required capital is identifiable but additional surplus exists | Protect the required core; allow surplus to pursue growth | Protected core + growth surplus architecture |

### Source-plan grounding

- Education plans separate the education corpus, college-year cashflow, loan funding, and contingency; upcoming payment requirements progressively move to safer/liquid assets.
- Vacation plans ring-fence the next 1–2 years of travel requirements and refill the next-trip bucket after each withdrawal.
- Wedding and home plans progressively move required capital toward safer/liquid holdings as the goal date approaches.
- The Protected-Core Preservation label is an architecture abstraction from the separation of required goal funding from surplus resources; it is not a named source-plan variant.

---

## 3. Debt Reduction

**Strategic intent:** Reduce liability burden where debt materially constrains goal funding or financial resilience.

| Variant | When it applies | Core architecture | Typical report output |
|---|---|---|---|
| Goal-Gap Debt Reduction | Debt materially contributes to the goal funding shortfall | Allocate resources between debt reduction and goal funding based on the binding goal constraint | Revised funding gap + debt reduction path |
| EMI-Relief Debt Reduction | EMI burden is the main cash-flow constraint | Reduce required EMI outflow to release monthly surplus | EMI reduction + surplus redeployment plan |
| Residual-Gap Debt Reduction | A defined residual funding gap remains after available resources | Coordinate debt reduction with the residual goal gap rather than treating debt in isolation | Residual gap + repayment/funding schedule |
| Goal-Linked Debt Reduction | Liability repayment and goal funding are interdependent | Coordinate repayment timing with goal contributions and required liquidity | Integrated goal + debt cash-flow plan |

### Source-plan grounding

The client plans explicitly separate loan financing from investment selection, quantify EMI affordability, and treat borrowing as a defined funding component for residual gaps. The exact Debt Reduction variant labels above are architecture labels derived from those patterns rather than named source-plan labels.

---

## 4. Credit Utilisation

**Strategic intent:** Determine whether credit can responsibly bridge a funding or timing mismatch without replacing the primary self-funding architecture.

| Variant | When it applies | Core architecture | Typical report output |
|---|---|---|---|
| Residual-Gap Bridge | Own resources leave a defined residual gap | Self-fund first → use credit only for the residual gap | Funding gap + residual credit requirement |
| Partial-Goal Financing | A defined portion of the goal is intentionally financed | Self-funded portion + explicitly financed portion | Self-funding vs financed split |
| EMI-Cap Financing | Credit is constrained by sustainable cash-flow capacity | Determine permissible credit from an EMI affordability ceiling | Loan amount → EMI → affordability assessment |
| Timing-Bridge Financing | Funding resources and payment timing do not align | Use temporary/defined credit to bridge the timing mismatch, with a repayment path | Timing mismatch + bridge requirement + repayment plan |

### Source-plan grounding

- Education explicitly uses an education loan as a planned funding component for the residual amount after corpus, scholarship, and cash-flow considerations.
- Wedding plans compare no-loan and partial-loan architectures and state that borrowing should be limited to a defined residual gap.
- Home purchase plans combine down-payment funding with a defined home loan and test future EMI sustainability.
- Timing-Bridge Financing is an architecture abstraction from the plans' treatment of funding/timing mismatches; it should not be presented as a source-plan term.

---

## Variant Selection Logic

Variant selection should occur **after Strategy eligibility** and before report/scenario generation.

### Step 1 — Select Strategy

Apply the Strategy Decision Flow and the 8-Fit Eligibility Gate:

- Cash-flow Fit
- Liquidity Fit
- Debt Fit
- Asset Resource Fit
- Risk Capacity Fit
- Goal Constraint Fit
- Multi-goal Conflict Fit
- Implementation Fit

### Step 2 — Identify the funding/protection pattern

Determine which structural pattern is present:

- Single fixed target/date
- Multiple payment tranches
- Recurring withdrawals
- Retirement/income transition
- Full near-term capital requirement
- Protected first payment
- Rolling reserve requirement
- Protected core + surplus
- Debt-driven goal constraint
- EMI-driven cash-flow constraint
- Residual funding gap
- Defined partial financing
- Timing mismatch

### Step 3 — Select Variant

Choose the Variant whose architecture best matches the structural pattern.

### Step 4 — Build the report architecture

The selected Variant determines what the report should show, for example:

- Funding gap and required contribution
- Goal-date or tranche-wise de-risking schedule
- Protected amount and liquidity dates
- Recurring withdrawal/refill cycle
- Debt/EMI impact
- Self-funded vs credit-funded amount
- What-if scenarios
- Action plan

### Step 5 — Generate scenario and actions

Quantify the selected architecture and produce the implementation actions.

---

## Example Mappings

| Goal pattern | Strategy | Variant | Report architecture |
|---|---|---|---|
| Education with staged tuition payments | Progressive De-risking | Payment-Tranche Glide Path | Education corpus → payment tranches → de-risking dates → liquid requirement → residual funding/loan |
| Annual domestic + biennial international travel | Progressive De-risking | Recurring-Cashflow Glide Path | Next-trip reserve → withdrawal → refill → next-cycle reserve |
| Retirement at a defined age | Progressive De-risking | Income-Transition Glide Path | Accumulation → transition glide path → near-term reserve → intermediate bucket → long-term growth → distribution |
| Wedding with full corpus requirement approaching | Capital Preservation | Full-Goal Preservation | Required corpus → protected amount → liquidity timeline → payment readiness |
| Education with several college-year payments | Capital Preservation | First-Payment Preservation | Upcoming tuition requirement protected → later payments remain separately planned |
| Wedding with defined residual loan requirement | Credit Utilisation | Residual-Gap Bridge | Self-funded corpus → residual gap → defined loan portion → post-wedding EMI/cashflow |
| Home purchase constrained by EMI capacity | Credit Utilisation | EMI-Cap Financing | Down payment → loan capacity → EMI affordability → emergency reserve → purchase feasibility |

---

## Boundary: Variant vs Technique vs Component

| Layer | Example | Meaning |
|---|---|---|
| Strategy | Progressive De-risking | Strategic intent |
| Variant | Payment-Tranche Glide Path | Implementation architecture |
| Technique | Bucketing; Cash-flow Matching; Laddering | Method used to execute the architecture |
| Component | Transition; Liquidity; Debt; Funding | Building block of the strategy |
| Solution | Glide Path; Bucketing; Cash-flow Matching | Concrete solution pattern |
| Scenario | Higher cost / lower return / delayed goal | Quantified alternative |
| Action | Shift required amount to safer/liquid assets | Client implementation step |

---

## Relationship to strategy-matrix.md

The Strategy Architecture Matrix remains the authoritative matrix for:

- Strategy Family
- Applicable Goal Types
- Activation Characteristics
- Strategic Objective
- Required Inputs
- Strategic Levers
- Variants
- Techniques
- Components
- Solutions
- Baseline Profile
- Trade-offs

This document provides the **detailed definition and report architecture of the Variant layer**. It should be referenced when populating or expanding the Variants column in the matrix.


---

## PDF Generation Architecture

The PDF layer should **not** have a separate PDF generator for every goal type.

The preferred architecture is:

**Goal Type → Strategy → Variant → Report Config → Common PDF Renderer**

### Core principle

Use **one common PDF rendering engine** and make the report structure/configuration goal-aware and strategy/variant-aware.

A goal type should not create its own independent PDF-generation implementation. Instead, it should provide the configuration and data required by the common renderer.

### Responsibilities by layer

| Layer | Responsibility |
|---|---|
| Goal Type | Defines goal-specific terminology, inputs, calculations, milestones, and required report sections |
| Strategy | Defines the strategic objective and applicable decision framework |
| Variant | Defines the implementation architecture and which report pattern should be used |
| Report Config | Maps the selected goal + strategy + variant into sections, tables, schedules, narratives, and calculations |
| Common PDF Renderer | Handles layout, typography, headers/footers, page breaks, tables, charts, styles, and final PDF generation |

### Recommended flow

`Client Data → Goal Analysis → Strategy Selection → Variant Selection → Report Config → Common PDF Renderer → PDF`

The renderer should receive a structured report model rather than containing hard-coded logic for Education, Wedding, Vacation, Retirement, etc.

### Example

| Goal Type | Strategy | Variant | Report Config | Renderer |
|---|---|---|---|---|
| Education | Progressive De-risking | Payment-Tranche Glide Path | Education + tranche schedule | Common PDF Renderer |
| Wedding | Progressive De-risking / Capital Preservation | Goal-Date / Full-Goal Preservation | Wedding + goal-date protection | Common PDF Renderer |
| Vacation | Progressive De-risking | Recurring-Cashflow Glide Path | Recurring trip + refill cycle | Common PDF Renderer |
| Retirement | Progressive De-risking | Income-Transition Glide Path | Accumulation + transition + distribution | Common PDF Renderer |
| Home Purchase | Progressive De-risking / Credit Utilisation | Goal-Date / EMI-Cap Financing | Down payment + loan + EMI feasibility | Common PDF Renderer |

### What should vary by goal

The following can be goal-specific through configuration:

- Section ordering
- Goal-specific calculations
- Required inputs
- Goal milestones
- Funding-gap presentation
- De-risking schedule
- Payment/tranche schedule
- Debt or credit section
- What-if scenarios
- Action plan
- Goal-specific terminology and explanatory text

### What should remain common

The following should remain in the shared PDF engine:

- Page/layout system
- Typography and styles
- Header/footer
- Tables
- Charts
- Page numbering
- Cover/page templates
- Reusable financial summary blocks
- Section rendering primitives
- PDF export
- Validation of the final report model

### Architectural rule

**Do not create:**

`education_pdf_generator.py`  
`wedding_pdf_generator.py`  
`vacation_pdf_generator.py`  
`retirement_pdf_generator.py`

as independent report engines.

**Prefer:**

`report_engine/`  
→ common renderer  
→ shared section components  
→ report schemas  
→ goal-specific report configs  
→ strategy/variant mappings

This keeps the reporting layer extensible: adding a new goal type should normally require a new configuration/schema and goal-specific sections, not a new PDF rendering engine.

### Separation of concerns

A useful implementation boundary is:

**Calculations → Report Model → Report Config → PDF Renderer**

- **Calculations** determine the financial outputs.
- **Report Model** stores normalized outputs required by the report.
- **Report Config** decides what should be shown and in what structure.
- **PDF Renderer** turns that structure into the final document.

This also allows the same report model to support other outputs later, such as HTML, web views, client dashboards, or API responses, without duplicating financial logic.
