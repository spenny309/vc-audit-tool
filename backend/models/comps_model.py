from pipeline.comps.comps_pipeline import CompsPipeline
from pipeline.pipeline import Pipeline
from models.valuation_model import ValuationModel
from schemas.comps_context import CompsContext
from schemas.report import ValuationReport
from schemas.request import CompsRequest


class CompsModel(ValuationModel[CompsRequest]):
    def __init__(self, pipeline: Pipeline[CompsContext] | None = None) -> None:
        self._pipeline = pipeline or CompsPipeline()

    def run(self, request: CompsRequest) -> ValuationReport:
        context = CompsContext(
            company_name=request.company_name,
            sector=request.sector,
            revenue_mm=request.revenue_mm,
        )
        return self._pipeline.execute(context)
