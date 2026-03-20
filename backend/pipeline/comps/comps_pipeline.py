from models.exceptions import ValuationError, CalculationError
from pipeline.pipeline import Pipeline
from pipeline.comps.stages.ingest import CompsIngestStage
from pipeline.comps.stages.select_comps import SelectCompsStage
from pipeline.comps.stages.calculate_multiple import CalculateMultipleStage
from pipeline.comps.stages.apply_multiple import ApplyMultipleStage
from pipeline.shared.stages.build_report import BuildReportStage
from schemas.context import CompsContext
from schemas.report import ValuationReport


class CompsPipeline(Pipeline[CompsContext]):
    def __init__(self) -> None:
        self._stages = [
            CompsIngestStage(),
            SelectCompsStage(),
            CalculateMultipleStage(),
            ApplyMultipleStage(),
            BuildReportStage(),
        ]

    def execute(self, context: CompsContext) -> ValuationReport:
        try:
            for stage in self._stages:
                context = stage.execute(context)
            return context.report
        except ValuationError:
            raise
        except Exception as e:
            raise CalculationError(f"Unexpected pipeline error: {e}") from e
