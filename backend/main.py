from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.strategy import router as strategy_router
from api.dashboard import router as dashboard_router


app = FastAPI(
    title="Planvesto Backend",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://planvesto.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(strategy_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {
        "service": "Planvesto Backend",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }