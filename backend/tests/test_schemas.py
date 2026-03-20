from schemas.request import Sector, ValuationRequest, ModelType
from schemas.report import RawCompData, CompData, ValuationReport, DcfYearData
from pydantic import ValidationError
import pytest


# --- Updated existing tests (add model field) ---

def test_valid_valuation_request():
    req = ValuationRequest(company_name="Modus", model=ModelType.COMPS, sector=Sector.SAAS, revenue_mm=10.0)
    assert req.company_name == "Modus"
    assert req.model == ModelType.COMPS
    assert req.sector == Sector.SAAS
    assert req.revenue_mm == 10.0


def test_invalid_sector_rejected():
    with pytest.raises(ValidationError):
        ValuationRequest(company_name="Modus", model=ModelType.COMPS, sector="NotASector", revenue_mm=10.0)


def test_negative_revenue_rejected():
    with pytest.raises(ValidationError):
        ValuationRequest(company_name="Modus", model=ModelType.COMPS, sector=Sector.SAAS, revenue_mm=-1.0)


def test_zero_revenue_rejected():
    with pytest.raises(ValidationError):
        ValuationRequest(company_name="Modus", model=ModelType.COMPS, sector=Sector.SAAS, revenue_mm=0.0)


# --- model_validator: Comps missing fields ---

def test_comps_missing_sector_rejected():
    with pytest.raises(ValidationError, match="sector is required"):
        ValuationRequest(company_name="X", model=ModelType.COMPS, revenue_mm=10.0)


def test_comps_missing_revenue_rejected():
    with pytest.raises(ValidationError, match="revenue_mm must be greater than 0"):
        ValuationRequest(company_name="X", model=ModelType.COMPS, sector=Sector.SAAS)


# --- model_validator: DCF valid request ---

def test_valid_dcf_request():
    req = ValuationRequest(
        company_name="Alpha",
        model=ModelType.DCF,
        projections=[10.0, 11.0, 12.0, 13.0, 14.0],
        ebitda_margin_pct=0.20,
        discount_rate=0.15,
        terminal_growth_rate=0.03,
    )
    assert req.model == ModelType.DCF
    assert req.projections == [10.0, 11.0, 12.0, 13.0, 14.0]


# --- model_validator: DCF invalid projections ---

def test_dcf_wrong_projection_count_rejected():
    with pytest.raises(ValidationError, match="exactly 5 values"):
        ValuationRequest(
            company_name="X", model=ModelType.DCF,
            projections=[10.0, 11.0, 12.0],
            ebitda_margin_pct=0.20, discount_rate=0.15, terminal_growth_rate=0.03,
        )


def test_dcf_negative_projection_rejected():
    with pytest.raises(ValidationError, match="greater than 0"):
        ValuationRequest(
            company_name="X", model=ModelType.DCF,
            projections=[10.0, -1.0, 12.0, 13.0, 14.0],
            ebitda_margin_pct=0.20, discount_rate=0.15, terminal_growth_rate=0.03,
        )


def test_dcf_terminal_growth_exceeds_discount_rejected():
    with pytest.raises(ValidationError, match="terminal_growth_rate must be less than discount_rate"):
        ValuationRequest(
            company_name="X", model=ModelType.DCF,
            projections=[10.0, 11.0, 12.0, 13.0, 14.0],
            ebitda_margin_pct=0.20, discount_rate=0.10, terminal_growth_rate=0.15,
        )


def test_dcf_out_of_range_margin_rejected():
    with pytest.raises(ValidationError, match="ebitda_margin_pct must be between 0 and 1"):
        ValuationRequest(
            company_name="X", model=ModelType.DCF,
            projections=[10.0, 11.0, 12.0, 13.0, 14.0],
            ebitda_margin_pct=1.5, discount_rate=0.15, terminal_growth_rate=0.03,
        )


# --- Updated ValuationReport tests (Comps fields still provided) ---

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
        mean_revenue_multiple=6.38,
        comps_used=[comp],
        assumptions=["Mean EV/Revenue multiple of 6.4x across 1 comparables"],
        citations=["Mock dataset (Yahoo Finance API in production)"],
        explanation="Modus was valued at $63.8M using a mean EV/Revenue multiple of 6.4x.",
    )
    assert report.fair_value_mm == 63.8
    assert len(report.comps_used) == 1


# --- DcfYearData ---

def test_dcf_year_data():
    row = DcfYearData(year=1, revenue_mm=10.0, fcf_mm=2.0, discounted_fcf_mm=1.74)
    assert row.year == 1
    assert row.discounted_fcf_mm == 1.74


# --- ValuationReport with DCF fields ---

def test_dcf_valuation_report():
    row = DcfYearData(year=1, revenue_mm=10.0, fcf_mm=2.0, discounted_fcf_mm=1.74)
    report = ValuationReport(
        company_name="Alpha",
        methodology="Discounted Cash Flow",
        fair_value_mm=19.81,
        assumptions=["Target company: Alpha, 5-year DCF projection"],
        citations=["Projections provided by user"],
        explanation="Alpha was valued at $19.8M.",
        dcf_cashflows=[row],
        terminal_value_mm=11.95,
        ebitda_margin_pct=0.20,
        discount_rate=0.15,
        terminal_growth_rate=0.03,
    )
    assert report.dcf_cashflows[0].year == 1
    assert report.terminal_value_mm == 11.95
    assert report.comps_used is None
    assert report.mean_revenue_multiple is None
