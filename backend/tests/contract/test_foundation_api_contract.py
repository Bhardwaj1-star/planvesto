"""Contract tests for Foundation API endpoints and error handling."""

from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.api.app import create_app
from main import app as legacy_app


def test_app_factory_creates_working_fastapi_instance():
    app = create_app()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "Planvesto" in data["service"]


def test_health_check_endpoint_contract():
    app = create_app()
    client = TestClient(app)
    with patch("app.api.routers.health.check_database_health") as mock_db:
        mock_db.return_value = {"connected": True}
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert data["database"] is True


def test_cors_headers_applied():
    app = create_app()
    client = TestClient(app)
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    # Status code can be 200 for CORS preflight
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_legacy_main_app_backward_compatibility():
    client = TestClient(legacy_app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
