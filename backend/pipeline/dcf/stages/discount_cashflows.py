from pipeline.stage import Stage
from schemas.dcf_context import DcfContext
from schemas.report import DcfYearData


class DcfDiscountCashflowsStage(Stage[DcfContext]):
    def execute(self, context: DcfContext) -> DcfContext:
        r = context.discount_rate
        discounted = []
        for item in context.cashflows:
            discounted_fcf_mm = round(item.fcf_mm / (1 + r) ** item.year, 2)
            discounted.append(DcfYearData(
                year=item.year,
                revenue_mm=item.revenue_mm,
                fcf_mm=item.fcf_mm,
                discounted_fcf_mm=discounted_fcf_mm,
            ))
        context.cashflows = discounted
        rate = context.discount_rate * 100
        context.assumptions.append(f"Cash flows discounted at {rate:.1f}% WACC")
        return context
