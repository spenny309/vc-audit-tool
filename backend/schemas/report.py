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


class ValuationReport(BaseModel):
    company_name: str
    methodology: str
    fair_value_mm: float
    mean_revenue_multiple: float
    comps_used: list[CompData]
    assumptions: list[str]
    citations: list[str]
    explanation: str
