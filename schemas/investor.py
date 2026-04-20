from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class RiskTolerance(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class GrowthVsValue(StrEnum):
    GROWTH = "growth"
    VALUE = "value"
    BALANCED = "balanced"


class InvestorProfileCreate(BaseModel):
    budget: float = Field(gt=0)
    currency: str = Field(default="USD", max_length=3)
    risk_tolerance: RiskTolerance
    investment_horizon_years: int = Field(ge=1, le=50)
    preferred_regions: list[str] = Field(default=["US"])
    preferred_sectors: list[str] = Field(default=[])
    dividend_preference: bool = False
    growth_vs_value: GrowthVsValue = GrowthVsValue.BALANCED
    esg_preference: bool = False


class InvestorProfile(InvestorProfileCreate):
    id: UUID = Field(default_factory=uuid4)
    investor_type: str | None = None
    contradictions: list[str] = Field(default=[])


class InvestorProfileResponse(InvestorProfile):
    pass
