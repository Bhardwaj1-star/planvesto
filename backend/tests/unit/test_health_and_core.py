"""
Unit tests for FastAPI composition root & core configuration.
"""

from fastapi.testclient import TestClient
from app.main import app
from app.core.config import Settings
from app.core.errors import EntityNotFoundError, DomainValidationError

client = TestClient(app)


def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "PlanVesto Backend"
    assert "timestamp" in data


def test_readiness_check_endpoint():
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"


def test_custom_exception_handler_entity_not_found():
    # Test route triggering AppBaseException
    @app.get("/test-not-found")
    async def trigger_not_found():
        raise EntityNotFoundError(entity_name="Goal", identifier="goal-123")

    response = client.get("/test-not-found")
    assert response.status_code == 404
    err_body = response.json()["error"]
    assert err_body["code"] == "ENTITY_NOT_FOUND"
    assert "goal-123" in err_body["message"]
    assert err_body["details"]["identifier"] == "goal-123"


def test_custom_exception_handler_domain_validation():
    @app.get("/test-validation-error")
    async def trigger_val_error():
        raise DomainValidationError(message="Invalid amount", details={"field": "amount"})

    response = client.get("/test-validation-error")
    assert response.status_code == 400
    err_body = response.json()["error"]
    assert err_body["code"] == "DOMAIN_VALIDATION_ERROR"
    assert err_body["details"]["field"] == "amount"


def test_settings_initialization():
    s = Settings(ENVIRONMENT="testing", DEBUG=True)
    assert s.ENVIRONMENT == "testing"
    assert s.DEBUG is True
    assert s.API_V1_PREFIX == "/api/v1"
