from pipeline.stage import Stage
from schemas.last_round_context import LastRoundContext
from data.mock_index import get_index_at_date, INDEX_VALUE_TODAY


class LastRoundFetchIndexStage(Stage[LastRoundContext]):
    def execute(self, context: LastRoundContext) -> LastRoundContext:
        index_name = context.index.value
        context.index_value_at_round = get_index_at_date(
            context.index, context.last_round_date_parsed
        )
        context.index_value_today = INDEX_VALUE_TODAY[context.index]
        context.citations.append(
            f"{index_name} index data: mock historical quarterly close prices "
            f"(source: mocked for audit demo)"
        )
        context.assumptions.append(
            f"{index_name} at round date ({context.last_round_date_parsed}): "
            f"{context.index_value_at_round:.2f} (nearest quarterly close)"
        )
        return context
