import json
import pytest
from unittest.mock import patch
from app import create_app
from models.exceptions import CalculationError


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_sectors_returns_list(client):
    response = client.get("/api/sectors")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert "SaaS" in data


def test_valuate_returns_report(client):
    response = client.post(
        "/api/valuate",
        json={"company_name": "Modus", "model": "Comps", "sector": "SaaS", "revenue_mm": 10.0},
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["company_name"] == "Modus"
    assert data["fair_value_mm"] > 0
    assert data["methodology"] == "Comparable Company Analysis"
    assert "assumptions" in data
    assert "citations" in data
    assert "explanation" in data
    assert "comps_used" in data


def test_valuate_rejects_invalid_sector(client):
    response = client.post(
        "/api/valuate",
        json={"company_name": "X", "model": "Comps", "sector": "NotASector", "revenue_mm": 10.0},
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data


def test_valuate_rejects_negative_revenue(client):
    response = client.post(
        "/api/valuate",
        json={"company_name": "X", "model": "Comps", "sector": "SaaS", "revenue_mm": -5.0},
    )
    assert response.status_code == 400


def test_valuate_rejects_missing_fields(client):
    response = client.post("/api/valuate", json={"company_name": "X"})
    assert response.status_code == 400


def test_valuate_calculation_error_returns_500(client):
    with patch("models.comps_model.CompsModel.run", side_effect=CalculationError("pipeline failure")):
        response = client.post(
            "/api/valuate",
            json={"company_name": "Modus", "model": "Comps", "sector": "SaaS", "revenue_mm": 10.0},
        )
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data["error"] == "CalculationError"
    assert data["status"] == 500
