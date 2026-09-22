import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be configured.")


def _parse_origins(raw: str | None) -> list[str]:
    """Parse a comma-separated CORS allowlist and reject wildcard origins."""
    values = [origin.strip().rstrip("/") for origin in (raw or "").split(",") if origin.strip()]
    if "*" in values:
        raise RuntimeError("CORS_ALLOWED_ORIGINS must not contain '*'.")
    return values


CORS_ALLOWED_ORIGINS = _parse_origins(
    os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,https://planvesto.com")
)
if not CORS_ALLOWED_ORIGINS:
    raise RuntimeError("CORS_ALLOWED_ORIGINS must contain at least one explicit origin.")
