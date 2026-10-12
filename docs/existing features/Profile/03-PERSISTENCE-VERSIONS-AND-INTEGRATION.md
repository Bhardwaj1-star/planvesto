# Profile — Persistence, Versions and Integration

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## Persistence lifecycle

`ProfileService` assembles a payload containing planning unit, investor, engine version, requested profile version, Financial State snapshot ID, full input snapshot and engine result. It allocates a version using `ProfileRepository.next_version()`, writes the profile run, then writes constraints and conflicts. Version-conflict errors are retried up to three attempts; other failures propagate. The run and child rows are separate writes in the inspected service path, so partial persistence failure deserves explicit testing.

Latest/history reads delegate to `ProfileRepository`. The API validates investor ownership and constrains history limit. Database constraints/migration `015_profile_constraints.sql` and reconciliation migration provide source evidence, not proof of live production schema.

## Integration boundary

The profile engine produces constraint/risk/behavior/identity evidence for planning. It does not itself select a strategy or accept a plan. Strategy Builder should consume canonical constraint/profile outputs only through its explicit integration path; do not infer that all engine outputs are wired into every strategy request.

## Freshness and authority

The stored snapshot ID records the financial state used at build time. Latest profile means newest persisted profile run, not necessarily a profile built from the current Financial State unless snapshot freshness is checked. Profile priorities are ordering metadata and must not override hard constraint authority.
