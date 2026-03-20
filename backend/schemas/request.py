from enum import Enum
from pydantic import BaseModel, field_validator


class Sector(str, Enum):
    SAAS = "SaaS"
    FINTECH = "FinTech"
    ECOMMERCE = "eCommerce"
    HEALTHTECH = "HealthTech"
    CYBERSECURITY = "Cybersecurity"
    MARTECH = "MarTech"
    EDTECH = "EdTech"
    CLEANTECH = "CleanTech"
    PROPTECH = "PropTech"
    HRTECH = "HRTech"


class ValuationRequest(BaseModel):
    company_name: str
    sector: Sector
    revenue_mm: float

    @field_validator("revenue_mm")
    @classmethod
    def revenue_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("revenue_mm must be greater than 0")
        return value
