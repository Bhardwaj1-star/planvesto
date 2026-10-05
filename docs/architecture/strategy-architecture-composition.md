# Strategy Architecture & Composition

**Status:** CANONICAL  
**Scope:** Construction of the executable strategy architecture for a goal.

## Architecture

A Strategy Architecture is the composed implementation structure selected for a goal.

| Layer | Responsibility |
|---|---|
| Primary Strategy | Owns the main financial responsibility |
| Supporting Strategies | Address additional required responsibilities |
| Techniques | Concrete mechanisms used by the architecture |
| Components | Functional strategy building blocks |
| Solutions | Concrete implementation paths |
| Architecture Rationale | Explains why the composition exists |
| Trade-offs | Captures consequences of the composition |
| Constraints | Records relevant decision limits |

## Runtime Flow

**Defined Goal → Applicable Strategies → 8-Fit Eligibility → Decision → Architecture Composition → Technique Execution**

## Code Ownership

- `backend/engines/strategy/composition.py` — architecture composition
- `backend/engines/strategy/identity.py` — canonical architecture identity
- `backend/models/strategy.py` — StrategyArchitecture model
- `backend/library/strategies/canonical.py` — canonical strategies
- `backend/library/strategies/solution_matrix.py` — strategy-to-solution mapping
- `backend/library/strategies/components.py` — component registry
- `backend/library/strategies/techniques_canonical.py` — technique registry
- `backend/engines/technique/engine.py` — technique execution

## Identity

Architecture identity is based on the owning goal and primary strategy. Supporting strategies, techniques and solutions are composition data, not identity.

## Composition Rules

The primary strategy establishes the main responsibility. Supporting strategies may be added when the decision architecture requires additional responsibilities. Techniques are de-duplicated when composed.

Goal Funding remains a canonical first-class strategy. Its six funding variants are solutions within that strategy, not separate canonical strategies.

## Execution Boundary

Composition selects the architecture. Technique Engine executes the selected techniques. Composition must not itself perform technique calculations.

## Persistence

The finalized architecture is carried into Strategy Version and Strategy Run records so the selected decision remains reproducible.
