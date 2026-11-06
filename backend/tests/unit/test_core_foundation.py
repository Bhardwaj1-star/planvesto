"""Unit tests for Core layer: settings, exceptions, and logging."""

import os
import pytest
from app.core.settings import Settings, parse_cors_origins
from app.core.exceptions import (
    AppException,
    ConfigurationError,
    AuthenticationError,
    AuthorizationError,
    DatabaseConnectionError,
    ResourceNotFoundError,
)
from app.core.logging import get_logger, SafeFormatter
import logging


def test_cors_origins_parsing_valid():
    raw = "http://localhost:3000, https://planvesto.com"
    origins = parse_cors_origins(raw)
    assert origins == ["http://localhost:3000", "https://planvesto.com"]


def test_cors_origins_wildcard_rejection():
    with pytest.raises(ValueError, match="must not contain wildcard"):
        parse_cors_origins("http://localhost:3000,*")


def test_cors_origins_empty_fallback():
    origins = parse_cors_origins("")
    assert len(origins) >= 1
    assert "http://localhost:3000" in origins


def test_settings_load_defaults():
    settings = Settings()
    assert settings.api_version == "2.0.0"
    assert "Planvesto" in settings.app_title
    assert isinstance(settings.cors_allowed_origins, list)


def test_exception_hierarchy_and_codes():
    auth_err = AuthenticationError("Token expired")
    assert auth_err.code == "AUTHENTICATION_REQUIRED"
    assert auth_err.message == "Token expired"
    assert isinstance(auth_err, AppException)

    authz_err = AuthorizationError("Forbidden")
    assert authz_err.code == "PERMISSION_DENIED"
    assert isinstance(authz_err, AppException)

    db_err = DatabaseConnectionError("Cannot connect")
    assert db_err.code == "DATABASE_CONNECTION_ERROR"
    assert isinstance(db_err, AppException)

    not_found_err = ResourceNotFoundError("Goal missing")
    assert not_found_err.code == "NOT_FOUND"


def test_safe_logging_masks_secrets():
    formatter = SafeFormatter("%(message)s")
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Request with Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 and secret=supersecret123",
        args=(),
        exc_info=None,
    )
    formatted = formatter.format(record)
    assert "Bearer [REDACTED]" in formatted
    assert "eyJhbGci" not in formatted
    assert "secret=[REDACTED]" in formatted
    assert "supersecret123" not in formatted
