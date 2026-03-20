from pipeline.stage import Stage
from schemas.context import CompsContext


class CompsIngestStage(Stage[CompsContext]):
    def execute(self, context: CompsContext) -> CompsContext:
        context.company_name = context.company_name.strip()
        context.assumptions.append(
            f"Target company: {context.company_name}, "
            f"Sector: {context.sector.value}, "
            f"LTM Revenue: ${context.revenue_mm}M"
        )
        return context
