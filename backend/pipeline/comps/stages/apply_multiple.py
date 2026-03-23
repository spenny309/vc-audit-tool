from pipeline.stage import Stage
from schemas.comps_context import CompsContext


class CompsApplyMultipleStage(Stage[CompsContext]):
    def execute(self, context: CompsContext) -> CompsContext:
        context.fair_value_mm = context.revenue_mm * context.mean_revenue_multiple
        context.assumptions.append(
            f"Mean multiple of {context.mean_revenue_multiple:.2f}x "
            f"applied to ${context.revenue_mm:.2f}M LTM revenue"
        )
        return context
