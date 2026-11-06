"""Integration tests for Supabase client and persistence health checking."""

from unittest.mock import MagicMock, patch
import pytest
from app.infrastructure.providers.supabase.client import SupabaseClientFactory, get_supabase_client, set_supabase_client
from app.infrastructure.persistence.database import check_database_health
from app.core.exceptions import DatabaseConnectionError


def test_supabase_factory_raises_when_unconfigured():
    with patch("app.infrastructure.providers.supabase.client.get_settings") as mock_settings:
        mock_settings.return_value = MagicMock(supabase_url="", supabase_service_role_key="")
        with pytest.raises(DatabaseConnectionError, match="Cannot connect to Supabase"):
            SupabaseClientFactory.create()


def test_supabase_check_health_safe_probe():
    mock_client = MagicMock()
    mock_client.auth.get_session.return_value = None
    healthy = SupabaseClientFactory.check_health(mock_client)
    assert healthy is True


def test_database_health_reporting_connected():
    with patch("app.infrastructure.persistence.database.get_db_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.table.return_value.select.return_value.limit.return_value.execute.return_value = MagicMock(data=[])
        mock_get_client.return_value = mock_client

        health = check_database_health()
        assert health["connected"] is True
        assert health["provider"] == "supabase_postgresql"


def test_database_health_reporting_disconnected_graceful():
    with patch("app.infrastructure.persistence.database.get_db_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.table.return_value.select.return_value.limit.return_value.execute.side_effect = Exception("Connection timeout")
        mock_get_client.return_value = mock_client

        health = check_database_health()
        assert health["connected"] is False
        assert "Connection timeout" in health["error"]
