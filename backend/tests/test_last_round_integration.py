import pytest
from app import create_app
from data.mock_index import INDEX_QUARTERLY_CLOSES, INDEX_VALUE_TODAY
from datetime import date
from schemas.request import IndexType


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def _last_round_payload(**kwargs):
    defaults = {
        "company_name": "Acme",
        "model": "Last Round",
        "last_post_money_valuation_mm": 100.0,
        "last_round_date": "2020-03-31",
        "index": "Nasdaq Composite",
    }
    defaults.update(kwargs)
    return defaults


def test_last_round_nasdaq_returns_200_with_exact_fair_value(client):
    resp = client.post("/api/valuate", json=_last_round_payload())
    assert resp.status_code == 200
    data = resp.get_json()
    # Compute expected fair value
    index_at_round = INDEX_QUARTERLY_CLOSES[IndexType.NASDAQ][date(2020, 3, 31)]
    index_today = INDEX_VALUE_TODAY[IndexType.NASDAQ]
    pct_change = (index_today - index_at_round) / index_at_round
    expected_fair_value = 100.0 * (1 + pct_change)
    assert data["fair_value_mm"] == pytest.approx(expected_fair_value)


def test_last_round_sp500_returns_correct_index_name(client):
    resp = client.post("/api/valuate", json=_last_round_payload(index="S&P 500"))
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["last_round_details"]["index_name"] == "S&P 500"


def test_last_round_russell_returns_correct_index_name(client):
    resp = client.post("/api/valuate", json=_last_round_payload(index="Russell 2000"))
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["last_round_details"]["index_name"] == "Russell 2000"


def test_last_round_no_index_defaults_to_nasdaq(client):
    payload = _last_round_payload()
    del payload["index"]
    resp = client.post("/api/valuate", json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["last_round_details"]["index_name"] == "Nasdaq Composite"


def test_get_indices_returns_all_three(client):
    resp = client.get("/api/indices")
    assert resp.status_code == 200
    indices = resp.get_json()
    assert "Nasdaq Composite" in indices
    assert "S&P 500" in indices
    assert "Russell 2000" in indices


def test_missing_last_post_money_valuation_returns_400(client):
    payload = _last_round_payload()
    del payload["last_post_money_valuation_mm"]
    resp = client.post("/api/valuate", json=payload)
    assert resp.status_code == 400


def test_missing_last_round_date_returns_400(client):
    payload = _last_round_payload()
    del payload["last_round_date"]
    resp = client.post("/api/valuate", json=payload)
    assert resp.status_code == 400


def test_future_last_round_date_returns_400(client):
    resp = client.post("/api/valuate", json=_last_round_payload(last_round_date="2099-01-01"))
    assert resp.status_code == 400


def test_last_round_date_before_2015_returns_400(client):
    resp = client.post("/api/valuate", json=_last_round_payload(last_round_date="2014-12-31"))
    assert resp.status_code == 400


def test_invalid_index_value_returns_400(client):
    resp = client.post("/api/valuate", json=_last_round_payload(index="Invalid Index"))
    assert resp.status_code == 400
