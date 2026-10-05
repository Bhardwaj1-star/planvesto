# Strategy Recommendation & Ranking Architecture

**Status:** CANONICAL  
**Scope:** Final strategy decision, ranking evidence, recommendation and alternatives.

## Decision Flow

**Goal → Applicability Gate → Candidate Strategies → 8-Fit Eligibility Gate → Decision Score/Ranking → Recommendation**

## Decision Ownership

| Stage | Owner | Rule |
|---|---|---|
| Applicability | Strategy Applicability | Goal type + configured goal characteristics |
| Eligibility | Strategy Eligibility | Common 8-fit framework |
| Hard Gate | Constraint/Eligibility | Any hard failure makes candidate ineligible |
| Decision | Strategy Decision | Compare eligible architectures |
| Ranking | Strategy Ranking | Present ordered evidence |
| Recommendation | Strategy Recommendation | Materialize selected strategy and rationale |

## 8-Fit Framework

Every candidate is evaluated on:
1. Cash-flow Fit
2. Liquidity Fit
3. Debt Fit
4. Asset Resource Fit
5. Risk Capacity Fit
6. Goal Constraint Fit
7. Multi-goal Conflict Fit
8. Implementation Fit

Statuses are Pass, Conditional and Fail.

## Selection Rule

- Any hard failure makes the strategy ineligible.
- Pass candidates are preferred.
- Conditional candidates are considered only when no Pass candidate exists.
- The highest-ranked eligible candidate becomes the recommendation.
- If no candidate is eligible, the result is infeasible and must expose required changes/failures.

## Ranking Evidence

Current ranking exposes:
- safety
- liquidity
- growth
- flexibility
- funding-gap evidence
- decision rank
- eligibility state
- ineligible reasons
- alternative indication

Composite/dimension scores are evidence; authoritative recommendation remains the Strategy Decision result.

## Output

Recommendation contains:
- recommended strategy
- recommended scenario
- short reasons
- complete reasoning
- selected architecture
- alternative architecture IDs
- feasibility status
- constraints

## Code

- `backend/engines/strategy/decision.py`
- `backend/engines/strategy/ranking.py`
- `backend/engines/strategy/recommendation.py`
- `backend/engines/strategy/eligibility.py`
