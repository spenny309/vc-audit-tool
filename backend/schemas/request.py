from enum import Enum
from typing import Optional
from pydantic import BaseModel, model_validator


class ModelType(str, Enum):
    COMPS = "Comps"
    DCF = "DCF"


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
    model: ModelType

    # Comps fields — required when model=COMPS
    sector: Optional[Sector] = None
    revenue_mm: Optional[float] = None

    # DCF fields — required when model=DCF
    projections: Optional[list[float]] = None   # exactly 5 values, all > 0
    ebitda_margin_pct: Optional[float] = None   # 0 < x < 1
    discount_rate: Optional[float] = None       # 0 < x < 1
    terminal_growth_rate: Optional[float] = None  # 0 < x < 1, must be < discount_rate

    @model_validator(mode="after")
    def validate_model_fields(self) -> "ValuationRequest":
        if self.model == ModelType.COMPS:
            if self.sector is None:
                raise ValueError("sector is required for Comps model")
            if self.revenue_mm is None or self.revenue_mm <= 0:
                raise ValueError("revenue_mm must be greater than 0 for Comps model")
        if self.model == ModelType.DCF:
            if self.projections is None or len(self.projections) != 5:
                raise ValueError("projections must be a list of exactly 5 values")
            if any(p <= 0 for p in self.projections):
                raise ValueError("all projection values must be greater than 0")
            if self.ebitda_margin_pct is None or not (0 < self.ebitda_margin_pct < 1):
                raise ValueError("ebitda_margin_pct must be between 0 and 1 (exclusive)")
            if self.discount_rate is None or not (0 < self.discount_rate < 1):
                raise ValueError("discount_rate must be between 0 and 1 (exclusive)")
            if self.terminal_growth_rate is None or not (0 < self.terminal_growth_rate < 1):
                raise ValueError("terminal_growth_rate must be between 0 and 1 (exclusive)")
            if self.terminal_growth_rate >= self.discount_rate:
                raise ValueError("terminal_growth_rate must be less than discount_rate")
        return self
