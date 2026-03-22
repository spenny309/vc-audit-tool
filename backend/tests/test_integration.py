import pytest
from schemas.request import Sector, ValuationRequest, ModelType
from models.comps_model import CompsModel
from schemas.report import ValuationReport


@pytest.mark.parametrize("sector", [s for s in Sector])
def test_full_pipeline_produces_valid_report_for_all_sectors(sector):
    request = ValuationRequest(company_name="Test Co", model=ModelType.COMPS, sector=sector, revenue_mm=50.0)
    report = CompsModel().run(request)

    assert isinstance(report, ValuationReport)
    assert report.company_name == "Test Co"
    assert report.methodology == "Comparable Company Analysis"
    assert report.comps_details is not None
    assert report.comps_details.mean_revenue_multiple > 0
    assert report.fair_value_mm == round(report.comps_details.mean_revenue_multiple * 50.0, 2)
    assert len(report.comps_details.comps_used) >= 2
    assert len(report.assumptions) >= 3
    assert len(report.citations) >= 1
    assert report.explanation != ""
    assert "Test Co" in report.explanation


def test_fair_value_is_multiple_times_revenue():
    request = ValuationRequest(company_name="Test Co", model=ModelType.COMPS, sector=Sector.SAAS, revenue_mm=10.0)
    report = CompsModel().run(request)
    expected = round(report.comps_details.mean_revenue_multiple * 10.0, 2)
    assert report.fair_value_mm == expected


def test_audit_trail_is_complete():
    request = ValuationRequest(company_name="Modus", model=ModelType.COMPS, sector=Sector.SAAS, revenue_mm=10.0)
    report = CompsModel().run(request)

    full_text = " ".join(report.assumptions + report.citations + [report.explanation])
    assert "Modus" in full_text
    assert "SaaS" in full_text
    assert "mock" in full_text.lower() or "Mock" in full_text
