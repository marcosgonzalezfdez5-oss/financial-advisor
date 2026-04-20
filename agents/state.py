from typing import TypedDict

from schemas.investor import InvestorProfile
from schemas.recommendation import MarketDataSnapshot, PortfolioDraft, FinalRecommendation


class AgentState(TypedDict):
    investor_profile: InvestorProfile | None
    market_data: dict[str, MarketDataSnapshot]
    portfolio_draft: PortfolioDraft | None
    recommendation: FinalRecommendation | None
    errors: list[str]
    requires_human_review: bool
    trace_id: str
