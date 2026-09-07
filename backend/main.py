from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.financial_state import router as financial_state_router

app = FastAPI(title="Planvesto Backend", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://planvesto.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(financial_state_router)

@app.get("/")
def root():
    return {"service": "Planvesto Backend", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
