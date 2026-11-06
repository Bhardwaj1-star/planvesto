"""Unit tests for Security layer: authentication and authorization."""

from unittest.mock import MagicMock, patch
import pytest
from fastapi import HTTPException
from app.security.authentication import authenticate_request
from app.security.authorization import (
    verify_planning_unit_ownership,
    verify_resource_ownership,
    verify_investor_ownership,
    verify_goal_ownership,
    verify_assets_ownership,
)
from app.security.policies import AccessControlPolicy


def test_authenticate_request_missing_token_raises_401():
    with pytest.raises(HTTPException) as exc_info:
        authenticate_request(None)
    assert exc_info.value.status_code == 401
    assert "token required" in exc_info.value.detail.lower()


def test_authenticate_request_empty_token_raises_401():
    with pytest.raises(HTTPException) as exc_info:
        authenticate_request("   ")
    assert exc_info.value.status_code == 401


@patch("app.infrastructure.providers.supabase.identity.get_supabase_client")
def test_authenticate_request_valid_token_returns_user_id(mock_get_client):
    mock_supabase = MagicMock()
    mock_user = MagicMock()
    mock_user.id = "user-uuid-123"
    mock_auth_res = MagicMock(user=mock_user)
    mock_supabase.auth.get_user.return_value = mock_auth_res
    mock_get_client.return_value = mock_supabase

    user_id = authenticate_request("Bearer valid.jwt.token")
    assert user_id == "user-uuid-123"
    mock_supabase.auth.get_user.assert_called_once_with("valid.jwt.token")


@patch("app.security.authorization.get_db_client")
def test_verify_planning_unit_ownership_success(mock_get_db):
    mock_client = MagicMock()
    mock_query = mock_client.table.return_value.select.return_value.eq.return_value.eq.return_value.maybe_single.return_value.execute
    mock_query.return_value.data = {"planning_unit_id": "pu-1"}
    mock_get_db.return_value = mock_client

    # Should not raise
    verify_planning_unit_ownership("pu-1", "user-1")


@patch("app.security.authorization.get_db_client")
def test_verify_planning_unit_ownership_mismatch_raises_403(mock_get_db):
    mock_client = MagicMock()
    mock_query = mock_client.table.return_value.select.return_value.eq.return_value.eq.return_value.maybe_single.return_value.execute
    mock_query.return_value.data = None
    mock_get_db.return_value = mock_client

    with pytest.raises(HTTPException) as exc_info:
        verify_planning_unit_ownership("pu-unknown", "user-1")
    assert exc_info.value.status_code == 403
    assert "Planning unit does not belong to authenticated user" in exc_info.value.detail


@patch("app.security.authorization.verify_planning_unit_ownership")
@patch("app.security.authorization.get_db_client")
def test_verify_goal_ownership_success(mock_get_db, mock_verify_pu):
    mock_client = MagicMock()
    mock_query = mock_client.table.return_value.select.return_value.eq.return_value.eq.return_value.maybe_single.return_value.execute
    mock_query.return_value.data = {"goal_id": "g-100"}
    mock_get_db.return_value = mock_client

    verify_goal_ownership("pu-1", "g-100", "user-1")
    mock_verify_pu.assert_called_once_with("pu-1", "user-1")


@patch("app.security.authorization.verify_planning_unit_ownership")
@patch("app.security.authorization.get_db_client")
def test_verify_assets_ownership_missing_asset_raises_403(mock_get_db, mock_verify_pu):
    mock_client = MagicMock()
    mock_exec = mock_client.table.return_value.select.return_value.eq.return_value.in_.return_value.execute
    # Only asset-1 returned, asset-2 missing
    mock_exec.return_value.data = [{"asset_id": "asset-1"}]
    mock_get_db.return_value = mock_client

    with pytest.raises(HTTPException) as exc_info:
        verify_assets_ownership("pu-1", ["asset-1", "asset-2"], "user-1")
    assert exc_info.value.status_code == 403
    assert "One or more assets do not belong to planning unit" in exc_info.value.detail
