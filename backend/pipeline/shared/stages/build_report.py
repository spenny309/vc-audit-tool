from pipeline.stage import Stage
from schemas.context import CompsContext
from schemas.report import ValuationReport


class BuildReportStage(Stage[CompsContext]):
    def execute(self, context: CompsContext) -> CompsContext:
        explanation = (
            f"{context.company_name} was valued at ${context.fair_value_mm}M "
            f"using a mean EV/Revenue multiple of {context.mean_revenue_multiple}x "
            f"applied to ${context.revenue_mm:.1f}M LTM revenue, "
            f"derived from {len(context.comps)} {context.sector.value} comparables."
        )

        context.report = ValuationReport(
            company_name=context.company_name,
            methodology="Comparable Company Analysis",
            fair_value_mm=context.fair_value_mm,
            mean_revenue_multiple=context.mean_revenue_multiple,
            comps_used=context.comps,
            assumptions=context.assumptions,
            citations=context.citations,
            explanation=explanation,
        )
        return context
