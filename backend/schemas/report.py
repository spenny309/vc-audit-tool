from __future__ import annotations
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


class CompsDetails(BaseModel):
    mean_revenue_multiple: float
    comps_used: list[CompData]


class DcfDetails(BaseModel):
    dcf_cashflows: list[DcfYearData]
    terminal_value_mm: float
    ebitda_margin_pct: float
    discount_rate: float
    terminal_growth_rate: float


class LastRoundDetails(BaseModel):
    last_post_money_valuation_mm: float
    last_round_date: str
    index_name: str
    index_value_at_round: float
    index_value_today: float
    index_pct_change: float


class ValuationReport(BaseModel):
    # Common — always populated
    company_name: str
    methodology: str
    fair_value_mm: float
    assumptions: list[str]
    citations: list[str]
    explanation: str

    # Model-specific — exactly one is populated per report
    comps_details: Optional[CompsDetails] = None
    dcf_details: Optional[DcfDetails] = None
    last_round_details: Optional[LastRoundDetails] = None
