from schemas.request import Sector
from schemas.context import CompsContext
from pipeline.comps.stages.ingest import CompsIngestStage


def make_context(**kwargs):
    defaults = dict(company_name="Modus", sector=Sector.SAAS, revenue_mm=10.0)
    return CompsContext(**{**defaults, **kwargs})


def test_strips_whitespace_from_company_name():
    ctx = make_context(company_name="  Modus  ")
    result = CompsIngestStage().execute(ctx)
    assert result.company_name == "Modus"


def test_appends_target_to_assumptions():
    ctx = make_context()
    result = CompsIngestStage().execute(ctx)
    assert len(result.assumptions) == 1
    assert "Modus" in result.assumptions[0]
    assert "SaaS" in result.assumptions[0]
    assert "$10.00M" in result.assumptions[0]


def test_revenue_formatted_to_two_decimals():
    ctx = make_context(revenue_mm=15.0)
    result = CompsIngestStage().execute(ctx)
    assert "$15.00M" in result.assumptions[0]


def test_does_not_modify_other_context_fields():
    ctx = make_context()
    result = CompsIngestStage().execute(ctx)
    assert result.raw_comps == []
    assert result.comps == []
    assert result.citations == []
