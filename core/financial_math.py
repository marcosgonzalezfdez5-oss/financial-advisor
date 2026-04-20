import statistics


def sharpe_ratio(returns: list[float], risk_free_rate: float = 0.04) -> float | None:
    if len(returns) < 2:
        return None
    mean_return = statistics.mean(returns)
    std_dev = statistics.stdev(returns)
    if std_dev == 0:
        return None
    return (mean_return - risk_free_rate) / std_dev


def portfolio_concentration(weights: dict[str, float]) -> float:
    """Herfindahl-Hirschman Index — higher means more concentrated."""
    return sum(w ** 2 for w in weights.values())
