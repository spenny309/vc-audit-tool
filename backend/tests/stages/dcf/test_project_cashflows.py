import pytest
from pipeline.dcf.stages.project_cashflows import DcfProjectCashflowsStage
from schemas.dcf_context import DcfContext


@pytest.fixture
def context():
    return DcfContext(
        company_name="Alpha",
        projections=[10.0, 11.0, 12.0, 13.0, 14.0],
        ebitda_margin_pct=0.20,
        discount_rate=0.15,
        terminal_growth_rate=0.03,
    )


def test_project_cashflows_creates_five_entries(context):
    stage = DcfProjectCashflowsStage()
    result = stage.execute(context)
    assert len(result.cashflows) == 5


def test_project_cashflows_year_indices_are_one_based(context):
    stage = DcfProjectCashflowsStage()
    result = stage.execute(context)
    assert [cf.year for cf in result.cashflows] == [1, 2, 3, 4, 5]


def test_project_cashflows_revenue_matches_projections(context):
    stage = DcfProjectCashflowsStage()
    result = stage.execute(context)
    assert result.cashflows[0].revenue_mm == 10.0
    assert result.cashflows[4].revenue_mm == 14.0


def test_project_cashflows_fcf_equals_revenue_times_margin(context):
    stage = DcfProjectCashflowsStage()
    result = stage.execute(context)
    # Year 1: 10.0 * 0.20 = 2.0
    assert result.cashflows[0].fcf_mm == 2.0
    # Year 5: 14.0 * 0.20 = 2.8
    assert result.cashflows[4].fcf_mm == 2.8


def test_project_cashflows_appends_assumption(context):
    stage = DcfProjectCashflowsStage()
    result = stage.execute(context)
    assert len(result.assumptions) == 1
    assert "20.0%" in result.assumptions[0]
    assert "EBITDA margin" in result.assumptions[0]


def test_project_cashflows_appends_citation(context):
    stage = DcfProjectCashflowsStage()
    result = stage.execute(context)
    assert "Projections provided by user" in result.citations
