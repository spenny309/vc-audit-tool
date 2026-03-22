from schemas.request import (
    Sector, ModelType, IndexType,
    CompsRequest, DcfRequest, LastRoundRequest,
)
from schemas.report import RawCompData, CompData, ValuationReport, DcfYearData, CompsDetails, DcfDetails
from pydantic import ValidationError
import pytest


# ---------------------------------------------------------------------------
# CompsRequest validation
# ---------------------------------------------------------------------------

def test_valid_comps_request():
    req = CompsRequest(model="Comps", company_name="Modus", sector=Sector.SAAS, revenue_mm=10.0)
    assert req.company_name == "Modus"
    assert req.model == "Comps"
    assert req.sector == Sector.SAAS
    assert req.revenue_mm == 10.0


def test_invalid_sector_rejected():
    with pytest.raises(ValidationError):
        CompsRequest(model="Comps", company_name="Modus", sector="NotASector", revenue_mm=10.0)


def test_negative_revenue_rejected():
    with pytest.raises(ValidationError):
        CompsRequest(model="Comps", company_name="Modus", sector=Sector.SAAS, revenue_mm=-1.0)


def test_zero_revenue_rejected():
    with pytest.raises(ValidationError):
        CompsRequest(model="Comps", company_name="Modus", sector=Sector.SAAS, revenue_mm=0.0)


def test_comps_missing_sector_rejected():
    with pytest.raises(ValidationError):
        CompsRequest(model="Comps", company_name="X", revenue_mm=10.0)


def test_comps_missing_revenue_rejected():
    with pytest.raises(ValidationError):
        CompsRequest(model="Comps", company_name="X", sector=Sector.SAAS)


# ---------------------------------------------------------------------------
# DcfRequest validation
# ---------------------------------------------------------------------------

def test_valid_dcf_request():
    req = DcfRequest(
        model="DCF",
        company_name="Alpha",
        projections=[10.0, 11.0, 12.0, 13.0, 14.0],
        ebitda_margin_pct=0.20,
        discount_rate=0.15,
        terminal_growth_rate=0.03,
    )
    assert req.model == "DCF"
    assert req.projections == [10.0, 11.0, 12.0, 13.0, 14.0]


def test_dcf_wrong_projection_count_rejected():
    with pytest.raises(ValidationError, match="exactly 5 annual values"):
        DcfRequest(
            model="DCF",
            company_name="X",
            projections=[10.0, 11.0, 12.0],
            ebitda_margin_pct=0.20,
            discount_rate=0.15,
            terminal_growth_rate=0.03,
        )


def test_dcf_negative_projection_rejected():
    with pytest.raises(ValidationError, match="all projections must be greater than 0"):
        DcfRequest(
            model="DCF",
            company_name="X",
            projections=[10.0, -1.0, 12.0, 13.0, 14.0],
            ebitda_margin_pct=0.20,
            discount_rate=0.15,
            terminal_growth_rate=0.03,
        )


def test_dcf_terminal_growth_exceeds_discount_rejected():
    with pytest.raises(ValidationError, match="terminal_growth_rate must be less than discount_rate"):
        DcfRequest(
            model="DCF",
            company_name="X",
            projections=[10.0, 11.0, 12.0, 13.0, 14.0],
            ebitda_margin_pct=0.20,
            discount_rate=0.10,
            terminal_growth_rate=0.15,
        )


def test_dcf_out_of_range_margin_rejected():
    with pytest.raises(ValidationError, match="rate must be between 0 and 1"):
        DcfRequest(
            model="DCF",
            company_name="X",
            projections=[10.0, 11.0, 12.0, 13.0, 14.0],
            ebitda_margin_pct=1.5,
            discount_rate=0.15,
            terminal_growth_rate=0.03,
        )


# ---------------------------------------------------------------------------
# LastRoundRequest validation
# ---------------------------------------------------------------------------

def test_last_round_valid_request():
    req = LastRoundRequest(
        model="Last Round",
        company_name="Acme",
        last_post_money_valuation_mm=100.0,
        last_round_date="2021-06-30",
    )
    assert req.model == "Last Round"
    assert req.last_post_money_valuation_mm == 100.0
    assert req.last_round_date == "2021-06-30"
    assert req.index == IndexType.NASDAQ  # validator sets default


