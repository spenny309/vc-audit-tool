import pytest
from pipeline.last_round.stages.apply_adjustment import LastRoundApplyAdjustmentStage
from schemas.last_round_context import LastRoundContext
from schemas.request import IndexType


def _make_context(
    index_at_round: float,
    index_today: float,
    valuation_mm: float = 100.0,
    index: IndexType = IndexType.NASDAQ,
) -> LastRoundContext:
    ctx = LastRoundContext(
        company_name="Acme",
        last_post_money_valuation_mm=valuation_mm,
        last_round_date="2020-03-31",
        index=index,
    )
    ctx.index_value_at_round = index_at_round
    ctx.index_value_today = index_today
    return ctx


def test_positive_market_move_increases_fair_value():
    ctx = _make_context(index_at_round=10000.0, index_today=12000.0, valuation_mm=100.0)
    result = LastRoundApplyAdjustmentStage().execute(ctx)
    assert result.fair_value_mm > result.last_post_money_valuation_mm
    assert result.fair_value_mm == 120.0


def test_negative_market_move_decreases_fair_value():
    ctx = _make_context(index_at_round=12000.0, index_today=10000.0, valuation_mm=100.0)
    result = LastRoundApplyAdjustmentStage().execute(ctx)
    assert result.fair_value_mm < result.last_post_money_valuation_mm


def test_zero_market_move_leaves_fair_value_unchanged():
    ctx = _make_context(index_at_round=10000.0, index_today=10000.0, valuation_mm=100.0)
    result = LastRoundApplyAdjustmentStage().execute(ctx)
    assert result.fair_value_mm == result.last_post_money_valuation_mm


def test_zero_index_at_round_raises_calculation_error():
    ctx = _make_context(index_at_round=0.0, index_today=10000.0)
    with pytest.raises(Exception) as exc_info:
        LastRoundApplyAdjustmentStage().execute(ctx)
    assert "zero" in str(exc_info.value).lower()


def test_assumption_text_positive_move():
    ctx = _make_context(index_at_round=10000.0, index_today=11420.0, valuation_mm=100.0)
    result = LastRoundApplyAdjustmentStage().execute(ctx)
    assert len(result.assumptions) == 1
    assert "+14.2%" in result.assumptions[0]
    assert "Nasdaq Composite" in result.assumptions[0]


def test_assumption_text_negative_move():
    ctx = _make_context(index_at_round=12000.0, index_today=10800.0, valuation_mm=50.0)
    result = LastRoundApplyAdjustmentStage().execute(ctx)
    assert "-10.0%" in result.assumptions[0]
    assert "$50.00M" in result.assumptions[0]


def test_index_pct_change_is_set():
    ctx = _make_context(index_at_round=10000.0, index_today=11000.0)
    result = LastRoundApplyAdjustmentStage().execute(ctx)
    assert result.index_pct_change == pytest.approx(0.1)
