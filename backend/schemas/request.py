from datetime import date as _date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, model_validator


class ModelType(str, Enum):
    COMPS = "Comps"
    DCF = "DCF"
    LAST_ROUND = "Last Round"


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


class IndexType(str, Enum):
    NASDAQ  = "Nasdaq Composite"
    SP500   = "S&P 500"
    RUSSELL = "Russell 2000"


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

    # Last Round fields — required when model=LAST_ROUND
    last_post_money_valuation_mm: Optional[float] = None
    last_round_date: Optional[str] = None
    index: Optional[IndexType] = None

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
        if self.model == ModelType.LAST_ROUND:
            if self.last_post_money_valuation_mm is None or self.last_post_money_valuation_mm <= 0:
                raise ValueError("last_post_money_valuation_mm must be greater than 0 for Last Round model")
            if self.last_round_date is None:
                raise ValueError("last_round_date is required for Last Round model")
            try:
                parsed = _date.fromisoformat(self.last_round_date)
            except ValueError:
                raise ValueError("last_round_date must be a valid ISO date (YYYY-MM-DD)")
            if parsed > _date.today():
                raise ValueError("last_round_date cannot be in the future")
            if parsed < _date(2015, 1, 1):
                raise ValueError("last_round_date cannot be before 2015-01-01")
            if self.index is None:
                self.index = IndexType.NASDAQ
        return self
