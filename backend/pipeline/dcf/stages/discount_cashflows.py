from pipeline.stage import Stage
from schemas.dcf_context import DcfContext
from schemas.report import DcfYearData


class DcfDiscountCashflowsStage(Stage[DcfContext]):
    def execute(self, context: DcfContext) -> DcfContext:
        discount_rate = context.discount_rate
        discounted_cashflows = []
        for cashflow in context.cashflows:
            discounted_fcf_mm = cashflow.fcf_mm / (1 + discount_rate) ** cashflow.year
            discounted_cashflows.append(DcfYearData(
                year=cashflow.year,
                revenue_mm=cashflow.revenue_mm,
                fcf_mm=cashflow.fcf_mm,
                discounted_fcf_mm=discounted_fcf_mm,
            ))
        context.cashflows = discounted_cashflows
        discount_rate_pct = discount_rate * 100
        context.assumptions.append(f"Cash flows discounted at {discount_rate_pct:.1f}% WACC")
        return context
