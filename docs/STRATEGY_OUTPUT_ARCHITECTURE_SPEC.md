# Strategy Output Architecture Specification

**Status:** Final architecture contract

## 1. Objective

Define the output architecture of the **goal-agnostic Strategy Builder** after conversion from the legacy score-driven model.

Strategy Builder determines applicable strategy architectures for a specific investor and goal, compares eligible architectures using explicit strategy-fit evidence, and produces a generic Strategy Result. Goal-specific reports are downstream outputs of that result.

Safety, Liquidity, Growth, Flexibility, and legacy composite scoring are not strategy-selection mechanisms.

## 2. Core Principle

**Strategy Builder is not a retirement planner. Retirement is one supported goal.**

The strategy decision answers:

> For THIS investor, for THIS goal, given THIS financial state and THESE priorities, what is the appropriate way to fund and achieve the goal?

## 3. Canonical Flow

`Financial State → Goal → Strategy Builder → Strategy Result → Goal-specific Output`

Retirement example:

`Financial State → Retirement Goal → Strategy Builder → Strategy Result → Retirement Report → PDF`

Other goals follow the same generic flow and do not require retirement-specific outputs.

## 4. Strategy Result Architecture

The generic Strategy Result may contain:

- Goal reference
- Recommended strategy architecture
- Why it fits / goal fit
- Eligibility status and diagnostics
- Feasibility
- Constraints
- Trade-offs
- Assumptions
- Techniques / implementation direction
- Alternative eligible architectures
- Scenarios / stress-test information
- Implementation parameters

The contract remains goal-agnostic. Retirement-specific fields are not mandatory for other goals.

## 5. Decision Authority

Strategy architectures are determined through:

1. Eligibility/applicability
2. Goal fit
3. Horizon fit
4. Funding fit
5. Feasibility and constraint compatibility
6. Applicable component/strategy evidence
7. Deterministic comparison of eligible architectures

The following must **not** determine strategy identity, eligibility, ranking, recommendation, or Strategy Result presentation:

- Safety
- Liquidity
- Growth
- Flexibility
- Legacy composite score

Legacy fields may exist for compatibility or historical evidence only.

## 6. Goal-Specific Outputs

Strategy Builder produces the generic Strategy Result. A goal-specific layer consumes it.

### Retirement

Retirement may produce:

- Retirement Report
- Retirement-specific projections and rationale
- PDF export

### Other Goals

Education, home purchase, vehicle purchase, major expense, and other supported goals may later receive their own reports or outputs. Adding one must not require rewriting the generic Strategy Builder.

## 7. Frontend Contract

The Strategy Builder UI represents strategy architectures and strategy-fit evidence, including where available:

- Strategy name
- Purpose / what it does
- Why applicable / goal fit
- Feasibility
- Constraints
- Trade-offs
- Assumptions
- Techniques
- Scenario/stress-test information
- Recommendation reasoning
- Alternatives

Safety/Liquidity/Growth/Flexibility must not appear as competing strategy identities or ranking criteria.

## 8. Retirement Boundary

Retirement Report/PDF is a **downstream retirement capability**, not part of the generic Strategy Builder contract.

The Strategy Builder must therefore be able to complete successfully for a non-retirement goal without creating, loading, or requiring a Retirement Report.

Retirement-specific reporting must consume the final generic Strategy Result rather than independently reconstructing the strategy decision.

## 9. Existing Investor Capabilities

Moneywheel and Budgeting are independent product capabilities. They are not removed or deprecated by this architecture specification.

Strategy-specific lifecycle pages may be contextual rather than primary sidebar navigation. Hiding a route from the sidebar does not authorize deletion of its underlying route or backend capability when the workflow still depends on it.

## 10. Acceptance Criteria

- Strategy Builder works through the same architecture for retirement and non-retirement goals.
- Eligible architectures are determined before comparison/recommendation.
- Recommendation uses explicit strategy-fit evidence.
- Safety/Liquidity/Growth/Flexibility do not determine recommendation.
- Legacy composite scoring does not determine recommendation.
- Strategy Result is goal-agnostic.
- Retirement Report/PDF is retirement-specific downstream output.
- Non-retirement Strategy Results do not depend on retirement reporting.
- Future goal-specific outputs can be added without rewriting Strategy Builder.
- Moneywheel and Budgeting remain available unless separately deprecated by an explicit product decision.
- Tests cover at least one retirement and one non-retirement flow.
