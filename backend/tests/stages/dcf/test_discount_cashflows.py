import pytest
from pipeline.dcf.stages.project_cashflows import DcfProjectCashflowsStage
from pipeline.dcf.stages.discount_cashflows import DcfDiscountCashflowsStage
from schemas.dcf_context import DcfContext


@pytest.fixture
def context_after_project():
    ctx = DcfContext(
        company_name="Alpha",
        projections=[10.0, 11.0, 12.0, 13.0, 14.0],
        ebitda_margin_pct=0.20,
        discount_rate=0.15,
        terminal_growth_rate=0.03,
    )
    return DcfProjectCashflowsStage().execute(ctx)


def test_discount_cashflows_populates_discounted_values(context_after_project):
    stage = DcfDiscountCashflowsStage()
    result = stage.execute(context_after_project)
    for cf in result.cashflows:
        assert cf.discounted_fcf_mm > 0


def test_discount_cashflows_year1_correct(context_after_project):
    stage = DcfDiscountCashflowsStage()
    result = stage.execute(context_after_project)
    # Year 1: fcf=2.0, r=0.15, discounted = round(2.0 / 1.15^1, 2) = round(1.7391, 2) = 1.74
    assert result.cashflows[0].discounted_fcf_mm == 1.74


def test_discount_cashflows_year5_correct(context_after_project):
    stage = DcfDiscountCashflowsStage()
    result = stage.execute(context_after_project)
    # Year 5: fcf=2.8, r=0.15, discounted = round(2.8 / 1.15^5, 2) = round(2.8/2.0114, 2) = round(1.3916, 2) = 1.39
    assert result.cashflows[4].discounted_fcf_mm == 1.39


def test_discount_cashflows_later_years_discounted_more(context_after_project):
    stage = DcfDiscountCashflowsStage()
    result = stage.execute(context_after_project)
    # Year 5 FCF (2.8) is larger than Year 1 FCF (2.0), but discounted value should be less
    assert result.cashflows[4].discounted_fcf_mm < result.cashflows[0].discounted_fcf_mm


def test_discount_cashflows_appends_assumption(context_after_project):
    stage = DcfDiscountCashflowsStage()
    result = stage.execute(context_after_project)
    last_assumption = result.assumptions[-1]
    assert "15.0%" in last_assumption
    assert "WACC" in last_assumption


def test_discount_cashflows_preserves_fcf_values(context_after_project):
    stage = DcfDiscountCashflowsStage()
    result = stage.execute(context_after_project)
    assert result.cashflows[0].fcf_mm == 2.0
    assert result.cashflows[4].fcf_mm == 2.8
