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
    # 2020-05-15 is closer to 2020-06-30 than to 2020-03-31
    result = get_index_at_date(IndexType.NASDAQ, date(2020, 5, 15))
    assert result == 10058.77  # 2020-06-30 entry


def test_nearest_date_early_in_quarter():
    # 2020-04-05 is closer to 2020-03-31 than to 2020-06-30
    result = get_index_at_date(IndexType.NASDAQ, date(2020, 4, 5))
    assert result == 7700.00  # 2020-03-31 entry
