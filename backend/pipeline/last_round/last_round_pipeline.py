from models.exceptions import ValuationError, CalculationError
from pipeline.pipeline import Pipeline
from pipeline.last_round.stages.ingest import LastRoundIngestStage
from pipeline.last_round.stages.fetch_index import LastRoundFetchIndexStage
from pipeline.last_round.stages.apply_adjustment import LastRoundApplyAdjustmentStage
from pipeline.last_round.stages.build_report import LastRoundBuildReportStage
from schemas.last_round_context import LastRoundContext
from schemas.report import ValuationReport


class LastRoundPipeline(Pipeline[LastRoundContext]):
    def __init__(self) -> None:
        self._stages = [
            LastRoundIngestStage(),
            LastRoundFetchIndexStage(),
            LastRoundApplyAdjustmentStage(),
            LastRoundBuildReportStage(),
        ]

    def execute(self, context: LastRoundContext) -> ValuationReport:
        try:
            for stage in self._stages:
                context = stage.execute(context)
            return context.report
        except ValuationError:
            raise
        except Exception as e:
            raise CalculationError(f"Unexpected pipeline error: {e}") from e
