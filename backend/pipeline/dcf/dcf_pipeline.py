from pipeline.pipeline import Pipeline
from pipeline.dcf.stages.ingest import DcfIngestStage
from pipeline.dcf.stages.project_cashflows import DcfProjectCashflowsStage
from pipeline.dcf.stages.discount_cashflows import DcfDiscountCashflowsStage
from pipeline.dcf.stages.apply_terminal_value import DcfApplyTerminalValueStage
from pipeline.dcf.stages.build_report import DcfBuildReportStage
from schemas.dcf_context import DcfContext


class DcfPipeline(Pipeline[DcfContext]):
    def __init__(self) -> None:
        super().__init__([
            DcfIngestStage(),
            DcfProjectCashflowsStage(),
            DcfDiscountCashflowsStage(),
            DcfApplyTerminalValueStage(),
            DcfBuildReportStage(),
        ])
