"""
core/config.py
PlanVesto backend application settings and environment validation.
"""

from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = "PlanVesto Backend"
    ENVIRONMENT: str = Field(default="development")  # development, testing, staging, production
    DEBUG: bool = Field(default=False)
    API_V1_PREFIX: str = "/api/v1"

    # CORS configuration
    CORS_ORIGINS: List[str] = [
        "https://planvesto.vercel.app",
        "https://planvesto.com",
        "https://www.planvesto.com",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # Database & Supabase settings (placeholders; verified during Phase 3)
    SUPABASE_URL: str = Field(default="")
    SUPABASE_ANON_KEY: str = Field(default="")
    SUPABASE_SERVICE_ROLE_KEY: str = Field(default="")
    DATABASE_URL: str = Field(default="postgresql://postgres:postgres@localhost:5432/planvesto")

    @property
    def supabase_url(self) -> str:
        return self.SUPABASE_URL

    @property
    def supabase_service_role_key(self) -> str:
        return self.SUPABASE_SERVICE_ROLE_KEY

    @property
    def cors_origins(self) -> List[str]:
        origins = set(self.CORS_ORIGINS)
        origins.update([
            "https://planvesto.vercel.app",
            "https://planvesto.com",
            "https://www.planvesto.com",
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ])
        import os
        legacy = os.getenv("CORS_ALLOWED_ORIGINS")
        if legacy:
            for item in legacy.split(","):
                if item.strip():
                    origins.add(item.strip().rstrip("/"))
        return list(origins)


settings = Settings()
