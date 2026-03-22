import pytest
from schemas.request import Sector
from schemas.comps_context import CompsContext
from pipeline.comps.comps_pipeline import CompsPipeline
from models.exceptions import ValuationError


def make_context():
    return CompsContext(company_name="Modus", sector=Sector.SAAS, revenue_mm=10.0)


def test_execute_returns_valuation_report():
    from schemas.report import ValuationReport
    ctx = make_context()
    report = CompsPipeline().execute(ctx)
    assert isinstance(report, ValuationReport)


def test_report_has_all_fields_populated():
    ctx = make_context()
    report = CompsPipeline().execute(ctx)
    assert report.company_name == "Modus"
    assert report.fair_value_mm > 0
    assert report.comps_details is not None
    assert report.comps_details.mean_revenue_multiple > 0
    assert len(report.comps_details.comps_used) >= 2
    assert len(report.assumptions) >= 3
    assert len(report.citations) >= 1
    assert report.explanation != ""


def test_valuation_error_propagates(monkeypatch):
    import data.mock_comps as mock_comps_module
    monkeypatch.setattr(mock_comps_module, "MOCK_COMPS", {})
    with pytest.raises(ValuationError):
        CompsPipeline().execute(make_context())
