from pipeline.stage import Stage
from schemas.last_round_context import LastRoundContext
from models.exceptions import CalculationError


class LastRoundApplyAdjustmentStage(Stage[LastRoundContext]):
    def execute(self, context: LastRoundContext) -> LastRoundContext:
        if context.index_value_at_round is None or context.index_value_today is None:
            raise CalculationError(
                "Index values are missing; cannot compute adjustment"
            )
        index_pct_change = (
            (context.index_value_today - context.index_value_at_round)
            / context.index_value_at_round
        )
        context.index_pct_change = index_pct_change
        context.fair_value_mm = context.last_post_money_valuation_mm * (1 + index_pct_change)
        index_name = context.index.value
        context.assumptions.append(
            f"{index_name} moved {index_pct_change * 100:+.1f}% from round date to today; "
            f"applied to last post-money valuation of ${context.last_post_money_valuation_mm:.2f}M"
        )
        return context
