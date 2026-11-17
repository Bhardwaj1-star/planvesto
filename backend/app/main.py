"""
main.py
PlanVesto Backend — Single Composition Root

Non-negotiable invariants:
1. One modular monolith composition root.
2. Structured errors and request tracing without leaking secrets or stack traces.
3. Health and readiness endpoints for container/platform orchestrators.
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.errors import AppBaseException
from app.core.logging import configure_logging, get_logger
from app.api.router import api_router

logger = get_logger("planvesto.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(level=10 if settings.DEBUG else 20)
    logger.info(f"Starting {settings.APP_NAME} in [{settings.ENVIRONMENT}] mode.")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}.")


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="PlanVesto - Investor-First Financial Decision System API",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"^https:\/\/.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppBaseException)
async def app_exception_handler(request: Request, exc: AppBaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    if exc.code == "UNAUTHORIZED":
        status_code = status.HTTP_401_UNAUTHORIZED
    elif exc.code == "ENTITY_NOT_FOUND":
        status_code = status.HTTP_404_NOT_FOUND
    elif exc.code == "CONFLICT":
        status_code = status.HTTP_409_CONFLICT

    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


@app.get("/health", tags=["System"])
async def health_check():
    """Liveness probe: verifies process is alive and responding."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/ready", tags=["System"])
async def readiness_check():
    """Readiness probe: verifies service is ready to receive requests."""
    return {
        "status": "ready",
        "app": settings.APP_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# Mount API routers
app.include_router(api_router)
