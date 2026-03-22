from schemas.request import Sector
from schemas.comps_context import CompsContext
from pipeline.comps.stages.apply_multiple import CompsApplyMultipleStage


def make_context_with_multiple():
    ctx = CompsContext(company_name="Modus", sector=Sector.SAAS, revenue_mm=10.0)
    ctx.mean_revenue_multiple = 8.0
    return ctx


def test_computes_fair_value():
    result = CompsApplyMultipleStage().execute(make_context_with_multiple())
    assert result.fair_value_mm == 80.0  # 10.0 * 8.0


def test_computes_fair_value_with_decimal_multiple():
    ctx = CompsContext(company_name="X", sector=Sector.SAAS, revenue_mm=15.0)
    ctx.mean_revenue_multiple = 6.5
    result = CompsApplyMultipleStage().execute(ctx)
    assert result.fair_value_mm == 97.5


def test_appends_assumption():
    result = CompsApplyMultipleStage().execute(make_context_with_multiple())
    assert any("8.0x" in a for a in result.assumptions)
    assert any("$10.00M" in a for a in result.assumptions)
