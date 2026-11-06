"""Configuration settings bridge preserving legacy exports."""

import os
from dotenv import load_dotenv
from app.core.settings import get_settings, parse_cors_origins

load_dotenv()

_settings = get_settings()

SUPABASE_URL = _settings.supabase_url
SUPABASE_SERVICE_ROLE_KEY = _settings.supabase_service_role_key

# Check for production / test runtime requirements if configured
if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    if os.getenv("ENVIRONMENT") == "production":
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be configured.")

CORS_ALLOWED_ORIGINS = _settings.cors_allowed_origins
if not CORS_ALLOWED_ORIGINS:
    raise RuntimeError("CORS_ALLOWED_ORIGINS must contain at least one explicit origin.")

__all__ = ["SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "CORS_ALLOWED_ORIGINS"]
