# Step 03 — Financial Ratio & Constraint Layer

## Purpose
Define the backend layer that evaluates financial-health/ratio conditions relevant to goals and strategy allocation.

## Business rule already decided
The client chooses goal priority. Planvesto checks relevant financial ratios/financial-health conditions. If a defined rule conflicts with the client's priority, the system may override the resulting allocation/strategy outcome. The UI does not present this as an editable priority change; the final report explains the reason.

## Scope
- Identify which existing financial-state values are available for ratio calculation.
- Implement only ratios/business rules that are explicitly defined in the project.
- Return deterministic constraint results to the multi-goal orchestrator.
- Distinguish informational warnings from hard constraints.
- Keep client priority and system-resolved outcome separately traceable.

## Do NOT
- Invent ratio thresholds.
- Change database schema.
- Build frontend UI.
- Make product recommendations.
- Put ratio logic inside the single-goal Strategy Engine.

## Expected output
A pure, testable constraint evaluation layer consumed by the multi-goal orchestrator.
