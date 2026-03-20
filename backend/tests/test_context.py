from schemas.request import Sector
from schemas.context import CompsContext


def test_comps_context_initializes_with_defaults():
    ctx = CompsContext(company_name="Basis AI", sector=Sector.SAAS, revenue_mm=10.0)
    assert ctx.company_name == "Basis AI"
    assert ctx.raw_comps == []
    assert ctx.comps == []
    assert ctx.mean_revenue_multiple is None
    assert ctx.fair_value_mm is None
    assert ctx.report is None
    assert ctx.assumptions == []
    assert ctx.citations == []


def test_comps_context_assumptions_and_citations_are_independent():
    ctx1 = CompsContext(company_name="A", sector=Sector.SAAS, revenue_mm=1.0)
    ctx2 = CompsContext(company_name="B", sector=Sector.FINTECH, revenue_mm=2.0)
    ctx1.assumptions.append("x")
    assert ctx2.assumptions == []
