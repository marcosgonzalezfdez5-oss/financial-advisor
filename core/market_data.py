from datetime import datetime, timezone
from typing import Any

import yfinance as yf

from schemas.recommendation import MarketDataSnapshot


def fetch_snapshot(ticker: str) -> MarketDataSnapshot:
    info: dict[str, Any] = yf.Ticker(ticker).info
    return MarketDataSnapshot(
        ticker=ticker,
        price=info.get("currentPrice") or info.get("regularMarketPrice"),
        pe_ratio=info.get("trailingPE"),
        dividend_yield=info.get("dividendYield"),
        week_52_high=info.get("fiftyTwoWeekHigh"),
        week_52_low=info.get("fiftyTwoWeekLow"),
        market_cap=info.get("marketCap"),
        volume=info.get("regularMarketVolume"),
        fetched_at=datetime.now(timezone.utc),
    )


def fetch_snapshots(tickers: list[str]) -> dict[str, MarketDataSnapshot]:
    return {ticker: fetch_snapshot(ticker) for ticker in tickers}
