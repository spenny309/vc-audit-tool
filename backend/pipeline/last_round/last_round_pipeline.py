from pipeline.pipeline import Pipeline
from pipeline.last_round.stages.ingest import LastRoundIngestStage
from pipeline.last_round.stages.fetch_index import LastRoundFetchIndexStage
from pipeline.last_round.stages.apply_adjustment import LastRoundApplyAdjustmentStage
from pipeline.last_round.stages.build_report import LastRoundBuildReportStage
from schemas.last_round_context import LastRoundContext


class LastRoundPipeline(Pipeline[LastRoundContext]):
    def __init__(self) -> None:
        super().__init__([
            LastRoundIngestStage(),
            LastRoundFetchIndexStage(),
            LastRoundApplyAdjustmentStage(),
            LastRoundBuildReportStage(),
        ])
