from schemas.request import Sector
from schemas.context import CompsContext
from schemas.report import RawCompData
from pipeline.comps.stages.calculate_multiple import CalculateMultipleStage


def make_context_with_raw_comps():
    ctx = CompsContext(company_name="Basis AI", sector=Sector.SAAS, revenue_mm=10.0)
    ctx.raw_comps = [
        RawCompData(name="A", enterprise_value_mm=100, revenue_mm=10),  # multiple = 10x
        RawCompData(name="B", enterprise_value_mm=200, revenue_mm=10),  # multiple = 20x
        RawCompData(name="C", enterprise_value_mm=300, revenue_mm=10),  # multiple = 30x
    ]
    return ctx


def test_computes_revenue_multiple_per_comp():
    result = CalculateMultipleStage().execute(make_context_with_raw_comps())
    multiples = [c.revenue_multiple for c in result.comps]
    assert multiples == [10.0, 20.0, 30.0]


def test_computes_mean_revenue_multiple():
    result = CalculateMultipleStage().execute(make_context_with_raw_comps())
    assert result.mean_revenue_multiple == 20.0  # (10 + 20 + 30) / 3


def test_populates_comps_with_all_fields():
    result = CalculateMultipleStage().execute(make_context_with_raw_comps())
    assert len(result.comps) == 3
    for comp in result.comps:
        assert comp.name
        assert comp.enterprise_value_mm > 0
        assert comp.revenue_mm > 0
        assert comp.revenue_multiple > 0


def test_appends_assumption():
    result = CalculateMultipleStage().execute(make_context_with_raw_comps())
    assert any("Mean EV/Revenue multiple" in a for a in result.assumptions)
    assert any("20.0x" in a for a in result.assumptions)
