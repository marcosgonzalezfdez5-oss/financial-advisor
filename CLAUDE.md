# CLAUDE.md

## Project Name

Investment Research Agent — ETF + Blue Chip Stock Recommendation System

---

# Project Purpose

An AI-powered investment research agent focused exclusively on:

* ETFs
* Blue-chip stocks

for:

* U.S. stock market
* European stock market

The system provides personalized long-term investment recommendations based on:

* investor profile
* risk tolerance
* investment horizon
* budget
* diversification needs
* macroeconomic context
* real market data (fetched, never hallucinated)

This is NOT a day trading system.
This is NOT a crypto trading bot.
This is NOT a financial advisor replacement.

The goal is to generate explainable, conservative, research-backed portfolio recommendations.

---

# Core Principles

## Allowed Assets

ONLY:

### ETFs

* SPY, VOO, QQQ, VTI, VXUS, IEFA, VGK, IWM, XLV, XLF, SCHD, VYM

### Blue-Chip Stocks

* Apple (AAPL), Microsoft (MSFT), NVIDIA (NVDA), Amazon (AMZN), Alphabet (GOOGL)
* Johnson & Johnson (JNJ), Procter & Gamble (PG), Visa (V)
* ASML (ASML), Nestlé (NESN), LVMH (MC.PA), SAP (SAP), Siemens (SIE.DE), Novo Nordisk (NVO)

---

## Forbidden Assets

NEVER recommend:

* crypto, options, forex, penny stocks, meme stocks
* leveraged or inverse ETFs
* speculative biotech, short-term signals
* any ticker not in the approved allowlist

The allowlist is enforced in Python code — not by prompt instruction alone.

---

## LLM Grounding Rules (Non-Negotiable)

1. **The LLM never generates financial figures from memory.**
   Every number in a recommendation (P/E, yield, return, price) must come from fetched market data injected into the prompt.

2. **The allowlist validator runs on every LLM output in Python** before it reaches the user.

3. **Every output must cite its data source and fetch timestamp.**

4. **Contradictions in investor input must be surfaced explicitly.**
   Example: "low risk" + "expecting 25% annual returns" → flag before proceeding.

---

# Agent Architecture (Simplified — 3 Nodes)

```
[User Input]
     │
     ▼
[ProfileAgent]       — classify investor, detect contradictions
     │
     ▼
[ResearchAgent]      — fetch real data via yfinance, inject into state
     │
     ▼
[PortfolioAgent]     — build recommendation, validate against allowlist
     │
     ▼
[Structured Output]
```

## Shared Agent State

All agents read and write a single `AgentState`:

```python
class AgentState(TypedDict):
    investor_profile: InvestorProfile | None
    market_data: dict[str, MarketDataSnapshot]
    portfolio_draft: PortfolioDraft | None
    recommendation: FinalRecommendation | None
    errors: list[str]
    requires_human_review: bool
    trace_id: str
```

## Agent Responsibilities

### ProfileAgent
- Parse and validate user input
- Classify investor type (conservative / moderate / aggressive)
- Detect contradictions between risk tolerance and return expectations
- Output: `InvestorProfile`

### ResearchAgent
- Fetch real market data for candidate assets using yfinance
- Normalize to `MarketDataSnapshot` (price, P/E, yield, 52w range, volume)
- LLM never sees a financial figure it didn't receive from this agent
- Output: populated `market_data` in state

### PortfolioAgent
- Generate asset allocation based on profile + real data
- LLM explains the reasoning — quantitative data must already be in the prompt
- Output passes through Python allowlist validator before returning
- Output: `FinalRecommendation`

---

# User Input Schema

```json
{
  "budget": 10000,
  "currency": "EUR",
  "risk_tolerance": "medium",
  "investment_horizon_years": 5,
  "preferred_regions": ["US", "Europe"],
  "preferred_sectors": ["Technology", "Healthcare"],
  "dividend_preference": true,
  "growth_vs_value": "balanced",
  "esg_preference": false
}
```

---

# Output Format

Every recommendation must include:

```json
{
  "portfolio": [
    {
      "ticker": "VOO",
      "allocation_pct": 35,
      "rationale": "...",
      "data_source": "yfinance",
      "data_fetched_at": "2024-01-15T09:30:00Z"
    }
  ],
  "risk_summary": "...",
  "alternatives": [...],
  "uncertainty": {
    "data_freshness": "Data fetched 2 hours ago",
    "caveats": ["Macro data does not reflect latest Fed decision"],
    "disclaimer": "This is not financial advice. Past performance does not guarantee future results."
  }
}
```

No confidence scores (implies false precision). Use explicit caveats instead.

---

# Technical Stack

| Layer | Choice |
|---|---|
| Language | Python 3.12+ |
| API Framework | FastAPI |
| Agent Framework | LangGraph |
| LLM | Claude (Anthropic SDK) |
| Database | PostgreSQL |
| Cache | In-memory / file cache (Redis deferred to Phase 2) |
| Market Data | yfinance (Phase 1), Alpha Vantage / FMP (Phase 2) |
| Package Manager | uv |
| Linting | ruff |
| Type Checking | mypy --strict |
| Testing | pytest + pytest-asyncio |
| Deployment | Docker + Railway or Render |

---

# Folder Structure

```
financial-advisor/
├── api/
│   ├── main.py
│   └── routers/
│       ├── profiles.py
│       └── recommendations.py
├── agents/
│   ├── graph.py
│   ├── state.py
│   ├── profile_agent.py
│   ├── research_agent.py
│   └── portfolio_agent.py
├── core/
│   ├── market_data.py
│   ├── allowlist.py
│   └── financial_math.py
├── db/
│   ├── models.py
│   ├── repository.py
│   └── session.py
├── schemas/
│   ├── investor.py
│   └── recommendation.py
├── prompts/
│   ├── profile.md
│   ├── research.md
│   └── portfolio.md
├── tests/
│   ├── test_allowlist.py
│   ├── test_market_data.py
│   └── test_graph.py
├── config/
│   └── settings.py
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── pyproject.toml
```

---

# Development Rules

## Code Quality

Always:
* strongly type all functions
* use Pydantic v2 models for all I/O
* keep business logic out of API routers
* write modular, testable agent nodes
* prefer explicit logic over abstractions

Never:
* mix prompts inside API controllers
* hardcode financial data or stock recommendations
* let the LLM generate numbers from memory
* skip allowlist validation on output

## Prompt Engineering Rules

Prompts must:
* inject real fetched data before asking for reasoning
* request structured output (Pydantic-parseable)
* include explicit instructions to cite data sources
* use conservative, institutional-quality language

Prompts must never:
* ask Claude to "recommend stocks" without providing market data
* use hype language or speculative framing
* omit financial disclaimers

---

# Phased Roadmap

## Phase 1 — MVP (Current)
* 3-node LangGraph pipeline
* yfinance market data
* PostgreSQL (profiles + recommendations)
* FastAPI endpoints
* Python allowlist enforcement

## Phase 2
* Redis caching
* Alpha Vantage + FMP data providers
* Separate RiskAnalysisAgent node
* Email/webhook alerts
* Next.js dashboard

## Phase 3
* MonitoringAgent + Celery background workers
* pgvector + RAG over earnings reports
* Backtesting engine

## Phase 4+
* Tax-aware optimization
* Multi-client support
* Institutional dashboard

---

# Final Rule

This project is an **INVESTMENT RESEARCH AGENT** — not a trading signal bot.

Every design decision must respect that principle.
