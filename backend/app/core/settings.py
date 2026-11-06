import os
from functools import lru_cache
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


def parse_cors_origins(raw: str | None) -> List[str]:
    """Parse comma-separated CORS allowlist and reject wildcard origins."""
    values = [origin.strip().rstrip("/") for origin in (raw or "").split(",") if origin.strip()]
    if "*" in values:
        raise ValueError("CORS_ALLOWED_ORIGINS must not contain wildcard '*'.")
    if not values:
        # Fallback to safe defaults if none provided
        return ["http://localhost:3000", "https://planvesto.com"]
    return values


class Settings:
    """Typed runtime configuration loaded from environment."""

    def __init__(self) -> None:
        self.supabase_url: str = os.getenv("SUPABASE_URL", "")
        self.supabase_service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
        self.environment: str = os.getenv("ENVIRONMENT", "development")
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.api_version: str = "2.0.0"
        self.app_title: str = "Planvesto Backend"

        raw_cors = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,https://planvesto.com")
        self.cors_allowed_origins: List[str] = parse_cors_origins(raw_cors)

    def validate_for_production(self) -> None:
        """Validate that all mandatory credentials are present."""
        if not self.supabase_url or not self.supabase_service_role_key:
            raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be configured.")
        if not self.cors_allowed_origins:
            raise RuntimeError("CORS_ALLOWED_ORIGINS must contain at least one explicit origin.")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings singleton."""
    return Settings()
