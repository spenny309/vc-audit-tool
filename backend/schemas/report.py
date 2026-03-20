from typing import Optional
from pydantic import BaseModel


class RawCompData(BaseModel):
    name: str
    enterprise_value_mm: float
    revenue_mm: float


class CompData(BaseModel):
    name: str
    enterprise_value_mm: float
    revenue_mm: float
    revenue_multiple: float


class DcfYearData(BaseModel):
    year: int                    # 1-indexed: Year 1, Year 2, ..., Year 5
    revenue_mm: float
    fcf_mm: float                # revenue_mm × ebitda_margin_pct
    discounted_fcf_mm: float     # fcf_mm / (1 + discount_rate) ^ year


class ValuationReport(BaseModel):
    # Common — always populated
    company_name: str
    methodology: str
    fair_value_mm: float
    assumptions: list[str]
    citations: list[str]
    explanation: str

    # Comps-specific — None for DCF reports
    mean_revenue_multiple: Optional[float] = None
    comps_used: Optional[list[CompData]] = None

    # DCF-specific — None for Comps reports
    dcf_cashflows: Optional[list[DcfYearData]] = None
    terminal_value_mm: Optional[float] = None    # discounted terminal value
    ebitda_margin_pct: Optional[float] = None
    discount_rate: Optional[float] = None
    terminal_growth_rate: Optional[float] = None
