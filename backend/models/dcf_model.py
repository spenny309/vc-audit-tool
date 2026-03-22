from pipeline.dcf.dcf_pipeline import DcfPipeline
from pipeline.pipeline import Pipeline
from models.valuation_model import ValuationModel
from schemas.dcf_context import DcfContext
from schemas.report import ValuationReport
from schemas.request import DcfRequest


class DcfModel(ValuationModel[DcfRequest]):
    def __init__(self, pipeline: Pipeline[DcfContext] | None = None) -> None:
        self._pipeline = pipeline or DcfPipeline()

    def run(self, request: DcfRequest) -> ValuationReport:
        context = DcfContext(
            company_name=request.company_name,
            projections=request.projections,
            ebitda_margin_pct=request.ebitda_margin_pct,
            discount_rate=request.discount_rate,
            terminal_growth_rate=request.terminal_growth_rate,
        )
        return self._pipeline.execute(context)
