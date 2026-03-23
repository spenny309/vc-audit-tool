from pipeline.stage import Stage
from schemas.dcf_context import DcfContext
from schemas.report import DcfYearData


class DcfProjectCashflowsStage(Stage[DcfContext]):
    def execute(self, context: DcfContext) -> DcfContext:
        for year in range(1, 6):
            revenue_mm = context.projections[year - 1]
            fcf_mm = revenue_mm * context.ebitda_margin_pct
            context.cashflows.append(
                DcfYearData(year=year, revenue_mm=revenue_mm, fcf_mm=fcf_mm, discounted_fcf_mm=0.0)
            )
        ebitda_margin_pct = context.ebitda_margin_pct * 100
        context.assumptions.append(
            f"EBITDA margin of {ebitda_margin_pct:.1f}% applied to revenue projections to derive free cash flow"
        )
        context.citations.append("Projections provided by user")
        return context
