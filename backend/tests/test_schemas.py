from schemas.request import Sector, ValuationRequest
from pydantic import ValidationError
import pytest


def test_valid_valuation_request():
    req = ValuationRequest(company_name="Basis AI", sector=Sector.SAAS, revenue_mm=10.0)
    assert req.company_name == "Basis AI"
    assert req.sector == Sector.SAAS
    assert req.revenue_mm == 10.0


def test_invalid_sector_rejected():
    with pytest.raises(ValidationError):
        ValuationRequest(company_name="Basis AI", sector="NotASector", revenue_mm=10.0)


def test_negative_revenue_rejected():
    with pytest.raises(ValidationError):
        ValuationRequest(company_name="Basis AI", sector=Sector.SAAS, revenue_mm=-1.0)


def test_zero_revenue_rejected():
    with pytest.raises(ValidationError):
        ValuationRequest(company_name="Basis AI", sector=Sector.SAAS, revenue_mm=0.0)


from schemas.report import RawCompData, CompData, ValuationReport


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
    comp = CompData(
        name="Salesforce",
        enterprise_value_mm=200_000,
        revenue_mm=31_352,
        revenue_multiple=6.38,
    )
    report = ValuationReport(
        company_name="Basis AI",
        methodology="Comparable Company Analysis",
        fair_value_mm=63.8,
        mean_revenue_multiple=6.38,
        comps_used=[comp],
        assumptions=["Mean EV/Revenue multiple of 6.4x across 1 comparables"],
        citations=["Mock dataset (Yahoo Finance API in production)"],
        explanation="Basis AI was valued at $63.8M using a mean EV/Revenue multiple of 6.4x.",
    )
    assert report.fair_value_mm == 63.8
    assert len(report.comps_used) == 1
