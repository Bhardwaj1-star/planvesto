# Dead / Legacy Data Audit & Remediation Log

| # | Dead / Legacy Item | Status | Code / File Evidence | Finding & Remediation Status |
|---|---|---|---|---|
| 1 | `targetAge` | **Resolved / Removed** | `frontend/lib/onboarding/goals/types.ts`<br>`frontend/lib/onboarding/goals/goals.ts`<br>`frontend/lib/onboarding/persistence.ts` | Removed orphaned `targetAge` from frontend Goal model, helpers, and load mapping. |
| 2 | `currentSavedAmount` | **Resolved / Removed** | `frontend/lib/onboarding/goals/types.ts`<br>`frontend/lib/onboarding/persistence.ts` | Removed orphaned `currentSavedAmount` from Goal model and persistence layer. |
| 3 | Goal-level `monthlyContribution` | **Resolved / Removed** | `frontend/lib/onboarding/goals/types.ts`<br>`frontend/lib/onboarding/persistence.ts` | Removed orphaned input; contribution is canonicalized via `DefinedGoal.required_monthly_contribution`. |
| 4 | `inflationApplicability` | **Resolved / Removed** | `frontend/lib/onboarding/goals/types.ts`<br>`frontend/lib/onboarding/persistence.ts` | Removed orphaned field; canonical inflation is driven by `inflation_rate`. |
| 5 | Goal-level `notes` | **Resolved / Removed** | `frontend/lib/onboarding/goals/types.ts`<br>`frontend/lib/onboarding/persistence.ts` | Removed orphaned field from Goal model and persistence layer. |
| 6 | `specialized_data` | **Resolved / Removed** | `backend/schemas/goals.py`<br>`backend/tests/test_goal_engine_build.py` | Removed dead contract residue from `GoalInput`; production calculations use `dynamic_details`. |
| 7 | `backend/engines/health_score/` | **Resolved / Removed** | `backend/engines/health_score/` | Dead directory deleted completely from repository. |
| 8 | Retirement DOB auto-enrichment block | **Resolved / Removed** | `backend/services/goal_service.py` | Removed unreachable dead code below early `return` in `_enrich_retirement_context()`. |
| 9 | MoneyWheel legacy ratio aliases | **Resolved / Removed** | `backend/rules/moneywheel.py` | `LEGACY_RATIO_ALIASES` deleted; MoneyWheel strictly reflects 9 canonical ratios. |
| 10 | MoneyWheel compatibility ratio definitions | **Resolved / Removed** | `backend/rules/moneywheel.py` | `COMPATIBILITY_RATIO_DEFINITIONS` deleted; coverage rules separated from MoneyWheel. |
| 11 | FinancialPlanService duplicate DTI calculation | **Resolved / Aligned** | `backend/services/financial_plan_service.py` | Replaced duplicate ad-hoc formula with canonical `calculate_debt_to_income_ratio()`. |
| 12 | FinancialPlanService duplicate emergency coverage | **Resolved / Aligned** | `backend/services/financial_plan_service.py` | Replaced ad-hoc formula with canonical `calculate_emergency_coverage()`. |
| 13 | Duplicate Risk Profile adapter surface | **Resolved / Consolidated** | `backend/engines/risk_profiler/engine.py`<br>`backend/tests/test_risk_profile.py` | Tests and callers consolidated to canonical `engines.risk_profiler.engine`. |
| 14 | Priority ranking definitions | **Resolved / Unified** | `backend/rules/multi_goal.py`<br>`backend/engines/orchestration/engine.py` | Unified to single integer rank standard (`priority_rank`), eliminating conflicting text priority maps. |
| 15 | Funding status vocabulary | **Documented / Mapped** | `backend/models/defined_goal.py`<br>`backend/engines/allocation/models.py` | DefinedGoal uses user-facing statuses (`Shortfall`, `On Track`), while internal allocation engine computes programmatic status. |
| 16 | Feasibility status vocabulary | **Documented / Mapped** | `backend/models/strategy.py`<br>`backend/engines/allocation/models.py` | Feasibility outcomes aligned between strategy engine and allocation models. |
| 17 | `GoalEvaluationInput` vs `GoalAllocationResult` | **Documented Contract** | `backend/engines/orchestration/models.py`<br>`backend/engines/allocation/models.py` | Distinct boundaries maintained between evaluation inputs and final allocation results. |
| 18 | Goal taxonomy aliases | **Resolved / Unified** | `backend/rules/goals.py` | Strict 10 canonical goal types enforced without redirects to `others`. |
| 19 | Duplicate dynamic-goal migration | **Resolved / Removed** | `frontend/supabase/migrations/007_dynamic_goal_details.sql` | Deleted redundant duplicate migration `007_dynamic_goal_details.sql`. |
| 20 | `goal_funding` compatibility field | **Active Contract** | `backend/services/goal_report_service.py`<br>`backend/schemas/strategy.py` | Required by Goal Strategy Report PDF structure and reporting models. |
| 21 | `goal_context` compatibility field | **Active Contract** | `backend/services/goal_report_service.py`<br>`backend/schemas/strategy.py` | Required by Goal Strategy Report PDF structure and reporting models. |
| 22 | `solvency_ratio` | **Resolved / Removed** | `backend/rules/moneywheel.py` | Removed from MoneyWheel rule definitions. |
| 23 | `strat-cap-preservation` | **Active Alias** | `backend/library/strategies/registry.py`<br>`backend/rules/strategy_decision.py` | Maintained for backward compatibility with decision rules and persisted runs. |
| 24 | Legacy architecture IDs | **Active Mapping** | `backend/services/strategy_service.py` | Deserialization mapping retained to upgrade historical database records. |
| 25 | Legacy MoneyWheel ratio keys | **Resolved / Removed** | `backend/api/moneywheel.py`<br>`backend/tests/test_moneywheel_api.py` | Normalization removed; API serves exact 9 canonical ratios. |
| 26 | Legacy planning-unit localStorage key | **Resolved / Removed** | `frontend/lib/api/client.ts` | Removed `planvesto_planning_unit_id` fallback; standardizes on `planvesto-planning-unit-id`. |
| 27 | Legacy retirement PDF route | **Active Route** | `backend/api/strategy.py`<br>`frontend/lib/api/strategy.ts` | Canonical forwarding route to `GoalReportService().generate_pdf()`. |
| 28 | `MoneyWheelEngine` public import alias | **Resolved / Removed** | `backend/engines/moneywheel/engine.py` | Removed alias; codebase strictly uses `MoneywheelEngine`. |
| 29 | Legacy constraint model exports | **Resolved / Cleaned** | `backend/engines/constraints/__init__.py` | Cleaned up export classifications. |
| 30 | `GoalPriorityLevel` duplicated type definitions | **Resolved / Unified** | `backend/rules/goals.py`<br>`backend/engines/allocation/models.py` | Canonical type unified in `rules.goals`. |
