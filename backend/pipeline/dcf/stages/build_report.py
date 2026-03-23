from pipeline.stage import Stage
from schemas.dcf_context import DcfContext
from schemas.report import ValuationReport, DcfDetails


class DcfBuildReportStage(Stage[DcfContext]):
    def execute(self, context: DcfContext) -> DcfContext:
        discount_rate_pct = context.discount_rate * 100
        growth_rate_pct = context.terminal_growth_rate * 100
        explanation = (
            f"{context.company_name} was valued at ${context.fair_value_mm:.2f}M "
            f"using a 5-year DCF with a {discount_rate_pct:.1f}% discount rate and {growth_rate_pct:.1f}% "
            f"terminal growth rate, based on user-provided revenue projections."
        )
        context.report = ValuationReport(
            company_name=context.company_name,
            methodology="Discounted Cash Flow",
            fair_value_mm=context.fair_value_mm,
            assumptions=context.assumptions,
            citations=context.citations,
            explanation=explanation,
            dcf_details=DcfDetails(
                dcf_cashflows=context.cashflows,
                terminal_value_mm=context.terminal_value_mm,
                ebitda_margin_pct=context.ebitda_margin_pct,
                discount_rate=context.discount_rate,
                terminal_growth_rate=context.terminal_growth_rate,
            ),
        )
        return context
