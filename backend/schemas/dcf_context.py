from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.report import DcfYearData, ValuationReport


@dataclass
class DcfContext:
    # Set at construction (from ValuationRequest)
    company_name: str
    projections: list[float]         # 5 annual revenue projections in $M (index 0 = Year 1)
    ebitda_margin_pct: float
    discount_rate: float
    terminal_growth_rate: float

    # Set by DcfProjectCashflowsStage + DcfDiscountCashflowsStage
    cashflows: list[DcfYearData] = field(default_factory=list)

    # Set by DcfApplyTerminalValueStage
    terminal_value_mm: Optional[float] = None
    fair_value_mm: Optional[float] = None

    # Set by DcfBuildReportStage
    report: Optional[ValuationReport] = None

    # Accumulated throughout
    assumptions: list[str] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)
