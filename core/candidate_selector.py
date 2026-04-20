from schemas.investor import GrowthVsValue, InvestorProfile, RiskTolerance

# Asset universe mapped by region, sector, and style
_US_BROAD_ETFS = ["VOO", "SPY", "VTI"]
_US_GROWTH_ETFS = ["QQQ"]
_US_INCOME_ETFS = ["SCHD", "VYM"]
_US_SECTOR_ETFS: dict[str, list[str]] = {
    "Technology": ["QQQ"],
    "Healthcare": ["XLV"],
    "Financials": ["XLF"],
}

_EUROPE_ETFS = ["VGK", "IEFA", "VXUS"]

_US_BLUE_CHIPS: dict[str, list[str]] = {
    "Technology": ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL"],
    "Healthcare": ["JNJ"],
    "Financials": ["V", "JPM"],
    "Consumer": ["PG"],
}

_EUROPE_BLUE_CHIPS: dict[str, list[str]] = {
    "Technology": ["ASML", "SAP"],
    "Healthcare": ["NVO"],
    "Consumer": ["NESN.SW"],
    "Industrials": ["SIE.DE"],
}

# Maximum candidate count — keeps API calls manageable
_MAX_CANDIDATES = 12


def select_candidates(profile: InvestorProfile) -> list[str]:
    candidates: set[str] = set()
    regions = [r.upper() for r in profile.preferred_regions]
    sectors = [s.title() for s in profile.preferred_sectors]

    # Always include broad US ETF as core holding
    candidates.update(_US_BROAD_ETFS[:2])

    # Add income ETFs if dividend preference
    if profile.dividend_preference:
        candidates.update(_US_INCOME_ETFS)

    # Add growth ETF for non-conservative profiles
    if profile.risk_tolerance in (RiskTolerance.MEDIUM, RiskTolerance.HIGH):
        if profile.growth_vs_value in (GrowthVsValue.GROWTH, GrowthVsValue.BALANCED):
            candidates.update(_US_GROWTH_ETFS)

    # Regional exposure
    if "EUROPE" in regions or "EU" in regions:
        candidates.update(_EUROPE_ETFS[:2])

    # Sector ETFs
    for sector in sectors:
        if sector in _US_SECTOR_ETFS:
            candidates.update(_US_SECTOR_ETFS[sector])

    # Blue-chip stocks — conservative profiles get fewer individual stocks
    stock_budget = 2 if profile.risk_tolerance == RiskTolerance.LOW else 4

    us_stocks: list[str] = []
    if sectors:
        for sector in sectors:
            us_stocks.extend(_US_BLUE_CHIPS.get(sector, []))
    if not us_stocks:
        us_stocks = _US_BLUE_CHIPS["Technology"][:2]

    candidates.update(us_stocks[:stock_budget])

    if "EUROPE" in regions or "EU" in regions:
        eu_stocks: list[str] = []
        for sector in (sectors or ["Technology", "Healthcare"]):
            eu_stocks.extend(_EUROPE_BLUE_CHIPS.get(sector, []))
        candidates.update(eu_stocks[:2])

    return list(candidates)[:_MAX_CANDIDATES]
