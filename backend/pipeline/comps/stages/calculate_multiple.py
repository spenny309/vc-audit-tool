from models.exceptions import CalculationError
from pipeline.stage import Stage
from schemas.comps_context import CompsContext
from schemas.report import CompData


class CompsCalculateMultipleStage(Stage[CompsContext]):
    def execute(self, context: CompsContext) -> CompsContext:
        comps = []
        for raw in context.raw_comps:
            if raw.revenue_mm == 0:
                raise CalculationError(
                    f"Comparable '{raw.name}' has zero revenue — cannot compute multiple"
                )
            multiple = raw.enterprise_value_mm / raw.revenue_mm
            comps.append(CompData(
                name=raw.name,
                enterprise_value_mm=raw.enterprise_value_mm,
                revenue_mm=raw.revenue_mm,
                revenue_multiple=round(multiple, 2),
            ))

        context.comps = comps
        context.mean_revenue_multiple = round(
            sum(c.revenue_multiple for c in comps) / len(comps), 2
        )

        context.assumptions.append(
            f"Mean EV/Revenue multiple of {context.mean_revenue_multiple}x "
            f"across {len(comps)} comparables"
        )
        return context
