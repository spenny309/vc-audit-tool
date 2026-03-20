from schemas.request import Sector, ValuationRequest
from schemas.report import ValuationReport, CompData
from models.comps_model import CompsModel
from pipeline.pipeline import Pipeline
from schemas.context import CompsContext


CANNED_REPORT = ValuationReport(
    company_name="Basis AI",
    methodology="Comparable Company Analysis",
    fair_value_mm=80.0,
    mean_revenue_multiple=8.0,
    comps_used=[
        CompData(name="Salesforce", enterprise_value_mm=200_000, revenue_mm=31_352, revenue_multiple=6.38)
    ],
    assumptions=["Mean EV/Revenue multiple of 8.0x across 1 comparables"],
    citations=["Mock dataset"],
    explanation="Basis AI was valued at $80.0M.",
)


class MockPipeline(Pipeline[CompsContext]):
    def execute(self, context: CompsContext) -> ValuationReport:
        return CANNED_REPORT


def test_model_delegates_to_pipeline():
    model = CompsModel(pipeline=MockPipeline())
    request = ValuationRequest(company_name="Basis AI", sector=Sector.SAAS, revenue_mm=10.0)
    report = model.run(request)
    assert report == CANNED_REPORT


def test_model_passes_correct_context_to_pipeline():
    captured = {}

    class CapturingPipeline(Pipeline[CompsContext]):
        def execute(self, context: CompsContext) -> ValuationReport:
            captured["context"] = context
            return CANNED_REPORT

    request = ValuationRequest(company_name="Basis AI", sector=Sector.SAAS, revenue_mm=10.0)
    CompsModel(pipeline=CapturingPipeline()).run(request)

    ctx = captured["context"]
    assert ctx.company_name == "Basis AI"
    assert ctx.sector == Sector.SAAS
    assert ctx.revenue_mm == 10.0


def test_model_uses_comps_pipeline_by_default():
    from pipeline.comps.comps_pipeline import CompsPipeline
    model = CompsModel()
    assert isinstance(model._pipeline, CompsPipeline)
