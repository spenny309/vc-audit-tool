import data.mock_comps as mock_comps
from models.exceptions import NoCompsFoundError, InsufficientDataError
from pipeline.stage import Stage
from schemas.comps_context import CompsContext
from schemas.report import RawCompData


class CompsSelectStage(Stage[CompsContext]):
    def execute(self, context: CompsContext) -> CompsContext:
        raw = mock_comps.MOCK_COMPS.get(context.sector)

        if raw is None:
            raise NoCompsFoundError(
                f"No comparable companies found for sector '{context.sector.value}'"
            )

        context.raw_comps = [RawCompData(**entry) for entry in raw]

        if len(context.raw_comps) < mock_comps.MIN_COMPS:
            raise InsufficientDataError(
                f"Found {len(context.raw_comps)} comparable(s) for sector "
                f"'{context.sector.value}', minimum required is {mock_comps.MIN_COMPS}"
            )

        context.assumptions.append(
            f"Selected {len(context.raw_comps)} {context.sector.value} comparables"
        )
        context.citations.append("Mock dataset (Yahoo Finance API in production)")
        return context
