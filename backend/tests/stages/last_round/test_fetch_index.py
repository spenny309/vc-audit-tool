from datetime import date
from data.mock_index import (
    INDEX_QUARTERLY_CLOSES,
    INDEX_VALUE_TODAY,
    get_index_at_date,
)
from schemas.request import IndexType


def test_all_three_indices_present():
    assert IndexType.NASDAQ in INDEX_QUARTERLY_CLOSES
    assert IndexType.SP500 in INDEX_QUARTERLY_CLOSES
    assert IndexType.RUSSELL in INDEX_QUARTERLY_CLOSES


def test_each_index_has_entries():
    for index_type, closes in INDEX_QUARTERLY_CLOSES.items():
        assert len(closes) >= 40, f"{index_type} has fewer than 40 entries"


def test_earliest_entry_is_2015():
    for closes in INDEX_QUARTERLY_CLOSES.values():
        assert min(closes) >= date(2015, 1, 1)


def test_index_value_today_matches_latest_entry():
    for index_type, closes in INDEX_QUARTERLY_CLOSES.items():
        latest_date = max(closes)
        assert INDEX_VALUE_TODAY[index_type] == closes[latest_date]


def test_exact_date_match_nasdaq():
    result = get_index_at_date(IndexType.NASDAQ, date(2020, 3, 31))
    assert result == 7700.00


def test_exact_date_match_sp500():
    result = get_index_at_date(IndexType.SP500, date(2020, 3, 31))
    assert result == 2584.59


def test_exact_date_match_russell():
    result = get_index_at_date(IndexType.RUSSELL, date(2020, 3, 31))
    assert result == 1153.56


def test_nearest_date_between_entries():
    # 2020-06-15 is much closer to 2020-06-30 than to 2020-03-31
    result = get_index_at_date(IndexType.NASDAQ, date(2020, 6, 15))
    assert result == 10058.77  # 2020-06-30 entry


def test_nearest_date_early_in_quarter():
    # 2020-04-05 is closer to 2020-03-31 than to 2020-06-30
    result = get_index_at_date(IndexType.NASDAQ, date(2020, 4, 5))
    assert result == 7700.00  # 2020-03-31 entry


# --- Stage tests ---
from pipeline.last_round.stages.fetch_index import LastRoundFetchIndexStage
from schemas.last_round_context import LastRoundContext
from data.mock_index import INDEX_VALUE_TODAY, INDEX_QUARTERLY_CLOSES


def _make_context(index=IndexType.NASDAQ, round_date=date(2020, 3, 31)) -> LastRoundContext:
    ctx = LastRoundContext(
        company_name="Acme",
        last_post_money_valuation_mm=100.0,
        last_round_date=str(round_date),
        index=index,
    )
    ctx.last_round_date_parsed = round_date
    return ctx


def test_fetch_index_sets_index_value_at_round_nasdaq():
    ctx = _make_context(index=IndexType.NASDAQ, round_date=date(2020, 3, 31))
    result = LastRoundFetchIndexStage().execute(ctx)
    assert result.index_value_at_round == INDEX_QUARTERLY_CLOSES[IndexType.NASDAQ][date(2020, 3, 31)]


def test_fetch_index_sets_index_value_at_round_sp500():
    ctx = _make_context(index=IndexType.SP500, round_date=date(2020, 3, 31))
    result = LastRoundFetchIndexStage().execute(ctx)
    assert result.index_value_at_round == INDEX_QUARTERLY_CLOSES[IndexType.SP500][date(2020, 3, 31)]


def test_fetch_index_sets_index_value_at_round_russell():
    ctx = _make_context(index=IndexType.RUSSELL, round_date=date(2020, 3, 31))
    result = LastRoundFetchIndexStage().execute(ctx)
    assert result.index_value_at_round == INDEX_QUARTERLY_CLOSES[IndexType.RUSSELL][date(2020, 3, 31)]


def test_fetch_index_sets_index_value_today():
    ctx = _make_context(index=IndexType.NASDAQ)
    result = LastRoundFetchIndexStage().execute(ctx)
    assert result.index_value_today == INDEX_VALUE_TODAY[IndexType.NASDAQ]


def test_fetch_index_today_is_deterministic_not_date_today():
    """index_value_today must equal the module constant, not a live lookup."""
    ctx = _make_context(index=IndexType.SP500)
    result = LastRoundFetchIndexStage().execute(ctx)
    assert result.index_value_today == INDEX_VALUE_TODAY[IndexType.SP500]


def test_citation_includes_index_name():
    ctx = _make_context(index=IndexType.NASDAQ)
    result = LastRoundFetchIndexStage().execute(ctx)
    assert len(result.citations) == 1
    assert "Nasdaq Composite" in result.citations[0]
    assert "mock historical quarterly close prices" in result.citations[0]


def test_assumption_includes_index_name_and_round_date():
    ctx = _make_context(index=IndexType.NASDAQ, round_date=date(2020, 3, 31))
    result = LastRoundFetchIndexStage().execute(ctx)
    assert len(result.assumptions) == 1
    assert "Nasdaq Composite" in result.assumptions[0]
    assert "2020-03-31" in result.assumptions[0]
    assert "nearest quarterly close" in result.assumptions[0]
