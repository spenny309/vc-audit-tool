from datetime import date
from pipeline.stage import Stage
from schemas.last_round_context import LastRoundContext


class LastRoundIngestStage(Stage[LastRoundContext]):
    def execute(self, context: LastRoundContext) -> LastRoundContext:
        context.company_name = context.company_name.strip()
        context.last_round_date_parsed = date.fromisoformat(context.last_round_date)
        context.assumptions.append(
            f"Target company: {context.company_name}, "
            f"Last Round (Market-Adjusted) valuation as of {context.last_round_date_parsed}"
        )
        return context
