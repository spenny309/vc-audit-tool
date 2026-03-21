from pipeline.stage import Stage
from schemas.dcf_context import DcfContext


class DcfIngestStage(Stage[DcfContext]):
    def execute(self, context: DcfContext) -> DcfContext:
        context.company_name = context.company_name.strip()
        context.assumptions.append(
            f"Target company: {context.company_name}, 5-year DCF projection"
        )
        return context
