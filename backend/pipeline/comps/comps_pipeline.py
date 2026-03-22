from pipeline.pipeline import Pipeline
from pipeline.comps.stages.ingest import CompsIngestStage
from pipeline.comps.stages.select_comps import CompsSelectStage
from pipeline.comps.stages.calculate_multiple import CompsCalculateMultipleStage
from pipeline.comps.stages.apply_multiple import CompsApplyMultipleStage
from pipeline.comps.stages.build_report import CompsBuildReportStage
from schemas.comps_context import CompsContext


class CompsPipeline(Pipeline[CompsContext]):
    def __init__(self) -> None:
        super().__init__([
            CompsIngestStage(),
            CompsSelectStage(),
            CompsCalculateMultipleStage(),
            CompsApplyMultipleStage(),
            CompsBuildReportStage(),
        ])
