from data.mock_comps import MOCK_COMPS, MIN_COMPS
from schemas.request import Sector


def test_min_comps_is_defined():
    assert MIN_COMPS == 2


def test_all_sectors_present():
    for sector in Sector:
        assert sector in MOCK_COMPS, f"Missing sector: {sector}"


def test_each_sector_meets_minimum():
    for sector, comps in MOCK_COMPS.items():
        assert len(comps) >= MIN_COMPS, f"{sector} has fewer than {MIN_COMPS} comps"


def test_comp_entries_have_required_fields():
    for sector, comps in MOCK_COMPS.items():
        for comp in comps:
            assert "name" in comp
            assert "enterprise_value_mm" in comp
            assert "revenue_mm" in comp
            assert comp["enterprise_value_mm"] > 0
            assert comp["revenue_mm"] > 0
