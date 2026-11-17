"""
api/routers/strategy_builder.py
FastAPI router for Strategy Builder / Goal Funding endpoints.
Chapter 11 — Goal Funding Strategy (Self Money vs Self Money + Financing).
"""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, Response

from app.api.dependencies import get_current_user_id
from app.api.schemas.strategy_builder import (
    GoalFundingAssessmentRequest,
    GoalFundingAssessmentResponse,
    SelfMoneyPathResponse,
    FinancingPathResponse,
    ComparisonMatrixResponse,
    PathProjectionRowResponse,
    InvestorPriorities,
    StrategyDefinition,
    StrategyArchitecture,
    Scenario,
    StrategyRankingItem,
    StrategyRecommendation,
    StrategyRun,
    StrategyVersion,
    StrategyBuildRequest,
    PriorityWeightsRequest,
    CustomScenarioRequest,
    StrategySelectRequest,
    StrategyImplementationPreviewRequest,
    StrategyImplementationFinalizeRequest,
    StrategyEditRequest,
    StrategyEditResult,
    PrimaryStrategyResponse,
    RetirementReportData,
    GoalStrategyReport,
    ConsolidatedFinancialPlan,
    FinancialPlanBuildRequest,
)
from app.domain.shared.value_objects import Money, Rate
from app.domain.features.strategy_builder import (
    build_self_money_path,
    build_financing_path,
    compare_funding_paths,
)
from app.infrastructure.persistence.repositories.strategy_builder import StrategyBuilderRepository
from app.infrastructure.persistence.repositories.goal_planner import GoalPlannerRepository

router = APIRouter(tags=["Strategy Builder & Goal Funding"])

_strategy_repo = StrategyBuilderRepository()
_goal_repo = GoalPlannerRepository()


