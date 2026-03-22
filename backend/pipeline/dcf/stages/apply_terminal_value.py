from pipeline.stage import Stage
from schemas.dcf_context import DcfContext


class DcfApplyTerminalValueStage(Stage[DcfContext]):
    def execute(self, context: DcfContext) -> DcfContext:
        r = context.discount_rate
        g = context.terminal_growth_rate
        fcf_5 = context.cashflows[4].fcf_mm
        undiscounted_tv = fcf_5 * (1 + g) / (r - g)
        context.terminal_value_mm = round(undiscounted_tv / (1 + r) ** 5, 2)
        sum_discounted = sum(item.discounted_fcf_mm for item in context.cashflows)
        context.fair_value_mm = round(sum_discounted + context.terminal_value_mm, 2)
        tv = context.terminal_value_mm
        g_pct = g * 100
        context.assumptions.append(
            f"Discounted terminal value of ${tv:.2f}M calculated using Gordon Growth Model "
            f"at {g_pct:.1f}% perpetual growth rate"
        )
        return context
