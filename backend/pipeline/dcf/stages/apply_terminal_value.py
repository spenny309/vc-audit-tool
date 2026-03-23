from pipeline.stage import Stage
from schemas.dcf_context import DcfContext


class DcfApplyTerminalValueStage(Stage[DcfContext]):
    def execute(self, context: DcfContext) -> DcfContext:
        discount_rate = context.discount_rate
        growth_rate = context.terminal_growth_rate
        terminal_year_fcf_mm = context.cashflows[4].fcf_mm
        undiscounted_terminal_value_mm = terminal_year_fcf_mm * (1 + growth_rate) / (discount_rate - growth_rate)
        context.terminal_value_mm = undiscounted_terminal_value_mm / (1 + discount_rate) ** 5
        sum_discounted_fcf_mm = sum(cashflow.discounted_fcf_mm for cashflow in context.cashflows)
        context.fair_value_mm = sum_discounted_fcf_mm + context.terminal_value_mm
        growth_rate_pct = growth_rate * 100
        context.assumptions.append(
            f"Discounted terminal value of ${context.terminal_value_mm:.2f}M calculated using Gordon Growth Model "
            f"at {growth_rate_pct:.1f}% perpetual growth rate"
        )
        return context
