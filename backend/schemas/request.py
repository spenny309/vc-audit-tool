from __future__ import annotations
from datetime import date as _date
from enum import Enum
from typing import Annotated, Literal, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator


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


class CompsRequest(BaseModel):
    model: Literal["Comps"]
    company_name: str
    sector: Sector
    revenue_mm: float

    @field_validator("revenue_mm")
    @classmethod
    def revenue_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("revenue_mm must be greater than 0")
        return v


class DcfRequest(BaseModel):
    model: Literal["DCF"]
    company_name: str
    projections: list[float]
    ebitda_margin_pct: float
    discount_rate: float
    terminal_growth_rate: float

    @field_validator("projections")
    @classmethod
    def projections_must_have_five_years(cls, v: list[float]) -> list[float]:
        if len(v) != 5:
            raise ValueError("projections must contain exactly 5 annual values")
        if any(p <= 0 for p in v):
            raise ValueError("all projections must be greater than 0")
        return v

    @field_validator("ebitda_margin_pct", "discount_rate", "terminal_growth_rate")
    @classmethod
    def rates_must_be_positive(cls, v: float) -> float:
        if v <= 0 or v >= 1:
            raise ValueError("rate must be between 0 and 1 (exclusive)")
        return v

    @model_validator(mode="after")
    def terminal_growth_must_be_less_than_wacc(self) -> "DcfRequest":
        if self.terminal_growth_rate >= self.discount_rate:
            raise ValueError("terminal_growth_rate must be less than discount_rate (WACC)")
        return self


class LastRoundRequest(BaseModel):
    model: Literal["Last Round"]
    company_name: str
    last_post_money_valuation_mm: float
    last_round_date: str
    index: Optional[IndexType] = None

    @field_validator("last_post_money_valuation_mm")
    @classmethod
    def valuation_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("last_post_money_valuation_mm must be greater than 0")
        return v

    @field_validator("last_round_date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        try:
            parsed = _date.fromisoformat(v)
        except ValueError:
            raise ValueError("last_round_date must be a valid ISO date (YYYY-MM-DD)")
        if parsed > _date.today():
            raise ValueError("last_round_date cannot be in the future")
        if parsed < _date(2015, 1, 1):
            raise ValueError("last_round_date cannot be before 2015-01-01")
        return v

    @model_validator(mode="after")
    def apply_index_default(self) -> "LastRoundRequest":
        if self.index is None:
            self.index = IndexType.NASDAQ
        return self


ValuationRequest = Annotated[
    Union[CompsRequest, DcfRequest, LastRoundRequest],
    Field(discriminator="model")
]
