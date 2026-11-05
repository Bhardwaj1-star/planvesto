from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.financial_state.financial_state import router as financial_state_router
from api.goal_planner.goals import router as goals_router
from api.shared.dashboard import router as dashboard_router
from api.goal_planner.goal_funding.goal_funding import router as goal_funding_router
from api.goal_planner.financial_plan import router as financial_plan_router
from api.action_plan.action_plan import router as action_plan_router
from api.moneywheel.moneywheel import router as moneywheel_router
from api.goal_planner.orchestration import router as orchestration_router
from api.goal_planner.goal_basket import router as goal_basket_router
from api.goal_planner.basket_report import router as basket_report_router
from api.diary.diary import router as diary_router
from api.investor_assessment.profile import router as profile_router
from api.financial_health_protection.insurance import router as insurance_router
from api.reports.summary_report import router as summary_report_router  # Added Summary Report router
from config.settings import CORS_ALLOWED_ORIGINS

app = FastAPI(title="Planvesto Backend", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(financial_state_router)
app.include_router(goals_router)
app.include_router(dashboard_router)
app.include_router(goal_funding_router)
app.include_router(financial_plan_router)
app.include_router(action_plan_router)
app.include_router(moneywheel_router)
app.include_router(orchestration_router)
app.include_router(goal_basket_router)
app.include_router(basket_report_router)
app.include_router(diary_router)
app.include_router(profile_router)
app.include_router(insurance_router)
app.include_router(summary_report_router)  # Added Summary Report router

@app.get("/")
def root():
    return {"service": "Planvesto Backend", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
