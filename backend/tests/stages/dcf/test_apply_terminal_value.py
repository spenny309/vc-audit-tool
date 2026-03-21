import pytest
from pipeline.dcf.stages.project_cashflows import DcfProjectCashflowsStage
from pipeline.dcf.stages.discount_cashflows import DcfDiscountCashflowsStage
from pipeline.dcf.stages.apply_terminal_value import DcfApplyTerminalValueStage
from schemas.dcf_context import DcfContext


@pytest.fixture
def context_after_discount():
    ctx = DcfContext(
        company_name="Alpha",
        projections=[10.0, 11.0, 12.0, 13.0, 14.0],
        ebitda_margin_pct=0.20,
        discount_rate=0.15,
        terminal_growth_rate=0.03,
    )
    ctx = DcfProjectCashflowsStage().execute(ctx)
    ctx = DcfDiscountCashflowsStage().execute(ctx)
    return ctx


def test_apply_terminal_value_sets_terminal_value_mm(context_after_discount):
    stage = DcfApplyTerminalValueStage()
    result = stage.execute(context_after_discount)
    assert result.terminal_value_mm is not None
    assert result.terminal_value_mm > 0


def test_apply_terminal_value_correct_amount(context_after_discount):
    stage = DcfApplyTerminalValueStage()
    result = stage.execute(context_after_discount)
    assert result.terminal_value_mm == 11.95


def test_apply_terminal_value_sets_fair_value_mm(context_after_discount):
    stage = DcfApplyTerminalValueStage()
    result = stage.execute(context_after_discount)
    assert result.fair_value_mm is not None
    assert result.fair_value_mm > 0


def test_apply_terminal_value_fair_value_equals_sum_plus_tv(context_after_discount):
    stage = DcfApplyTerminalValueStage()
    result = stage.execute(context_after_discount)
    assert result.fair_value_mm == 19.81


def test_apply_terminal_value_appends_assumption(context_after_discount):
    stage = DcfApplyTerminalValueStage()
    result = stage.execute(context_after_discount)
    last = result.assumptions[-1]
    assert "Discounted terminal value" in last
    assert "Gordon Growth Model" in last
    assert "3.0%" in last
