from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.financial_state import router as financial_state_router
from api.goals import router as goals_router
from api.dashboard import router as dashboard_router
from api.strategy import router as strategy_router
from api.strategy_approval import router as strategy_approval_router
from api.strategy_edit import router as strategy_edit_router
from api.strategy_version import router as strategy_version_router
from api.action_plan import router as action_plan_router
from api.moneywheel import router as moneywheel_router
from api.orchestration import router as orchestration_router
from api.diary import router as diary_router
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
app.include_router(strategy_router)
app.include_router(strategy_approval_router)
app.include_router(strategy_edit_router)
app.include_router(strategy_version_router)
app.include_router(action_plan_router)
app.include_router(moneywheel_router)
app.include_router(orchestration_router)
app.include_router(diary_router)

@app.get("/")
def root():
    return {"service": "Planvesto Backend", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
