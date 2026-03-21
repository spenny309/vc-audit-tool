from models.exceptions import ValuationError, CalculationError
from pipeline.pipeline import Pipeline
from pipeline.dcf.stages.ingest import DcfIngestStage
from pipeline.dcf.stages.project_cashflows import DcfProjectCashflowsStage
from pipeline.dcf.stages.discount_cashflows import DcfDiscountCashflowsStage
from pipeline.dcf.stages.apply_terminal_value import DcfApplyTerminalValueStage
from pipeline.dcf.stages.build_report import DcfBuildReportStage
from schemas.dcf_context import DcfContext
from schemas.report import ValuationReport


class DcfPipeline(Pipeline[DcfContext]):
    def __init__(self) -> None:
        self._stages = [
            DcfIngestStage(),
            DcfProjectCashflowsStage(),
            DcfDiscountCashflowsStage(),
            DcfApplyTerminalValueStage(),
            DcfBuildReportStage(),
        ]

    def execute(self, context: DcfContext) -> ValuationReport:
        try:
            for stage in self._stages:
                context = stage.execute(context)
            return context.report
        except ValuationError:
            raise
        except Exception as e:
            raise CalculationError(f"Unexpected pipeline error: {e}") from e
