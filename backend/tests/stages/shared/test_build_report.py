from schemas.request import Sector
from schemas.comps_context import CompsContext
from schemas.report import CompData
from pipeline.comps.stages.build_report import CompsBuildReportStage


def make_fully_enriched_context():
    ctx = CompsContext(company_name="Modus", sector=Sector.SAAS, revenue_mm=10.0)
    ctx.comps = [
        CompData(name="Salesforce", enterprise_value_mm=200_000, revenue_mm=31_352, revenue_multiple=6.38),
        CompData(name="HubSpot", enterprise_value_mm=18_000, revenue_mm=2_250, revenue_multiple=8.0),
    ]
    ctx.mean_revenue_multiple = 7.19
    ctx.fair_value_mm = 71.9
    ctx.assumptions = ["Selected 2 SaaS comparables", "Mean EV/Revenue multiple of 7.19x"]
    ctx.citations = ["Mock dataset (Yahoo Finance API in production)"]
    return ctx


def test_populates_report_on_context():
    ctx = make_fully_enriched_context()
    result = CompsBuildReportStage().execute(ctx)
    assert result.report is not None


def test_report_has_all_required_fields():
    ctx = make_fully_enriched_context()
    result = CompsBuildReportStage().execute(ctx)
    report = result.report
    assert report.company_name == "Modus"
    assert report.methodology == "Comparable Company Analysis"
    assert report.fair_value_mm == 71.9
    assert report.mean_revenue_multiple == 7.19
    assert len(report.comps_used) == 2
    assert len(report.assumptions) == 2
    assert len(report.citations) == 1


def test_explanation_contains_key_values():
    ctx = make_fully_enriched_context()
    result = CompsBuildReportStage().execute(ctx)
    explanation = result.report.explanation
    assert "Modus" in explanation
    assert "71.9" in explanation
    assert "7.19x" in explanation
    assert "10.0" in explanation
    assert "2" in explanation  # number of comps