def test_last_round_missing_valuation_rejected():
    with pytest.raises(ValidationError):
        LastRoundRequest(
            model="Last Round",
            company_name="Acme",
            last_round_date="2021-06-30",
        )


def test_last_round_zero_valuation_rejected():
    with pytest.raises(ValidationError):
        LastRoundRequest(
            model="Last Round",
            company_name="Acme",
            last_post_money_valuation_mm=0.0,
            last_round_date="2021-06-30",
        )


def test_last_round_missing_date_rejected():
    with pytest.raises(ValidationError):
        LastRoundRequest(
            model="Last Round",
            company_name="Acme",
            last_post_money_valuation_mm=100.0,
        )


def test_last_round_invalid_date_format_rejected():
    with pytest.raises(ValidationError):
        LastRoundRequest(
            model="Last Round",
            company_name="Acme",
            last_post_money_valuation_mm=100.0,
            last_round_date="06/30/2021",
        )


def test_last_round_future_date_rejected():
    with pytest.raises(ValidationError):
        LastRoundRequest(
            model="Last Round",
            company_name="Acme",
            last_post_money_valuation_mm=100.0,
            last_round_date="2099-01-01",
        )


def test_last_round_date_before_2015_rejected():
    with pytest.raises(ValidationError):
        LastRoundRequest(
            model="Last Round",
            company_name="Acme",
            last_post_money_valuation_mm=100.0,
            last_round_date="2014-12-31",
        )


def test_last_round_explicit_sp500_index():
    req = LastRoundRequest(
        model="Last Round",
        company_name="Acme",
        last_post_money_valuation_mm=50.0,
        last_round_date="2022-06-30",
        index="S&P 500",
    )
    assert req.index == IndexType.SP500


def test_last_round_invalid_index_rejected():
    with pytest.raises(ValidationError):
        LastRoundRequest(
            model="Last Round",
            company_name="Acme",
            last_post_money_valuation_mm=100.0,
            last_round_date="2021-06-30",
            index="Dow Jones",
        )


# ---------------------------------------------------------------------------
# ValuationReport tests (unchanged)
# ---------------------------------------------------------------------------

def test_raw_comp_data():
    comp = RawCompData(name="Salesforce", enterprise_value_mm=200_000, revenue_mm=31_352)
    assert comp.name == "Salesforce"


def test_comp_data_with_multiple():
    comp = CompData(
        name="Salesforce",
        enterprise_value_mm=200_000,
        revenue_mm=31_352,
        revenue_multiple=6.38,
    )
    assert comp.revenue_multiple == 6.38


def test_valuation_report():
    comp = CompData(name="Salesforce", enterprise_value_mm=200_000, revenue_mm=31_352, revenue_multiple=6.38)
    report = ValuationReport(
        company_name="Modus",
        methodology="Comparable Company Analysis",
        fair_value_mm=63.8,
        assumptions=["Mean EV/Revenue multiple of 6.4x across 1 comparables"],
        citations=["Mock dataset (Yahoo Finance API in production)"],
        explanation="Modus was valued at $63.8M using a mean EV/Revenue multiple of 6.4x.",
        comps_details=CompsDetails(mean_revenue_multiple=6.38, comps_used=[comp]),
    )
    assert report.fair_value_mm == 63.8
    assert report.comps_details is not None
    assert len(report.comps_details.comps_used) == 1


def test_dcf_year_data():
    row = DcfYearData(year=1, revenue_mm=10.0, fcf_mm=2.0, discounted_fcf_mm=1.74)
    assert row.year == 1
    assert row.discounted_fcf_mm == 1.74


def test_dcf_valuation_report():
    row = DcfYearData(year=1, revenue_mm=10.0, fcf_mm=2.0, discounted_fcf_mm=1.74)
    report = ValuationReport(
        company_name="Alpha",
        methodology="Discounted Cash Flow",
        fair_value_mm=19.81,
        assumptions=["Target company: Alpha, 5-year DCF projection"],
        citations=["Projections provided by user"],
        explanation="Alpha was valued at $19.8M.",
        dcf_details=DcfDetails(
            dcf_cashflows=[row],
            terminal_value_mm=11.95,
            ebitda_margin_pct=0.20,
            discount_rate=0.15,
            terminal_growth_rate=0.03,
        ),
    )
    assert report.dcf_details is not None
    assert report.dcf_details.dcf_cashflows[0].year == 1
    assert report.dcf_details.terminal_value_mm == 11.95
    assert report.comps_details is None
