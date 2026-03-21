import pytest
from pipeline.dcf.stages.ingest import DcfIngestStage
from schemas.dcf_context import DcfContext


@pytest.fixture
def context():
    return DcfContext(
        company_name="  Alpha  ",
        projections=[10.0, 11.0, 12.0, 13.0, 14.0],
        ebitda_margin_pct=0.20,
        discount_rate=0.15,
        terminal_growth_rate=0.03,
    )


def test_ingest_strips_company_name(context):
    stage = DcfIngestStage()
    result = stage.execute(context)
    assert result.company_name == "Alpha"


def test_ingest_appends_assumption(context):
    stage = DcfIngestStage()
    result = stage.execute(context)
    assert len(result.assumptions) == 1
    assert "Alpha" in result.assumptions[0]
    assert "5-year DCF projection" in result.assumptions[0]


def test_ingest_appends_no_citation(context):
    stage = DcfIngestStage()
    result = stage.execute(context)
    assert len(result.citations) == 0
