# Step 04 — Multi-Goal Resource Allocation

## Purpose
Allocate shared financial resources across goals after single-goal strategies and constraints have been evaluated.

## Inputs
- Client-selected goal priority.
- Per-goal strategy result.
- Financial ratio/constraint results.
- Available surplus/resources.
- Existing financial-state context.

## Responsibilities
1. Determine total resources available for goal funding.
2. Detect resource competition across goals.
3. Apply explicit priority and constraint rules.
4. Resolve partial funding and infeasibility deterministically.
5. Preserve the reason for every material allocation decision.
6. Return goal-level and consolidated allocation results.

## Rule
Do not silently discard a client's priority. If a system rule changes the resulting allocation, preserve the client's original priority and the rule/reason causing the change for reporting.

## Do NOT
- Modify Supabase schema.
- Implement UI.
- Rewrite the Strategy Engine.
- Invent allocation thresholds without an approved business rule.

## Tests
Cover sufficient resources, competing goals, partial funding, infeasible combinations, and ratio-driven allocation changes.
