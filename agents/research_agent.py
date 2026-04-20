import logging

from agents.state import AgentState
from core.allowlist import ALLOWED_TICKERS
from core.candidate_selector import select_candidates
from core.market_data import fetch_snapshot
from schemas.recommendation import MarketDataSnapshot

logger = logging.getLogger(__name__)


def run_research_agent(state: AgentState) -> AgentState:
    profile = state["investor_profile"]
    if profile is None:
        return {**state, "errors": state["errors"] + ["ResearchAgent: no investor_profile in state"]}

    candidates = select_candidates(profile)
    # Hard filter — only tickers in the approved universe ever reach yfinance
    safe_candidates = [t for t in candidates if t in ALLOWED_TICKERS]

    logger.info("ResearchAgent: fetching data for %d candidates: %s", len(safe_candidates), safe_candidates)

    market_data: dict[str, MarketDataSnapshot] = {}
    fetch_errors: list[str] = []

    for ticker in safe_candidates:
        try:
            snapshot = fetch_snapshot(ticker)
            if snapshot.price is not None:
                market_data[ticker] = snapshot
            else:
                logger.warning("ResearchAgent: no price data for %s — skipping", ticker)
        except Exception as exc:
            msg = f"ResearchAgent: failed to fetch {ticker}: {exc}"
            logger.warning(msg)
            fetch_errors.append(msg)

    if not market_data:
        return {
            **state,
            "errors": state["errors"] + ["ResearchAgent: no market data could be fetched"] + fetch_errors,
        }

    logger.info("ResearchAgent: fetched data for %d assets", len(market_data))

    return {
        **state,
        "market_data": market_data,
        "errors": state["errors"] + fetch_errors,
    }
