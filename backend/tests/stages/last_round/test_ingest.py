from datetime import date
from pipeline.last_round.stages.ingest import LastRoundIngestStage
from schemas.last_round_context import LastRoundContext
from schemas.request import IndexType


def _make_context(**kwargs) -> LastRoundContext:
    defaults = dict(
        company_name="Acme Corp",
        last_post_money_valuation_mm=100.0,
        last_round_date="2022-06-30",
        index=IndexType.NASDAQ,
    )
    defaults.update(kwargs)
    return LastRoundContext(**defaults)


def test_company_name_is_stripped():
    ctx = _make_context(company_name="  Acme Corp  ")
    result = LastRoundIngestStage().execute(ctx)
    assert result.company_name == "Acme Corp"


def test_last_round_date_parsed():
    ctx = _make_context(last_round_date="2022-06-30")
    result = LastRoundIngestStage().execute(ctx)
    assert result.last_round_date_parsed == date(2022, 6, 30)


def test_assumption_appended():
    ctx = _make_context(company_name="Acme Corp", last_round_date="2022-06-30")
    result = LastRoundIngestStage().execute(ctx)
    assert len(result.assumptions) == 1
    assert result.assumptions[0] == (
        "Target company: Acme Corp, Last Round (Market-Adjusted) valuation as of 2022-06-30"
    )
