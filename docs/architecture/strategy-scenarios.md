# Strategy Scenarios Architecture

**Status:** CANONICAL  
**Scope:** Strategy scenario generation, assumptions, funding structures, and scenario comparison.

## Architecture

| Stage | Source | Responsibility | Output |
|---|---|---|---|
| Defined Goal | Goal Planner | Target, horizon, funding gap, mapped resources | Defined Goal |
| Strategy Candidate | Strategy Decision | Applicable/eligible strategy | Strategy Definition |
| Baseline Scenario Generation | `backend/engines/strategy/scenario.py` | Build deterministic strategy-specific scenarios | Scenario[] |
| Scenario Metrics | Scenario Engine | Funding projection, gap, contribution, certainty evidence | Scenario metrics |
| Scenario Comparison | `backend/engines/strategy/comparison.py` | Normalize scenarios side-by-side | Comparison matrix |
| Ranking | `backend/engines/strategy/ranking.py` | Combine decision result with scenario evidence | Ranked scenarios |

## Scenario Model

A Scenario belongs to one Strategy and contains:
- scenario_id
- strategy_id
- scenario_type
- scenario_name
- assumptions
- funding_structure
- metrics
- trade_off_notes
- investor-modification state where supported

Scenario types are **baseline**, **modified**, and **custom**.

## Baseline Generation

Goal Funding scenarios are generated from the canonical Goal Funding variants. The engine calculates incremental contribution/lumpsum effects without double-counting already projected mapped assets.

Current funding evidence includes:
- target corpus
- projected total resources
- funding gap
- required monthly contribution
- additional monthly contribution
- additional lumpsum
- annual step-up
- duration
- return assumption
- funded ratio
- deterministic success-probability band

Non-Goal-Funding strategies receive strategy-specific baseline scenario construction from the Strategy Engine.

## Decision Boundary

Scenario generation does **not** decide the final strategy. Eligibility and decision remain authoritative in the Strategy Decision layer.

Flow:

**Goal → Applicability → Candidate Strategy → 8-Fit Eligibility → Scenario Generation → Decision/Ranking → Recommendation**

## Data Ownership

| Data | Owner |
|---|---|
| Goal target/horizon/gap | Goal Planner |
| Strategy definition | Strategy Library |
| Scenario assumptions | Scenario Engine |
| Funding projection | Goal/Scenario calculation logic |
| Eligibility | Strategy Eligibility |
| Final recommendation | Strategy Decision |

## Implementation Notes

Scenario comparison is descriptive evidence. The authoritative recommendation comes from `DecisionResult`; ranking consumes that result rather than independently overriding it.
