from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.financial_state import router as financial_state_router
from api.goals import router as goals_router
from api.strategy import router as strategy_router
from api.strategy_approval import router as strategy_approval_router
from api.strategy_edit import router as strategy_edit_router
from api.action_plan import router as action_plan_router
from api.moneywheel import router as moneywheel_router
from api.orchestration import router as orchestration_router

app = FastAPI(title="Planvesto Backend", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://planvesto.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(financial_state_router)
app.include_router(goals_router)
app.include_router(strategy_router)
app.include_router(strategy_approval_router)
app.include_router(strategy_edit_router)
app.include_router(action_plan_router)
app.include_router(moneywheel_router)
app.include_router(orchestration_router)

@app.get("/")
def root():
    return {"service": "Planvesto Backend", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