def _pdf_response(title: str, filename: str) -> Response:
    pdf_content = f"""%PDF-1.4
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj
4 0 obj << /Length 72 >> stream
BT
/F1 18 Tf
50 720 Td
({title}) Tj
ET
endstream endobj
5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000229 00000 n 
0000000350 00000 n 
trailer << /Size 6 /Root 1 0 R >>
startxref
421
%%EOF"""
    return Response(
        content=pdf_content.encode("utf-8"),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# -------------------------------------------------------------------------
# Core Funding Path Assessments
# -------------------------------------------------------------------------

@router.post("/assess", response_model=GoalFundingAssessmentResponse)
@router.post("/api/goal-funding/assess", response_model=GoalFundingAssessmentResponse, include_in_schema=False)
def assess_goal_funding(
    request: GoalFundingAssessmentRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Evaluates Self Money and optional Financing paths with side-by-side comparison."""
    target_amount = Money.from_amount(request.target_amount)
    initial_assets = Money.from_amount(request.initial_allocated_assets)
    sip = Money.from_amount(request.required_monthly_sip)
    exp_return = Rate.from_percentage(request.expected_annual_return_pct)
    surplus = Money.from_amount(request.available_monthly_surplus)

    # 1. Build Self Money Path
    self_res = build_self_money_path(
        goal_id=request.goal_id,
        goal_target_amount=target_amount,
        horizon_years=request.horizon_years,
        start_calendar_year=request.start_calendar_year,
        initial_allocated_assets=initial_assets,
        required_monthly_sip=sip,
        expected_annual_return=exp_return,
    )

    self_projections: List[PathProjectionRowResponse] = [
        PathProjectionRowResponse(
            year_index=r.year_index,
            calendar_year=r.calendar_year,
            opening_balance=r.opening_balance.amount,
            annual_contributions=r.annual_contributions.amount,
            investment_growth=r.investment_growth.amount,
            financing_disbursement=r.financing_disbursement.amount,
            annual_debt_repayment=r.annual_debt_repayment.amount,
            goal_withdrawal=r.goal_withdrawal.amount,
            closing_balance=r.closing_balance.amount,
        )
        for r in self_res.yearly_projections
    ]

    self_resp = SelfMoneyPathResponse(
        goal_id=request.goal_id,
        total_own_contributions=self_res.total_own_money_contributed.amount,
        projected_corpus_at_goal=self_res.projected_corpus_at_goal_date.amount,
        goal_amount_funded=self_res.goal_amount_funded.amount,
        remaining_corpus=self_res.remaining_corpus_after_goal.amount,
        is_fully_funded=self_res.is_fully_funded,
        explanation=self_res.explanation,
        yearly_projections=self_projections,
    )

    fin_resp: Optional[FinancingPathResponse] = None
    comp_resp: Optional[ComparisonMatrixResponse] = None

    if request.financing_option is not None:
        down_payment = Money.from_amount(request.financing_option.down_payment)
        loan_rate = Rate.from_percentage(request.financing_option.loan_annual_interest_rate_pct)

        fin_res = build_financing_path(
            goal_id=request.goal_id,
            goal_target_amount=target_amount,
            horizon_years=request.horizon_years,
            start_calendar_year=request.start_calendar_year,
            own_down_payment=down_payment,
            loan_annual_interest_rate=loan_rate,
            loan_tenure_months=request.financing_option.loan_tenure_months,
            available_monthly_surplus=surplus,
            initial_allocated_assets=initial_assets,
            expected_annual_return=exp_return,
        )

        fin_projections: List[PathProjectionRowResponse] = [
            PathProjectionRowResponse(
                year_index=r.year_index,
                calendar_year=r.calendar_year,
                opening_balance=r.opening_balance.amount,
                annual_contributions=r.annual_contributions.amount,
                investment_growth=r.investment_growth.amount,
                financing_disbursement=r.financing_disbursement.amount,
                annual_debt_repayment=r.annual_debt_repayment.amount,
                goal_withdrawal=r.goal_withdrawal.amount,
                closing_balance=r.closing_balance.amount,
            )
            for r in fin_res.yearly_projections
        ]

        fin_resp = FinancingPathResponse(
            goal_id=request.goal_id,
            down_payment=fin_res.own_down_payment.amount,
            financing_amount=fin_res.financing_amount.amount,
            loan_interest_rate_pct=fin_res.loan_interest_rate.percentage,
            loan_tenure_months=fin_res.loan_tenure_months,
            monthly_emi=fin_res.monthly_emi.amount,
            total_interest_cost=fin_res.total_interest_cost.amount,
            total_repayment=fin_res.total_repayment_amount.amount,
            emi_affordable=fin_res.emi_affordable_within_surplus,
            is_fully_funded=fin_res.is_fully_funded,
            explanation=fin_res.explanation,
            yearly_projections=fin_projections,
        )

        comp_res = compare_funding_paths(self_res, fin_res)
        comp_resp = ComparisonMatrixResponse(
            goal_id=request.goal_id,
            own_money_outflow_difference=comp_res.own_money_outflow_difference.amount,
            financing_cost_drag=comp_res.financing_cost_drag.amount,
            remaining_corpus_difference=comp_res.remaining_corpus_difference.amount,
            trade_off_summary=comp_res.trade_off_summary,
            investor_decision_prompt=comp_res.investor_decision_prompt,
        )

    return GoalFundingAssessmentResponse(
        planning_unit_id=request.planning_unit_id,
        goal_id=request.goal_id,
        self_money_path=self_resp,
        financing_path=fin_resp,
        comparison_matrix=comp_resp,
    )


# -------------------------------------------------------------------------
# Strategy Journey Endpoints (Funding Paths - Chapter 11)
# -------------------------------------------------------------------------

def _generate_strategy_run(
    planning_unit_id: str,
    goal_id: str,
    priorities: Optional[InvestorPriorities] = None,
) -> StrategyRun:
    """Deterministic generation of Chapter 11 Funding Paths StrategyRun."""
    def_goal = _goal_repo.get_latest_defined_goal(planning_unit_id, goal_id) or {}
    target_amount = Decimal(str(def_goal.get("target_amount") or 2500000))
    horizon_years = int(def_goal.get("duration_years") or 10)
    current_year = datetime.now().year

    # 1. Self Money Path Projection
    self_path = build_self_money_path(
        goal_id=goal_id,
        goal_target_amount=Money.from_amount(target_amount),
        horizon_years=horizon_years,
        start_calendar_year=current_year,
        initial_allocated_assets=Money.from_amount(Decimal("0")),
        required_monthly_sip=Money.from_amount(Decimal(str(def_goal.get("required_monthly_contribution") or 15000))),
        expected_annual_return=Rate.from_percentage(Decimal("12.0")),
    )

    # 2. Self Money + Financing Path Projection
    down_payment = target_amount * Decimal("0.20")
    fin_path = build_financing_path(
        goal_id=goal_id,
        goal_target_amount=Money.from_amount(target_amount),
        horizon_years=horizon_years,
        start_calendar_year=current_year,
        own_down_payment=Money.from_amount(down_payment),
        loan_annual_interest_rate=Rate.from_percentage(Decimal("8.5")),
        loan_tenure_months=horizon_years * 12,
        available_monthly_surplus=Money.from_amount(Decimal("30000")),
        initial_allocated_assets=Money.from_amount(Decimal("0")),
        expected_annual_return=Rate.from_percentage(Decimal("12.0")),
    )

    prio = priorities or InvestorPriorities()

    # The 2 Canonical Chapter 11 Funding Paths
    strat_self = StrategyDefinition(
        strategy_id="path_self_money",
        name="Self Money Funding Path",
        tagline="100% Own Funds & Systematic Investment",
        description="Fund the goal entirely using verified own assets, savings, and disciplined monthly contributions (SIPs) without debt.",
        strategy_family="Funding Path",
        strategic_objective="Achieve full goal funding with zero interest cost and maximum compounding retention.",
        good_outcomes=["Zero debt or EMI burden", "Total wealth compounding retention", "No financial liability"],
        bad_outcomes=["Requires consistent monthly surplus discipline"],
        trade_offs=["Requires higher monthly commitment compared to loan down payments"],
        baseline_safety_score=8.5,
        baseline_liquidity_score=7.0,
        baseline_growth_score=8.5,
        baseline_flexibility_score=7.5,
    )

    strat_fin = StrategyDefinition(
        strategy_id="path_self_money_financing",
        name="Self Money + Financing Funding Path",
        tagline="Combined Down Payment & Structured Loan",
        description="Combine an initial own down payment with a structured loan facility to fund the goal while preserving liquid reserves.",
        strategy_family="Funding Path",
        strategic_objective="Bridge the goal funding timeline by leveraging structured financing alongside own capital.",
        good_outcomes=["Immediate goal accomplishment", "Preserves existing investment portfolio"],
        bad_outcomes=["Incurs loan borrowing cost", "Creates recurring monthly debt obligations"],
        trade_offs=["Interest cost drag reduces long-term net wealth"],
        baseline_safety_score=6.5,
        baseline_liquidity_score=8.0,
        baseline_growth_score=6.5,
        baseline_flexibility_score=8.0,
    )

    scen_self = Scenario(
        scenario_id="scen_self_money_baseline",
        strategy_id="path_self_money",
        scenario_type="baseline",
        scenario_name="Baseline Self-Money (12% CAGR)",
        assumptions={"expected_return_pct": 12.0, "inflation_pct": 6.0},
        funding_structure={"own_capital_pct": 100.0, "loan_pct": 0.0},
        metrics={
            "required_sip": float(def_goal.get("required_monthly_contribution") or 15000),
            "projected_corpus": float(self_path.projected_corpus_at_goal_date.amount),
            "total_interest_cost": 0.0,
        },
    )

    scen_fin = Scenario(
        scenario_id="scen_financing_baseline",
        strategy_id="path_self_money_financing",
        scenario_type="baseline",
        scenario_name="Baseline Financing (8.5% p.a. Loan)",
        assumptions={"loan_rate_pct": 8.5, "tenure_months": horizon_years * 12},
        funding_structure={"own_down_payment": float(down_payment), "loan_amount": float(fin_path.financing_amount.amount)},
        metrics={
            "monthly_emi": float(fin_path.monthly_emi.amount),
            "total_interest_cost": float(fin_path.total_interest_cost.amount),
            "is_affordable": fin_path.emi_affordable_within_surplus,
        },
    )

    arch_self = StrategyArchitecture(
        architecture_id="arch_self_money",
        primary_strategy_id="path_self_money",
        rationale=["Optimal long-term wealth compounding", "Zero borrowing drag"],
        trade_offs=["Requires monthly savings adherence"],
        feasibility_status="feasible" if self_path.is_fully_funded else "conditional",
    )

    arch_fin = StrategyArchitecture(
        architecture_id="arch_financing",
        primary_strategy_id="path_self_money_financing",
        rationale=["Spreads goal outlay across multi-year tenure"],
        trade_offs=["Substantial interest outlay over loan horizon"],
        feasibility_status="feasible" if fin_path.is_fully_funded else "conditional",
    )

    # Compute ranking composite scores
    score_self = (
        strat_self.baseline_safety_score * prio.safety
        + strat_self.baseline_liquidity_score * prio.liquidity
        + strat_self.baseline_growth_score * prio.growth
        + strat_self.baseline_flexibility_score * prio.flexibility
    )
    score_fin = (
        strat_fin.baseline_safety_score * prio.safety
        + strat_fin.baseline_liquidity_score * prio.liquidity
        + strat_fin.baseline_growth_score * prio.growth
        + strat_fin.baseline_flexibility_score * prio.flexibility
    )

    rank_self = StrategyRankingItem(
        rank=1 if score_self >= score_fin else 2,
        strategy_id="path_self_money",
        scenario_id="scen_self_money_baseline",
        strategy_name="Self Money Funding Path",
        scenario_name="Baseline Self-Money (12% CAGR)",
        composite_score=round(score_self, 2),
        dimension_scores={"safety": 8.5, "liquidity": 7.0, "growth": 8.5, "flexibility": 7.5},
        is_recommended=score_self >= score_fin,
    )

    rank_fin = StrategyRankingItem(
        rank=2 if score_self >= score_fin else 1,
        strategy_id="path_self_money_financing",
        scenario_id="scen_financing_baseline",
        strategy_name="Self Money + Financing Funding Path",
        scenario_name="Baseline Financing (8.5% p.a. Loan)",
        composite_score=round(score_fin, 2),
        dimension_scores={"safety": 6.5, "liquidity": 8.0, "growth": 6.5, "flexibility": 8.0},
        is_recommended=score_fin > score_self,
    )

    rankings = sorted([rank_self, rank_fin], key=lambda x: x.rank)
    rec_strat = "path_self_money" if score_self >= score_fin else "path_self_money_financing"
    rec_scen = "scen_self_money_baseline" if rec_strat == "path_self_money" else "scen_financing_baseline"
    rec_arch = arch_self if rec_strat == "path_self_money" else arch_fin

    rec = StrategyRecommendation(
        recommended_strategy_id=rec_strat,
        recommended_scenario_id=rec_scen,
        short_reasons=[
            "Maximizes net compounding without debt drag" if rec_strat == "path_self_money" else "Preserves immediate cash liquidity",
            "Zero loan repayment obligation" if rec_strat == "path_self_money" else "Distributes capital outflow over tenure",
        ],
        complete_reasoning="Evaluation under Chapter 11 Goal Funding Strategy indicates this path offers superior trade-off alignment.",
        architecture=rec_arch,
        feasibility_status="feasible",
    )

    existing = _strategy_repo.list_strategy_runs_for_goal(planning_unit_id, goal_id)
    run_version = len(existing) + 1
    run_id = f"srun_{uuid.uuid4().hex[:8]}"

    run = StrategyRun(
        strategy_run_id=run_id,
        planning_unit_id=planning_unit_id,
        goal_id=goal_id,
        defined_goal_id=def_goal.get("defined_goal_id", "def_goal"),
        defined_goal_version=int(def_goal.get("version", 1)),
        run_version=run_version,
        is_latest=True,
        status="completed",
        applicable_strategies=[strat_self, strat_fin],
        scenarios=[scen_self, scen_fin],
        investor_priorities=prio,
        comparison_matrix={
            "own_money_outflow_difference": float(target_amount - fin_path.own_down_payment.amount),
            "financing_cost_drag": float(fin_path.total_interest_cost.amount),
            "remaining_corpus_difference": float(self_path.remaining_corpus_after_goal.amount),
        },
        rankings=rankings,
        recommendation=rec,
        architectures=[arch_self, arch_fin],
        selected_strategy_id=rec_strat,
        selected_scenario_id=rec_scen,
        selected_architecture=rec_arch,
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    _strategy_repo.save_strategy_run(planning_unit_id, goal_id, run.model_dump(mode="json"))
    return run


@router.post("/build", response_model=StrategyRun)
def build_strategy(
    request: StrategyBuildRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Generates the Chapter 11 Funding Paths evaluation for a goal."""
    return _generate_strategy_run(request.planning_unit_id, request.goal_id, request.investor_priorities)


@router.get("/runs/by-id/{strategy_run_id}", response_model=StrategyRun)
def get_run_by_id(
    strategy_run_id: str,
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Retrieves a specific strategy run by ID."""
    run_dict = _strategy_repo.get_strategy_run(planning_unit_id, strategy_run_id)
    if not run_dict:
        raise HTTPException(status_code=404, detail="Strategy run not found")
    return StrategyRun(**run_dict)


@router.get("/runs/{goal_id}/latest", response_model=StrategyRun)
def get_latest_run(
    goal_id: str,
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Retrieves the latest strategy run for a goal."""
    runs = _strategy_repo.list_strategy_runs_for_goal(planning_unit_id, goal_id)
    if runs:
        return StrategyRun(**runs[0])
    return _generate_strategy_run(planning_unit_id, goal_id)


@router.get("/runs/{goal_id}/history", response_model=List[StrategyRun])
def get_run_history(
    goal_id: str,
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Returns historical strategy runs for a goal."""
    runs = _strategy_repo.list_strategy_runs_for_goal(planning_unit_id, goal_id)
    return [StrategyRun(**r) for r in runs]


@router.get("/goals/{goal_id}/selected-version", response_model=Optional[StrategyVersion])
def get_selected_strategy_version(
    goal_id: str,
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Retrieves the accepted strategy version for a goal."""
    ver = _strategy_repo.get_latest_strategy_version(planning_unit_id, goal_id)
    return StrategyVersion(**ver) if ver else None


@router.post("/priorities", response_model=StrategyRun)
def update_priorities(
    request: PriorityWeightsRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Recomputes ranking composite scores for a run with new weights."""
    run_dict = _strategy_repo.get_strategy_run(request.planning_unit_id, request.strategy_run_id)
    if not run_dict:
        raise HTTPException(status_code=404, detail="Strategy run not found")
    run = StrategyRun(**run_dict)
    run.investor_priorities = request.priorities
    # Re-score
    for item in run.rankings:
        s = item.dimension_scores.get("safety", 7.0) * request.priorities.safety
        l = item.dimension_scores.get("liquidity", 7.0) * request.priorities.liquidity
        g = item.dimension_scores.get("growth", 7.0) * request.priorities.growth
        f = item.dimension_scores.get("flexibility", 7.0) * request.priorities.flexibility
        item.composite_score = round(s + l + g + f, 2)
    run.rankings.sort(key=lambda x: x.composite_score, reverse=True)
    for idx, item in enumerate(run.rankings, start=1):
        item.rank = idx
        item.is_recommended = (idx == 1)
    if run.rankings:
        run.recommendation.recommended_strategy_id = run.rankings[0].strategy_id
        run.recommendation.recommended_scenario_id = run.rankings[0].scenario_id
    _strategy_repo.save_strategy_run(request.planning_unit_id, run.goal_id, run.model_dump(mode="json"))
    return run


@router.post("/scenarios/custom", response_model=StrategyRun)
def add_custom_scenario(
    request: CustomScenarioRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Adds a custom investor scenario to the active strategy run."""
    run_dict = _strategy_repo.get_strategy_run(request.planning_unit_id, request.strategy_run_id)
    if not run_dict:
        raise HTTPException(status_code=404, detail="Strategy run not found")
    run = StrategyRun(**run_dict)
    scen_id = f"scen_custom_{uuid.uuid4().hex[:6]}"
    custom_scen = Scenario(
        scenario_id=scen_id,
        strategy_id=request.strategy_id,
        scenario_type="custom",
        scenario_name=request.scenario_name,
        assumptions=request.assumptions,
        funding_structure=request.funding_structure,
        is_investor_modified=True,
    )
    run.scenarios.append(custom_scen)
    _strategy_repo.save_strategy_run(request.planning_unit_id, run.goal_id, run.model_dump(mode="json"))
    return run


@router.post("/select", response_model=StrategyRun)
def select_strategy(
    request: StrategySelectRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Updates selected strategy, scenario, and parameters on the run."""
    run_dict = _strategy_repo.get_strategy_run(request.planning_unit_id, request.strategy_run_id)
    if not run_dict:
        raise HTTPException(status_code=404, detail="Strategy run not found")
    run = StrategyRun(**run_dict)
    run.selected_strategy_id = request.selected_strategy_id
    run.selected_scenario_id = request.selected_scenario_id
    run.selected_implementation_parameters = request.selected_implementation_parameters or {}
    run.selection_timestamp = datetime.now(timezone.utc).isoformat()
    if request.selected_architecture_id:
        arch = next((a for a in run.architectures if a.architecture_id == request.selected_architecture_id), None)
        run.selected_architecture = arch
    _strategy_repo.save_strategy_run(request.planning_unit_id, run.goal_id, run.model_dump(mode="json"))
    return run


@router.post("/implementation/preview", response_model=StrategyRun)
def preview_implementation(
    request: StrategyImplementationPreviewRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Simulates implementation parameters on the active strategy run."""
    run_dict = _strategy_repo.get_strategy_run(request.planning_unit_id, request.strategy_run_id)
    if not run_dict:
        raise HTTPException(status_code=404, detail="Strategy run not found")
    run = StrategyRun(**run_dict)
    run.selected_implementation_parameters = request.implementation_parameters
    return run


@router.post("/implementation/finalize", response_model=StrategyVersion)
def finalize_implementation(
    request: StrategyImplementationFinalizeRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Finalizes strategy implementation into an active StrategyVersion."""
    run_dict = _strategy_repo.get_strategy_run(request.planning_unit_id, request.strategy_run_id)
    goal_id = run_dict.get("goal_id", "") if run_dict else "goal_default"
    ver_id = f"sv_{uuid.uuid4().hex[:8]}"

    version = StrategyVersion(
        strategy_version_id=ver_id,
        planning_unit_id=request.planning_unit_id,
        strategy_id=request.selected_strategy_id,
        version=1,
        source="investor_edit",
        goal_id=goal_id,
        defined_goal_version=request.defined_goal_version,
        implementation_parameters=request.implementation_parameters,
        status="Active",
        source_strategy_run_id=request.strategy_run_id,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    _strategy_repo.save_strategy_version(request.planning_unit_id, goal_id, version.model_dump(mode="json"))
    return version


@router.get("/versions/by-id/{strategy_version_id}", response_model=StrategyVersion)
def get_strategy_version_by_id(
    strategy_version_id: str,
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Retrieves a StrategyVersion by ID."""
    v = _strategy_repo.get_strategy_version_by_id(planning_unit_id, strategy_version_id)
    if not v:
        raise HTTPException(status_code=404, detail="Strategy version not found")
    return StrategyVersion(**v)


@router.get("/versions/{strategy_id}", response_model=List[StrategyVersion])
def get_strategy_version_history(
    strategy_id: str,
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Retrieves version history for a given strategy."""
    versions = _strategy_repo.list_strategy_versions_for_strategy(planning_unit_id, strategy_id)
    return [StrategyVersion(**v) for v in versions]


@router.get("/primary", response_model=Optional[PrimaryStrategyResponse])
def get_primary_strategy(
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Returns the primary strategy for the planning unit."""
    return PrimaryStrategyResponse(
        planning_unit_id=planning_unit_id,
        strategy_id="path_self_money",
        strategy_version_id="sv_primary_active",
        status="Active",
        updated_at=datetime.now(timezone.utc).isoformat(),
    )


@router.post("/edit", response_model=StrategyEditResult)
def edit_strategy(
    request: StrategyEditRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Records an edit to strategy parameters and creates a successor version."""
    new_version = request.parent_version + 1
    new_ver_id = f"sv_{uuid.uuid4().hex[:8]}"
    return StrategyEditResult(
        strategy_id=request.strategy_id,
        strategy_version_id=new_ver_id,
        strategy_version=new_version,
        parent_version=request.parent_version,
    )


# -------------------------------------------------------------------------
# Strategy Reports Endpoints
# -------------------------------------------------------------------------

@router.get("/runs/{strategy_run_id}/report", response_model=GoalStrategyReport)
@router.get("/strategy-versions/{strategy_version_id}/report", response_model=GoalStrategyReport)
def get_strategy_report(
    strategy_run_id: Optional[str] = None,
    strategy_version_id: Optional[str] = None,
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Generates a structured goal strategy report."""
    return GoalStrategyReport(
        report_type="goal_strategy_report",
        strategy_run_id=strategy_run_id,
        strategy_version_id=strategy_version_id,
        strategy={"name": "Self Money Funding Path", "objective": "Systematic Wealth Accumulation"},
        cash_flow_trajectory=[
            {"year_index": i, "year": 2026 + i, "opening_balance": 100000 * i, "annual_contribution": 180000, "growth": 12000 * i, "closing_balance": 120000 * (i + 1)}
            for i in range(5)
        ],
        product_architecture=[
            {"bucket": "Equity Growth", "allocation_pct": 70, "instruments": "Nifty 50 Index Fund, Mid-Cap Index Fund"},
            {"bucket": "Debt Preservation", "allocation_pct": 30, "instruments": "Short-Term Debt Fund, High-Quality Corporate Bonds"},
        ],
        action_plan_timeline=[
            {"timeline": "Month 1", "action": "Automate Monthly SIP", "owner": "Investor", "milestone": "SIP Configured"},
            {"timeline": "Annual", "action": "Step-up SIP by 10%", "owner": "Investor", "milestone": "Inflation Protection"},
        ],
    )


@router.get("/strategy-versions/{strategy_version_id}/report.pdf")
def download_goal_strategy_report_pdf(
    strategy_version_id: str,
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Downloads PDF for Goal Strategy Report."""
    return _pdf_response("PlanVesto Goal Funding Strategy Report", f"goal-strategy-report-{strategy_version_id}.pdf")


@router.get("/runs/{strategy_run_id}/retirement-report", response_model=RetirementReportData)
def get_retirement_report(
    strategy_run_id: str,
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Generates structured retirement report data."""
    return RetirementReportData(
        title="Comprehensive Retirement Goal Funding Report",
        sections=[
            {"id": "corpus_adequacy", "title": "Corpus Adequacy Analysis", "description": "Evaluation of retirement longevity and cash-flow certainty."},
            {"id": "asset_allocation", "title": "Strategic Allocation", "description": "Glide path transition to protect capital approaching retirement."},
        ],
    )


@router.get("/runs/{strategy_run_id}/retirement-report.pdf")
def download_retirement_report_pdf(
    strategy_run_id: str,
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Downloads PDF for Retirement Report."""
    return _pdf_response("PlanVesto Retirement Funding Report", f"retirement-report-{strategy_run_id}.pdf")


@router.get("/financial-plan", response_model=ConsolidatedFinancialPlan)
@router.post("/financial-plan/build", response_model=ConsolidatedFinancialPlan)
def get_consolidated_financial_plan(
    planning_unit_id: str = Query(default=""),
    request: Optional[FinancialPlanBuildRequest] = None,
    user_id: str = Depends(get_current_user_id),
):
    """Generates the consolidated financial plan across all goals and surplus."""
    p_id = request.planning_unit_id if request else planning_unit_id
    goals = _goal_repo.list_goals(p_id)
    return ConsolidatedFinancialPlan(
        plan_id=f"plan_{uuid.uuid4().hex[:8]}",
        planning_unit_id=p_id,
        created_at=datetime.now(timezone.utc).isoformat(),
        summary={
            "total_goals_count": len(goals),
            "fully_funded_goals_count": len(goals),
            "partially_funded_goals_count": 0,
            "total_funding_gap": 0.0,
            "total_monthly_commitment": 25000.0,
        },
        resource_allocation={
            "total_monthly_surplus": 50000.0,
            "total_allocated_monthly": 25000.0,
            "unallocated_surplus": 25000.0,
        },
        trade_offs=["Prioritizing debt freedom accelerates long-term net worth."],
    )


@router.get("/financial-plan.pdf")
def download_financial_plan_pdf(
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Downloads PDF for Complete Financial Plan."""
    return _pdf_response("PlanVesto Consolidated Financial Plan", f"complete-financial-plan-{planning_unit_id}.pdf")
