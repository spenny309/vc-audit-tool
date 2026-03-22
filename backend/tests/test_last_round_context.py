from datetime import date
from schemas.last_round_context import LastRoundContext
from schemas.request import IndexType


def test_construction_with_required_fields():
    ctx = LastRoundContext(
        company_name="Acme",
        last_post_money_valuation_mm=100.0,
        last_round_date="2022-06-30",
        index=IndexType.NASDAQ,
    )
    assert ctx.company_name == "Acme"
    assert ctx.last_post_money_valuation_mm == 100.0
    assert ctx.last_round_date == "2022-06-30"
    assert ctx.index == IndexType.NASDAQ
    assert ctx.last_round_date_parsed is None
    assert ctx.index_value_at_round is None
    assert ctx.index_value_today is None
    assert ctx.index_pct_change is None
    assert ctx.fair_value_mm is None
    assert ctx.report is None
    assert ctx.assumptions == []
    assert ctx.citations == []


def test_optional_fields_can_be_set():
    ctx = LastRoundContext(
        company_name="Acme",
        last_post_money_valuation_mm=100.0,
        last_round_date="2022-06-30",
        index=IndexType.NASDAQ,
    )
    ctx.last_round_date_parsed = date(2022, 6, 30)
    ctx.index_value_at_round = 11834.11
    ctx.index_value_today = 18500.0
    ctx.index_pct_change = 0.564
    ctx.fair_value_mm = 156.4
    ctx.assumptions.append("Test assumption")
    ctx.citations.append("Test citation")

    assert ctx.last_round_date_parsed == date(2022, 6, 30)
    assert ctx.index_value_at_round == 11834.11
    assert ctx.index_value_today == 18500.0
    assert ctx.index_pct_change == 0.564
    assert ctx.fair_value_mm == 156.4
    assert ctx.assumptions == ["Test assumption"]
    assert ctx.citations == ["Test citation"]
