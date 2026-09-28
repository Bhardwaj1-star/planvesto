# Strategy Output Architecture Specification

## Purpose

Strategy Builder is a **goal-agnostic financial strategy engine**. It must work for every supported financial goal, not only retirement.

Retirement is one goal type and its Retirement Report/PDF is one goal-specific output. It must not become the architectural definition of Strategy Builder.

## Canonical Product Flow

`Financial State → Goal → Strategy Builder → Strategy Result → Goal-specific Output`

For retirement:

`Financial State → Retirement Goal → Strategy Builder → Strategy Result → Retirement Report → PDF`

For other goals, the same Strategy Builder produces the strategy result, while the final presentation/report is determined by that goal's requirements.

## Core Rules

1. Strategy Builder must remain reusable across all supported financial goals.
2. No retirement-specific logic may become a prerequisite for Strategy Builder completion.
3. `StrategyRun` / `StrategyRecommendation` are generic contracts and must not require retirement-report fields.
4. Retirement Report is a **goal-specific presentation/output layer**, not the Strategy Builder itself.
5. The UI must not assume that every completed strategy has a Retirement Report or PDF.
6. Goal-specific reports may be introduced independently without changing the core Strategy Builder architecture.
7. Existing capabilities such as Budgeting and Moneywheel are independent investor capabilities and must not be removed merely because the retirement flow is being implemented.

## Output Model

The generic Strategy Result should contain, as applicable:

- Goal reference
- Selected/recommended strategy architecture
- Strategy rationale / goal fit
- Eligibility and feasibility
- Constraints
- Trade-offs
- Assumptions
- Techniques / implementation direction
- Alternatives
- Scenarios / stress-test information
- Implementation parameters

Goal-specific output is layered on top of this result.

## Retirement Output

Retirement may additionally provide:

- Retirement Report
- Retirement-specific projections and rationale
- PDF export

These are downstream retirement capabilities and must not be embedded as mandatory fields or mandatory navigation for every goal.

## Other Financial Goals

The architecture must support equivalent goal-specific outputs in the future, for example education, home purchase, vehicle purchase, major expense, or other supported goals. The exact reports are not defined by this document; they must be added without changing the generic Strategy Builder contract.

## Navigation Rule

Keep existing investor capabilities such as Moneywheel and Budgeting available unless an explicit product specification says otherwise. Strategy-specific routes may be contextual rather than primary navigation, but they must not be deleted solely because they are not visible in the sidebar.

## Acceptance Criteria

- A retirement goal can complete Strategy Builder and reach Retirement Report/PDF.
- A non-retirement goal can complete Strategy Builder without requiring Retirement Report/PDF.
- Strategy API contracts remain goal-agnostic.
- Retirement-specific code is downstream of the generic strategy result.
- Adding another goal-specific report does not require rewriting Strategy Builder.
- Moneywheel and Budgeting remain available unless separately deprecated by an authoritative specification.
- Tests cover at least one retirement and one non-retirement strategy flow.
