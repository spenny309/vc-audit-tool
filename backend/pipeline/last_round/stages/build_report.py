from pipeline.stage import Stage
from schemas.last_round_context import LastRoundContext
from schemas.report import ValuationReport, LastRoundDetails


class LastRoundBuildReportStage(Stage[LastRoundContext]):
    def execute(self, context: LastRoundContext) -> LastRoundContext:
        index_name = context.index.value
        pct = context.index_pct_change * 100
        explanation = (
            f"{context.company_name} was valued at ${context.fair_value_mm:.2f}M, "
            f"starting from a last post-money valuation of "
            f"${context.last_post_money_valuation_mm:.2f}M "
            f"(round date: {context.last_round_date}) "
            f"and adjusting by {pct:+.1f}% to reflect {index_name} performance over that period."
        )
        context.report = ValuationReport(
            company_name=context.company_name,
            methodology="Last Round (Market-Adjusted)",
            fair_value_mm=context.fair_value_mm,
            explanation=explanation,
            assumptions=context.assumptions,
            citations=context.citations,
            last_round_details=LastRoundDetails(
                last_post_money_valuation_mm=context.last_post_money_valuation_mm,
                last_round_date=context.last_round_date,
                index_name=index_name,
                index_value_at_round=context.index_value_at_round,
                index_value_today=context.index_value_today,
                index_pct_change=context.index_pct_change,
            ),
        )
        return context
