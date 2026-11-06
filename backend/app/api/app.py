"""FastAPI Application Factory."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.settings import get_settings
from app.core.exceptions import (
    AppException,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    DatabaseConnectionError,
)
from app.core.logging import get_logger
from app.api.routers.health import router as health_router

logger = get_logger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    application = FastAPI(
        title=settings.app_title,
        version=settings.api_version,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS configuration
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    # Global Exception Handlers
    @application.exception_handler(AuthenticationError)
    async def auth_exception_handler(request: Request, exc: AuthenticationError):
        return JSONResponse(status_code=401, content={"detail": exc.message, "code": exc.code})

    @application.exception_handler(AuthorizationError)
    async def authz_exception_handler(request: Request, exc: AuthorizationError):
        return JSONResponse(status_code=403, content={"detail": exc.message, "code": exc.code})

    @application.exception_handler(ResourceNotFoundError)
    async def not_found_exception_handler(request: Request, exc: ResourceNotFoundError):
        return JSONResponse(status_code=404, content={"detail": exc.message, "code": exc.code})

    @application.exception_handler(DatabaseConnectionError)
    async def db_exception_handler(request: Request, exc: DatabaseConnectionError):
        return JSONResponse(status_code=503, content={"detail": exc.message, "code": exc.code})

    @application.exception_handler(AppException)
    async def general_app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(status_code=400, content={"detail": exc.message, "code": exc.code})

    # Register Routers
    application.include_router(health_router)

    return application
