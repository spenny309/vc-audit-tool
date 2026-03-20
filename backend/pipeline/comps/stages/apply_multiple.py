from pipeline.stage import Stage
from schemas.context import CompsContext


class ApplyMultipleStage(Stage[CompsContext]):
    def execute(self, context: CompsContext) -> CompsContext:
        context.fair_value_mm = round(
            context.revenue_mm * context.mean_revenue_multiple, 2
        )
        context.assumptions.append(
            f"Mean multiple of {context.mean_revenue_multiple}x "
            f"applied to ${context.revenue_mm:.1f}M LTM revenue"
        )
        return context
