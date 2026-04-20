from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    profile_id: UUID


class MarketDataSnapshot(BaseModel):
    ticker: str
    price: float | None = None
    pe_ratio: float | None = None
    dividend_yield: float | None = None
    week_52_high: float | None = None
    week_52_low: float | None = None
    market_cap: float | None = None
    volume: int | None = None
    fetched_at: datetime


class PortfolioHolding(BaseModel):
    ticker: str
    allocation_pct: float = Field(ge=0, le=100)
    rationale: str
    data_fetched_at: datetime


class PortfolioDraft(BaseModel):
    holdings: list[PortfolioHolding]
    total_allocation_pct: float


class UncertaintyReport(BaseModel):
    data_freshness: str
    caveats: list[str] = Field(default=[])
    disclaimer: str = (
        "This is not financial advice. "
        "Past performance does not guarantee future results. "
        "Consult a licensed financial advisor before making investment decisions."
    )


class FinalRecommendation(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    profile_id: UUID
    portfolio: list[PortfolioHolding]
    risk_summary: str
    alternatives: list[str] = Field(default=[])
    uncertainty: UncertaintyReport
    created_at: datetime


class RecommendationResponse(FinalRecommendation):
    pass
