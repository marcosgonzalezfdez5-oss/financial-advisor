ALLOWED_TICKERS: frozenset[str] = frozenset({
    # US ETFs
    "SPY", "VOO", "QQQ", "VTI", "VXUS", "IEFA", "VGK", "IWM",
    "XLV", "XLF", "SCHD", "VYM",
    # US Blue-Chip
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "GOOG",
    "JNJ", "PG", "V", "JPM", "BRK-B",
    # European Blue-Chip
    "ASML", "NVO", "SAP", "NESN.SW", "MC.PA", "SIE.DE",
})


class AllowlistViolationError(ValueError):
    pass


def validate_ticker(ticker: str) -> str:
    if ticker.upper() not in ALLOWED_TICKERS:
        raise AllowlistViolationError(
            f"Ticker '{ticker}' is not in the approved asset universe. "
            "Only ETFs and blue-chip stocks are permitted."
        )
    return ticker.upper()


def validate_portfolio(holdings: list[dict]) -> list[dict]:
    for holding in holdings:
        validate_ticker(holding["ticker"])
    return holdings
