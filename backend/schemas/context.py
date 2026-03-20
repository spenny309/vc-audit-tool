from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from schemas.request import Sector
from schemas.report import RawCompData, CompData

if TYPE_CHECKING:
    from schemas.report import ValuationReport


@dataclass
class CompsContext:
    # Set at construction
    company_name: str
    sector: Sector
    revenue_mm: float

    # Set at select_comps
    raw_comps: list[RawCompData] = field(default_factory=list)

    # Set at calculate_multiple
    comps: list[CompData] = field(default_factory=list)
    mean_revenue_multiple: Optional[float] = None

    # Set at apply_multiple
    fair_value_mm: Optional[float] = None

    # Set at build_report
    report: Optional[ValuationReport] = None

    # Accumulated throughout
    assumptions: list[str] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)
