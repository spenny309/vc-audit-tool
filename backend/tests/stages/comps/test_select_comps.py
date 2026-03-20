import pytest
import data.mock_comps as mock_comps_module
from schemas.request import Sector
from schemas.context import CompsContext
from schemas.report import RawCompData
from pipeline.comps.stages.select_comps import SelectCompsStage
from models.exceptions import InsufficientDataError, NoCompsFoundError


def make_context(sector=Sector.SAAS):
    return CompsContext(company_name="Modus", sector=sector, revenue_mm=10.0)


def test_populates_raw_comps_for_known_sector():
    ctx = make_context(Sector.SAAS)
    result = SelectCompsStage().execute(ctx)
    assert len(result.raw_comps) >= 2
    assert all(isinstance(c, RawCompData) for c in result.raw_comps)


def test_raw_comps_have_correct_fields():
    ctx = make_context(Sector.SAAS)
    result = SelectCompsStage().execute(ctx)
    for comp in result.raw_comps:
        assert comp.enterprise_value_mm > 0
        assert comp.revenue_mm > 0


def test_appends_assumption_and_citation():
    ctx = make_context(Sector.SAAS)
    result = SelectCompsStage().execute(ctx)
    assert any("comparables" in a for a in result.assumptions)
    assert any("Mock dataset" in c for c in result.citations)


def test_raises_no_comps_found_error_for_missing_sector(monkeypatch):
    monkeypatch.setattr(mock_comps_module, "MOCK_COMPS", {})
    with pytest.raises(NoCompsFoundError):
        SelectCompsStage().execute(make_context(Sector.SAAS))


def test_raises_insufficient_data_error_for_too_few_comps(monkeypatch):
    monkeypatch.setattr(mock_comps_module, "MOCK_COMPS", {Sector.SAAS: [
        {"name": "OnlyOne", "enterprise_value_mm": 100, "revenue_mm": 10}
    ]})
    with pytest.raises(InsufficientDataError):
        SelectCompsStage().execute(make_context(Sector.SAAS))
