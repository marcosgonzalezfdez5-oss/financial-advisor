import pytest

from core.allowlist import AllowlistViolationError, validate_portfolio, validate_ticker


def test_valid_ticker_passes() -> None:
    assert validate_ticker("VOO") == "VOO"


def test_invalid_ticker_raises() -> None:
    with pytest.raises(AllowlistViolationError):
        validate_ticker("DOGE")


def test_crypto_rejected() -> None:
    with pytest.raises(AllowlistViolationError):
        validate_ticker("BTC")


def test_leveraged_etf_rejected() -> None:
    with pytest.raises(AllowlistViolationError):
        validate_ticker("TQQQ")


def test_valid_portfolio_passes() -> None:
    holdings = [{"ticker": "VOO"}, {"ticker": "AAPL"}]
    assert validate_portfolio(holdings) == holdings


def test_invalid_portfolio_raises() -> None:
    holdings = [{"ticker": "VOO"}, {"ticker": "SHIB"}]
    with pytest.raises(AllowlistViolationError):
        validate_portfolio(holdings)
