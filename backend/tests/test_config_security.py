import importlib

import pytest


def _load_settings(monkeypatch, **env):
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "test-service-role-key")
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    import config.settings as settings
    return importlib.reload(settings)


def test_cors_origins_are_explicit_and_parsed(monkeypatch):
    settings = _load_settings(
        monkeypatch,
        CORS_ALLOWED_ORIGINS="http://localhost:3000, https://planvesto.com/",
    )
    assert settings.CORS_ALLOWED_ORIGINS == [
        "http://localhost:3000",
        "https://planvesto.com",
    ]


def test_cors_wildcard_is_rejected(monkeypatch):
    with pytest.raises(RuntimeError, match="must not contain '\\*'"):
        _load_settings(monkeypatch, CORS_ALLOWED_ORIGINS="*")


def test_cors_empty_allowlist_is_rejected(monkeypatch):
    with pytest.raises(RuntimeError, match="at least one explicit origin"):
        _load_settings(monkeypatch, CORS_ALLOWED_ORIGINS=" ")
