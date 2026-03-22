import pytest
from pipeline.dcf.stages.project_cashflows import DcfProjectCashflowsStage
from pipeline.dcf.stages.discount_cashflows import DcfDiscountCashflowsStage
from pipeline.dcf.stages.apply_terminal_value import DcfApplyTerminalValueStage
from pipeline.dcf.stages.build_report import DcfBuildReportStage
from schemas.dcf_context import DcfContext


@pytest.fixture
def context_after_terminal():
    ctx = DcfContext(
        company_name="Alpha",
        projections=[10.0, 11.0, 12.0, 13.0, 14.0],
        ebitda_margin_pct=0.20,
        discount_rate=0.15,
        terminal_growth_rate=0.03,
    )
    ctx = DcfProjectCashflowsStage().execute(ctx)
    ctx = DcfDiscountCashflowsStage().execute(ctx)
    ctx = DcfApplyTerminalValueStage().execute(ctx)
    return ctx


def test_build_report_sets_report(context_after_terminal):
    stage = DcfBuildReportStage()
    result = stage.execute(context_after_terminal)
    assert result.report is not None


def test_build_report_methodology(context_after_terminal):
    stage = DcfBuildReportStage()
    result = stage.execute(context_after_terminal)
    assert result.report.methodology == "Discounted Cash Flow"


def test_build_report_company_name(context_after_terminal):
    stage = DcfBuildReportStage()
    result = stage.execute(context_after_terminal)
    assert result.report.company_name == "Alpha"


def test_build_report_fair_value(context_after_terminal):
    stage = DcfBuildReportStage()
    result = stage.execute(context_after_terminal)
    assert result.report.fair_value_mm == 19.81


def test_build_report_dcf_cashflows_populated(context_after_terminal):
    stage = DcfBuildReportStage()
    result = stage.execute(context_after_terminal)
    assert result.report.dcf_details is not None
    assert len(result.report.dcf_details.dcf_cashflows) == 5
    assert result.report.dcf_details.dcf_cashflows[0].year == 1


def test_build_report_rate_fields_populated(context_after_terminal):
    stage = DcfBuildReportStage()
    result = stage.execute(context_after_terminal)
    assert result.report.dcf_details.terminal_value_mm == 11.95
    assert result.report.dcf_details.ebitda_margin_pct == 0.20
    assert result.report.dcf_details.discount_rate == 0.15
    assert result.report.dcf_details.terminal_growth_rate == 0.03


def test_build_report_comps_fields_are_none(context_after_terminal):
    stage = DcfBuildReportStage()
    result = stage.execute(context_after_terminal)
    assert result.report.comps_details is None


def test_build_report_assumptions_and_citations_passed_through(context_after_terminal):
    stage = DcfBuildReportStage()
    result = stage.execute(context_after_terminal)
    assert len(result.report.assumptions) > 0
    assert len(result.report.citations) > 0
