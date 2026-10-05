# Strategy Versioning & Approval Architecture

**Status:** CANONICAL  
**Scope:** Immutable strategy snapshots, investor edits, selection and approval lifecycle.

## Purpose

A Strategy Version freezes the implementation state used for an approved strategy so later library changes do not silently change an investor's selected plan.

## Version Creation

`StrategyVersionService`:
1. resolves the active Strategy Definition;
2. validates implementation parameters;
3. validates parent version when present;
4. assigns the next version number;
5. stores library/implementation versions;
6. stores Goal and architecture context;
7. stores decision snapshot and source Strategy Run.

## Sources

Supported version sources:
- `library`
- `investor_edit`

Investor edits require a parent version.

Implementation parameters are validated against Strategy Library definitions. Non-editable parameters cannot be changed in an investor-derived version.

## Lifecycle Boundary

New versions are created as **draft** or **provisional**. Approval and Primary/selected lifecycle are separate records and must not mutate the immutable version snapshot.

## Selection

The selected/current Strategy Version is the version used downstream for:
- action generation
- current goal implementation
- reporting
- multi-goal planning

## Action Gate

Only an approved and currently selected Strategy Version can generate actions.

## Persistence

Relevant code:
- `backend/models/strategy_version.py`
- `backend/services/strategy_version_service.py`
- `backend/data/strategy_version_repository.py`
- `backend/models/primary_strategy_state.py`
- `backend/data/primary_strategy_repository.py`

## Reproducibility

A version retains:
- strategy ID/version
- library version
- implementation version
- implementation parameters
- defined goal/version
- architecture
- decision snapshot
- source Strategy Run

This provides an auditable decision snapshot.
