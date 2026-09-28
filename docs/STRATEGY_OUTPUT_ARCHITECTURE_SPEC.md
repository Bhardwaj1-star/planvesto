# Strategy Output Architecture Specification

## 1. Objective

Define the architecture of Strategy Builder as a **goal-agnostic financial strategy decision system**.

Strategy Builder must determine which strategy architectures are applicable to a specific investor and goal, evaluate those eligible architectures using explicit strategy-fit evidence, and produce a generic Strategy Result.

It must not be architected around retirement, a particular report, or the legacy Safety/Liquidity/Growth/Flexibility scoring model.

## 2. Core Principle

A financial goal determines the planning context. Strategy Builder determines the appropriate strategy architecture for that goal given the investor's financial state and constraints.

**Strategy Builder is not a retirement planner. Retirement is one supported goal.**

## 3. Canonical Flow

`Financial State → Goal → Strategy Builder → Strategy Result → Goal-specific Output`

Example:

`Financial State → Retirement Goal → Strategy Builder → Strategy Result → Retirement Report → PDF`

Another goal follows the same generic path:

`Financial State → Education/Home/Vehicle/etc. Goal → Strategy Builder → Strategy Result → Goal-specific Output`

A non-retirement goal must never require a Retirement Report or retirement PDF to complete Strategy Builder.

## 4. Strategy Decision Architecture

The Strategy Builder decision process is:

1. **Eligibility** — determine whether a strategy architecture is applicable to the investor and goal.
2. **Goal fit** — evaluate how the architecture fits the canonical goal and its characteristics.
3. **Horizon fit** — evaluate compatibility with the goal horizon.
4. **Funding fit** — evaluate compatibility with the goal's funding position/funding gap.
5. **Feasibility and constraints** — determine whether the architecture can realistically be implemented under its constraints.
6. **Component fit** — incorporate relevant strategy/component applicability where defined by the backend.
7. **Deterministic comparison** — compare eligible architectures using explicit evidence and produce a recommendation plus alternatives.

### 4.1 What Strategy Builder Must NOT Use as Decision Authority

The following are explicitly **not strategy-selection dimensions**:

- Safety
- Liquidity
- Growth
- Flexibility
- Legacy composite score

They must not determine strategy identity, eligibility, ranking, recommendation, or Strategy Result presentation.

If legacy dimension values remain anywhere for compatibility or historical data, they are non-authoritative metadata only and must not be reintroduced into the decision model.

## 5. Generic Strategy Result

The Strategy Result is the reusable output of Strategy Builder for every supported goal.

It may contain:

- Goal reference
- Recommended strategy architecture
- Strategy rationale / goal fit
- Eligibility status and diagnostics
- Feasibility status
- Constraints
- Trade-offs
- Assumptions
- Techniques / implementation direction
- Alternative architectures
- Scenario / stress-test information
- Implementation parameters

The contract must remain goal-agnostic. Retirement-specific fields must not be mandatory for all Strategy Results.

## 6. Goal-Specific Outputs

Goal-specific outputs are downstream presentation or implementation layers built on the generic Strategy Result.

### Retirement

Retirement may provide:

- Retirement Report
- Retirement-specific projections and rationale
- PDF export

### Other Goals

Education, home purchase, vehicle purchase, major expense, and other supported goals may receive their own appropriate output/report in the future.

Adding a new goal-specific output must not require rewriting the core Strategy Builder decision engine or generic Strategy Result contract.

## 7. Frontend Architecture

The Strategy Builder UI must present strategy architecture and decision evidence—not the legacy four-dimension scoring model.

Architecture presentation should expose applicable information such as:

- Purpose
- Why applicable / goal fit
- Feasibility
- Constraints
- Trade-offs
- Assumptions
- Techniques / implementation direction
- Scenarios / stress-test information
- Recommendation reasoning
- Alternatives

The UI must not present Safety/Liquidity/Growth/Flexibility as strategy identity or ranking criteria.

## 8. Navigation and Existing Capabilities

Strategy-specific lifecycle pages may be contextual rather than primary sidebar navigation. Removing a page from the sidebar does **not** mean deleting the underlying route or backend capability unless an authoritative specification explicitly requires deletion.

Existing investor capabilities such as **Moneywheel** and **Budgeting** remain part of the product unless separately deprecated by an authoritative product decision.

## 9. Separation of Responsibilities

**Strategy Builder:** decides the appropriate strategy architecture.

**Strategy Result:** communicates the generic decision and its evidence.

**Goal-specific output:** presents or operationalizes that result for a particular goal.

**Retirement Report/PDF:** retirement-specific downstream output only.

This separation prevents retirement-specific implementation from becoming a hidden dependency of the generic Strategy Builder.

## 10. Acceptance Criteria

- Strategy Builder works for retirement and non-retirement goals through the same generic decision architecture.
- Eligible strategy architectures are determined before comparison/recommendation.
- Recommendation is based on explicit strategy-fit evidence.
- Safety/Liquidity/Growth/Flexibility do not determine the recommendation.
- Legacy composite scoring does not determine the recommendation.
- Strategy Result remains goal-agnostic.
- Retirement Report/PDF is required only for retirement-specific output.
- A non-retirement Strategy Result can complete without retirement-report dependencies.
- Goal-specific outputs can be added without rewriting Strategy Builder.
- Moneywheel and Budgeting are not removed as a side effect of strategy/retirement cleanup.
- Contextual strategy routes are not deleted merely because they are absent from the primary sidebar.
- Tests cover at least one retirement and one non-retirement Strategy Builder flow.
