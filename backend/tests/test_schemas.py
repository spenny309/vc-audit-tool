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
