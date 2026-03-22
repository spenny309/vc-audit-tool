from models.valuation_model import ValuationModel
from pipeline.pipeline import Pipeline
from pipeline.last_round.last_round_pipeline import LastRoundPipeline
from schemas.last_round_context import LastRoundContext
from schemas.report import ValuationReport
from schemas.request import LastRoundRequest


class LastRoundModel(ValuationModel[LastRoundRequest]):
    def __init__(self, pipeline: Pipeline[LastRoundContext] | None = None) -> None:
        self._pipeline = pipeline or LastRoundPipeline()

    def run(self, request: LastRoundRequest) -> ValuationReport:
        context = LastRoundContext(
            company_name=request.company_name,
            last_post_money_valuation_mm=request.last_post_money_valuation_mm,
            last_round_date=request.last_round_date,
            index=request.index,
        )
        return self._pipeline.execute(context)
