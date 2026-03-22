import json
import pytest
from unittest.mock import patch
from app import create_app
from models.exceptions import CalculationError
from schemas.report import ValuationReport


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
    assert "comps_details" in data


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


def test_get_models_returns_list(client):
    response = client.get("/api/models")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == ["Comps", "DCF", "Last Round"]


def test_valuate_dcf_returns_report(client):
    response = client.post(
        "/api/valuate",
        json={
            "company_name": "Alpha",
            "model": "DCF",
            "projections": [10.0, 11.0, 12.0, 13.0, 14.0],
            "ebitda_margin_pct": 0.20,
            "discount_rate": 0.15,
            "terminal_growth_rate": 0.03,
        },
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["company_name"] == "Alpha"
    assert data["methodology"] == "Discounted Cash Flow"
    assert data["fair_value_mm"] > 0
    assert "dcf_details" in data
    assert len(data["dcf_details"]["dcf_cashflows"]) == 5


def test_valuate_dcf_rejects_missing_projections(client):
    response = client.post(
        "/api/valuate",
        json={
            "company_name": "X",
            "model": "DCF",
            "ebitda_margin_pct": 0.20,
            "discount_rate": 0.15,
            "terminal_growth_rate": 0.03,
        },
    )
    assert response.status_code == 400


def test_valuate_dcf_rejects_invalid_growth_rate(client):
    response = client.post(
        "/api/valuate",
        json={
            "company_name": "X",
            "model": "DCF",
            "projections": [10.0, 11.0, 12.0, 13.0, 14.0],
            "ebitda_margin_pct": 0.20,
            "discount_rate": 0.10,
            "terminal_growth_rate": 0.15,
        },
    )
    assert response.status_code == 400


def test_create_app_accepts_registry_injection():
    from unittest.mock import MagicMock
    from schemas.request import ModelType
    mock_model = MagicMock()
    mock_model.run.return_value = ValuationReport(
        company_name="Test", methodology="Test", fair_value_mm=1.0,
        assumptions=[], citations=[], explanation="test",
    )
    app = create_app(registry={ModelType.COMPS: mock_model})
    app.config["TESTING"] = True
    with app.test_client() as c:
        response = c.post(
            "/api/valuate",
            json={"company_name": "Test", "model": "Comps", "sector": "SaaS", "revenue_mm": 10.0},
        )
    assert response.status_code == 200
    mock_model.run.assert_called_once()
