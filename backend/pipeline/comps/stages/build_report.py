from pipeline.stage import Stage
from schemas.comps_context import CompsContext
from schemas.report import ValuationReport, CompsDetails


class CompsBuildReportStage(Stage[CompsContext]):
    def execute(self, context: CompsContext) -> CompsContext:
        explanation = (
            f"{context.company_name} was valued at ${context.fair_value_mm:.2f}M "
            f"using a mean EV/Revenue multiple of {context.mean_revenue_multiple:.2f}x "
            f"applied to ${context.revenue_mm:.1f}M LTM revenue, "
            f"derived from {len(context.comps)} {context.sector.value} comparables."
        )

        context.report = ValuationReport(
            company_name=context.company_name,
            methodology="Comparable Company Analysis",
            fair_value_mm=context.fair_value_mm,
            assumptions=context.assumptions,
            citations=context.citations,
            explanation=explanation,
            comps_details=CompsDetails(
                mean_revenue_multiple=context.mean_revenue_multiple,
                comps_used=context.comps,
            ),
        )
        return context
