from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional, TYPE_CHECKING

from schemas.request import IndexType

if TYPE_CHECKING:
    from schemas.report import ValuationReport


@dataclass
class LastRoundContext:
    # Set at construction (from ValuationRequest)
    company_name: str
    last_post_money_valuation_mm: float
    last_round_date: str                           # ISO string: "YYYY-MM-DD"
    index: IndexType                               # always set; model applies default

    # Set by IngestStage
    last_round_date_parsed: Optional[date] = None  # parsed datetime.date

    # Set by FetchIndexStage
    index_value_at_round: Optional[float] = None
    index_value_today: Optional[float] = None

    # Set by ApplyAdjustmentStage
    index_pct_change: Optional[float] = None       # e.g. 0.142 = +14.2%
    fair_value_mm: Optional[float] = None

    # Set by BuildReportStage
    report: Optional[ValuationReport] = None

    # Accumulated throughout
    assumptions: list[str] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)
