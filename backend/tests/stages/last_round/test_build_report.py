from datetime import date
from pipeline.last_round.stages.build_report import LastRoundBuildReportStage
from schemas.last_round_context import LastRoundContext
from schemas.request import IndexType


def _make_context() -> LastRoundContext:
    ctx = LastRoundContext(
        company_name="Acme Corp",
        last_post_money_valuation_mm=100.0,
        last_round_date="2020-03-31",
        index=IndexType.NASDAQ,
    )
    ctx.last_round_date_parsed = date(2020, 3, 31)
    ctx.index_value_at_round = 7700.0
    ctx.index_value_today = 18500.0
    ctx.index_pct_change = 1.40259  # (18500 - 7700) / 7700
    ctx.fair_value_mm = 240.26
    ctx.assumptions = ["Assumption 1"]
    ctx.citations = ["Citation 1"]
    return ctx


def test_all_last_round_fields_populated():
    ctx = _make_context()
    result = LastRoundBuildReportStage().execute(ctx)
    report = result.report
    assert report.company_name == "Acme Corp"
    assert report.methodology == "Last Round (Market-Adjusted)"
    assert report.fair_value_mm == 240.26
    assert report.last_round_details is not None
    assert report.last_round_details.last_post_money_valuation_mm == 100.0
    assert report.last_round_details.last_round_date == "2020-03-31"
    assert report.last_round_details.index_name == "Nasdaq Composite"
    assert report.last_round_details.index_value_at_round == 7700.0
    assert report.last_round_details.index_value_today == 18500.0
    assert report.last_round_details.index_pct_change == 1.40259


def test_explanation_contains_key_info():
    ctx = _make_context()
    result = LastRoundBuildReportStage().execute(ctx)
    explanation = result.report.explanation
    assert "Acme Corp" in explanation
    assert "240.26" in explanation  # fair value
    assert "100.00" in explanation  # original valuation
    assert "2020-03-31" in explanation  # round date
    assert "Nasdaq Composite" in explanation  # index name
    assert "+140.3%" in explanation  # adjustment pct


def test_assumptions_and_citations_passed_through():
    ctx = _make_context()
    result = LastRoundBuildReportStage().execute(ctx)
    assert result.report.assumptions == ["Assumption 1"]
    assert result.report.citations == ["Citation 1"]
