# Strategy Output Architecture Specification

## Purpose

Strategy Builder is a **goal-agnostic financial strategy engine**. It must work for every supported financial goal, not only retirement.

Retirement is one goal type. Its Retirement Report/PDF is one goal-specific downstream output; it must not define the Strategy Builder architecture.

## Canonical Product Flow

`Financial State → Goal → Strategy Builder → Strategy Result → Goal-specific Output`

For retirement:

`Financial State → Retirement Goal → Strategy Builder → Strategy Result → Retirement Report → PDF`

For other goals, the same Strategy Builder produces the generic Strategy Result. Any later report or presentation is determined by that goal's requirements.

## Core Strategy Decision Model

The current backend decision engine evaluates strategy architectures using explicit strategy-fit evidence. The decision sequence is:

1. **Eligibility gate** — determine whether a strategy architecture is applicable to the investor and goal.
2. **Goal fit** — evaluate the strategy's suitability for the canonical goal type and applicable goal characteristics.
3. **Horizon fit** — evaluate suitability against the goal's time horizon.
4. **Funding fit** — evaluate the strategy against the goal's funding status and funding gap.
5. **Feasibility / constraint compatibility** — evaluate whether the architecture can be implemented under its constraints.
6. **Component fit** — incorporate applicable component metadata/supporting strategies where present.
7. **Deterministic comparison** — compare eligible architectures using the explicit decision evidence and select the recommended architecture plus alternatives.

The authoritative backend implementation is `backend/engines/strategy/decision.py`. fileciteturn535file0 fileciteturn536file0

### Explicitly Removed From Decision Authority

`Safety`, `Liquidity`, `Growth`, and `Flexibility` are **not strategy-selection dimensions** and must not determine the recommendation. The legacy composite score must not determine ranking or recommendation either. The current ranking implementation documents these values as descriptive/backward-compatibility evidence rather than decision authority. fileciteturn534file0

Therefore, new Strategy Builder UI, API contracts, tests, documentation, and future strategy logic must not reintroduce these four dimensions as strategy identity, ranking criteria, or recommendation criteria.

## Generic Strategy Result

The Strategy Result should expose, as applicable:

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

These are generic strategy outputs and must remain usable for every supported goal.

## Retirement Output

Retirement may additionally provide:

- Retirement Report
- Retirement-specific projections and rationale
- PDF export

These are downstream retirement capabilities. They must not be mandatory fields or mandatory navigation for every strategy run.

## Other Financial Goals

The architecture must support the same generic Strategy Builder for education, home purchase, vehicle purchase, major expenses, and other supported goals. Goal-specific reports can be introduced independently without rewriting the Strategy Builder decision engine or generic Strategy Result contract.

## Existing Investor Capabilities

Moneywheel and Budgeting are independent investor capabilities. They must remain available unless a separate authoritative product specification explicitly deprecates them. Their removal from sidebar navigation must not be interpreted as permission to delete their routes, backend services, or product functionality. 

## Navigation Rule

Strategy-specific lifecycle routes may be contextual rather than primary sidebar navigation. Hiding a route from the sidebar does **not** mean deleting the underlying route or backend lifecycle capability when it is required by the strategy workflow.

## Acceptance Criteria

- Retirement can complete Strategy Builder and reach Retirement Report/PDF.
- Non-retirement goals can complete Strategy Builder without requiring Retirement Report/PDF.
- Strategy API contracts remain goal-agnostic.
- Retirement-specific code remains downstream of the generic Strategy Result.
- Adding another goal-specific report does not require rewriting Strategy Builder.
- Safety/Liquidity/Growth/Flexibility cannot determine the recommended strategy.
- Composite score cannot determine the recommended strategy.
- Eligibility, goal fit, horizon fit, funding fit, feasibility/constraints, and applicable component fit remain the decision evidence defined by the backend.
- Moneywheel and Budgeting remain available unless separately deprecated by an authoritative specification.
- Tests cover at least one retirement and one non-retirement strategy flow.
