# CLAUDE.md

## Project Name

Investment Research Agent — ETF + Blue Chip Stock Recommendation System

---

# Project Purpose

This project is an AI-powered investment research agent focused exclusively on:

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
* real-time market data

This is NOT a day trading system.

This is NOT a crypto trading bot.

This is NOT a financial advisor replacement.

The goal is to generate explainable, conservative, research-backed portfolio recommendations.

The agent must prioritize:

* explainability
* diversification
* risk management
* long-term investing
* professional-grade output

over speculative “buy now” recommendations.

---

# Core Principles

## Allowed Assets

ONLY:

### ETFs

Examples:

* SPY
* VOO
* QQQ
* VTI
* VXUS
* IEFA
* VGK
* IWM
* XLV
* XLF
* SCHD
* VYM

### Blue-Chip Stocks

Examples:

* Apple
* Microsoft
* NVIDIA
* Amazon
* Alphabet
* Johnson & Johnson
* Procter & Gamble
* Visa
* ASML
* Nestlé
* LVMH
* SAP
* Siemens
* Novo Nordisk

---

## Forbidden Assets

NEVER recommend:

* crypto
* options
* forex
* penny stocks
* meme stocks
* leveraged ETFs
* inverse ETFs
* speculative biotech
* short-term trading signals
* pump-and-dump assets
* gambling-style recommendations

---

# Agent Responsibilities

The system must:

1. Understand investor goals
2. Retrieve financial market data
3. Evaluate risk and diversification
4. Recommend ETF + blue-chip allocations
5. Explain WHY each recommendation exists
6. Monitor important portfolio changes
7. Generate alerts for major market events

The system must NOT:

* guarantee returns
* promise profits
* give reckless buy/sell signals
* act as a licensed financial advisor

All outputs must include clear financial disclaimers.

---

# User Input Schema

Required inputs:

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

# Multi-Agent Architecture

## 1. Investor Profile Agent

Responsibilities:

* parse user goals
* classify investor type
* assess risk tolerance
* detect constraints
* validate unrealistic expectations

Output:

Investor profile summary

---

## 2. Market Research Agent

Responsibilities:

* fetch ETF and stock data
* retrieve:

  * P/E ratio
  * dividend yield
  * revenue growth
  * analyst ratings
  * earnings reports
  * market sentiment
  * macroeconomic context

Sources:

* Yahoo Finance
* Alpha Vantage
* Finnhub
* Financial Modeling Prep
* SEC EDGAR
* ECB / Federal Reserve public data

---

## 3. Risk Analysis Agent

Responsibilities:

* diversification analysis
* sector concentration detection
* volatility evaluation
* valuation risk review
* macroeconomic sensitivity analysis

Output:

Risk report with explanation

---

## 4. Portfolio Construction Agent

Responsibilities:

Generate:

* asset allocation
* ETF weighting
* blue-chip stock allocation
* regional diversification
* sector balancing
* cash reserve recommendation

Example:

* 35% VOO
* 20% VGK
* 10% SCHD
* 10% Microsoft
* 10% ASML
* 10% Johnson & Johnson
* 5% cash reserve

---

## 5. Monitoring & Alerts Agent

Responsibilities:

Track:

* earnings announcements
* analyst downgrades
* major volatility
* Fed / ECB decisions
* dividend cuts
* recession indicators

Outputs:

* email alerts
* dashboard alerts
* weekly portfolio review summary

---

# Output Format Requirements

Every recommendation must include:

## Recommendation

Example:

Increase exposure to European healthcare through Novo Nordisk and Healthcare ETF allocation.

---

## Why

Example:

Novo Nordisk shows resilient earnings growth, strong cash flow, and defensive characteristics during macroeconomic slowdowns.

---

## Risk

Example:

Current valuation is elevated compared to historical averages, so allocation should remain moderate.

---

## Alternative

Example:

Johnson & Johnson for lower volatility and stronger dividend stability.

---

## Confidence Score

Example:

8.4 / 10

---

# Technical Stack

## Backend

Python

## API Framework

FastAPI

## Agent Framework

LangGraph

## LLM

Claude Code + Claude Pro

## Database

PostgreSQL

## Cache

Redis

## Vector Storage (optional)

pgvector

## Frontend (optional)

Next.js dashboard

## Deployment

Docker + Railway / Render / AWS

---

# Development Rules

## Code Quality

Always:

* strongly type functions
* use Pydantic models
* keep business logic separate from API routes
* write modular agents
* prioritize testability
* prefer explicit logic over magic abstractions

Never:

* mix prompts inside API controllers
* hardcode stock recommendations
* use hidden assumptions
* produce unsupported claims

---

# Prompt Engineering Rules

Prompts must prioritize:

* explainability
* financial conservatism
* portfolio diversification
* institutional-quality reasoning

Prompts must avoid:

* hype language
* speculative recommendations
* “guaranteed returns”
* emotional trading suggestions

Bad:

“Buy NVIDIA now before it explodes”

Good:

“NVIDIA has strong structural AI growth drivers, but elevated valuation suggests a partial allocation strategy rather than concentrated exposure.”

---

# Evaluation Criteria

Success means:

* recommendations are explainable
* portfolio risk is controlled
* diversification is strong
* outputs look professional
* investor trust is high

Failure means:

* random stock picks
* speculative recommendations
* poor diversification
* weak reasoning
* hallucinated financial claims

---

# Long-Term Roadmap

Phase 1:

ETF + blue-chip recommendation engine

Phase 2:

Portfolio monitoring + alerts

Phase 3:

Backtesting engine

Phase 4:

Tax-aware portfolio optimization

Phase 5:

Wealth manager / advisor dashboard

Phase 6:

Institutional multi-client support

---

# Final Rule

This project is an

INVESTMENT RESEARCH AGENT

not a

TRADING SIGNAL BOT

Every design decision must respect that principle.
