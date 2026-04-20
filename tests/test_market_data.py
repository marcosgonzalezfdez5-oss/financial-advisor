from unittest.mock import MagicMock, patch

from core.market_data import fetch_snapshot


def test_fetch_snapshot_returns_snapshot() -> None:
    mock_info = {
        "currentPrice": 480.50,
        "trailingPE": 24.5,
        "dividendYield": 0.013,
        "fiftyTwoWeekHigh": 510.0,
        "fiftyTwoWeekLow": 380.0,
        "marketCap": 40_000_000_000,
        "regularMarketVolume": 5_000_000,
    }
    with patch("core.market_data.yf.Ticker") as mock_ticker:
        mock_ticker.return_value.info = mock_info
        snapshot = fetch_snapshot("VOO")

    assert snapshot.ticker == "VOO"
    assert snapshot.price == 480.50
    assert snapshot.pe_ratio == 24.5
    assert snapshot.fetched_at is not None


def test_fetch_snapshot_handles_missing_fields() -> None:
    with patch("core.market_data.yf.Ticker") as mock_ticker:
        mock_ticker.return_value.info = {}
        snapshot = fetch_snapshot("VOO")

    assert snapshot.ticker == "VOO"
    assert snapshot.price is None
