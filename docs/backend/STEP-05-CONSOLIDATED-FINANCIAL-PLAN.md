# Step 05 — Consolidated Financial Plan

## Purpose
Transform the resolved multi-goal orchestration result into one coherent financial-plan data structure.

## Responsibilities
- Consolidate all selected goals.
- Store client priority and resolved priority/allocation separately.
- Include each goal's strategy, funding requirement, allocation, feasibility and constraints.
- Include cross-goal trade-offs and unresolved limitations.
- Produce a deterministic machine-readable plan suitable for reporting and later API consumption.

## Architectural boundary
This layer assembles results; it does not independently calculate strategies or invent allocation rules.

## Do NOT
- Change database schema.
- Build frontend.
- Add product selection logic.
- Hide infeasible goals or trade-offs.

## Completion gate
A multi-goal request must produce one internally consistent Financial Plan object that can be consumed by report generation without recalculating business logic.
