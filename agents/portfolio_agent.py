import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import anthropic

from agents.state import AgentState
from config.settings import settings
from core.allowlist import AllowlistViolationError, validate_portfolio
from schemas.recommendation import FinalRecommendation, PortfolioHolding, UncertaintyReport

logger = logging.getLogger(__name__)

_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
_PROMPT_TEMPLATE = (Path(__file__).parent.parent / "prompts" / "portfolio.md").read_text()


def _build_market_data_json(state: AgentState) -> str:
    return json.dumps(
        {
            ticker: {
                "price": snap.price,
                "pe_ratio": snap.pe_ratio,
                "dividend_yield": round(snap.dividend_yield * 100, 2) if snap.dividend_yield else None,
                "week_52_high": snap.week_52_high,
                "week_52_low": snap.week_52_low,
                "market_cap_billions": round(snap.market_cap / 1e9, 1) if snap.market_cap else None,
                "fetched_at": snap.fetched_at.isoformat(),
            }
            for ticker, snap in state["market_data"].items()
        },
        indent=2,
    )


def _parse_holdings(raw: list[dict], market_data_fetched_at: datetime) -> list[PortfolioHolding]:
    return [
        PortfolioHolding(
            ticker=h["ticker"].upper(),
            allocation_pct=float(h["allocation_pct"]),
            rationale=h["rationale"],
            data_fetched_at=market_data_fetched_at,
        )
        for h in raw
    ]


def run_portfolio_agent(state: AgentState) -> AgentState:
    profile = state["investor_profile"]
    market_data = state["market_data"]

    if profile is None:
        return {**state, "errors": state["errors"] + ["PortfolioAgent: no investor_profile in state"]}
    if not market_data:
        return {**state, "errors": state["errors"] + ["PortfolioAgent: no market data in state"]}

    fetched_at = next(iter(market_data.values())).fetched_at
    market_data_json = _build_market_data_json(state)

    prompt = _PROMPT_TEMPLATE.format(
        budget=profile.budget,
        currency=profile.currency,
        investor_type=profile.investor_type or profile.risk_tolerance,
        risk_tolerance=profile.risk_tolerance,
        investment_horizon_years=profile.investment_horizon_years,
        dividend_preference=profile.dividend_preference,
        growth_vs_value=profile.growth_vs_value,
        fetched_at=fetched_at.isoformat(),
        market_data_json=market_data_json,
        asset_assessments_json="{}",
    )

    try:
        response = _client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        parsed = json.loads(text[start:end])
    except Exception as exc:
        return {**state, "errors": state["errors"] + [f"PortfolioAgent: LLM call failed: {exc}"]}

    try:
        validate_portfolio(parsed.get("portfolio", []))
    except AllowlistViolationError as exc:
        return {**state, "errors": state["errors"] + [f"PortfolioAgent: allowlist violation: {exc}"]}

    holdings = _parse_holdings(parsed["portfolio"], fetched_at)

    freshness_minutes = round((datetime.now(timezone.utc) - fetched_at).total_seconds() / 60)
    recommendation = FinalRecommendation(
        profile_id=profile.id,
        portfolio=holdings,
        risk_summary=parsed.get("risk_summary", ""),
        alternatives=parsed.get("alternatives", []),
        uncertainty=UncertaintyReport(
            data_freshness=f"Market data fetched {freshness_minutes} minute(s) ago via Yahoo Finance.",
            caveats=parsed.get("caveats", []),
        ),
        created_at=datetime.now(timezone.utc),
    )

    logger.info(
        "PortfolioAgent: built recommendation with %d holdings for profile %s",
        len(holdings),
        profile.id,
    )

    return {**state, "recommendation": recommendation}
