"""Natural language analysis service for Glimmora MacroMind.

Uses the OpenAI GPT-4o API for intelligent financial analysis,
with a keyword-based fallback when the API is unavailable.
"""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

from app.data.mock_data import generate_sparkline, get_company_profile, get_macro_report, get_market_overview
from app.models.schemas import AnalysisResponse

logger = logging.getLogger(__name__)

# ─── In-memory cache ────────────────────────────────────────────────────────

_query_cache: dict[str, tuple[float, AnalysisResponse]] = {}
_CACHE_TTL = 600  # 10 minutes

# ─── OpenAI client initialization ─────────────────────────────────────────

_client = None
try:
    from openai import OpenAI
    if os.environ.get("OPENAI_API_KEY"):
        _client = OpenAI()
        logger.info("OpenAI client initialized successfully")
    else:
        logger.warning("OPENAI_API_KEY not set — using fallback analysis")
except Exception as e:
    logger.warning("OpenAI client not initialized — using fallback analysis: %s", e)

# ─── System prompt ──────────────────────────────────────────────────────────

_SYSTEM_PROMPT = """You are MacroMind, an AGI-powered global financial intelligence system. You are a world-class financial analyst with deep expertise in:
- Macroeconomics and monetary policy
- Equity research and valuation
- Commodity markets and energy
- Geopolitical risk assessment
- Cryptocurrency and digital assets
- Global trade flows and supply chains

When answering financial queries, provide:
1. A detailed, insightful analysis (2-4 paragraphs with markdown formatting)
2. Key data points with current approximate values
3. Chart suggestions for visualizing the data
4. Credible source references

Respond in JSON format:
{
  "answer": "markdown formatted analysis...",
  "data_points": [{"label": "GDP Growth", "value": "2.1%"}, ...],
  "charts": [{"type": "bar|line|pie|gauge", "title": "...", "data": [...]}, ...],
  "sources": ["Source 1", "Source 2", ...]
}

For charts, use these types:
- "bar": data should be list of {name: string, value: number}
- "line": data should be list of numbers
- "pie": data should be list of {name: string, value: number}
- "gauge": data should have {value: number, max: number}

Always provide approximate current real-world data. Be specific with numbers.
IMPORTANT: Respond with ONLY valid JSON. No markdown code fences, no extra text before or after the JSON object."""

# ─── Known ticker patterns for quick lookup (used by fallback) ──────────────

_KNOWN_TICKERS = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "JPM", "TSLA",
    "2222", "TSMC", "TSM", "NVO", "META", "BHP",
]


# ─── Main entry point ───────────────────────────────────────────────────────

def analyze_query(query: str) -> AnalysisResponse:
    """Parse a natural language query and return relevant analysis.

    Tries the OpenAI API first; falls back to keyword-based analysis
    if the API is unavailable or returns an error.
    """
    # Check cache
    cache_key = query.strip().lower()
    if cache_key in _query_cache:
        cached_time, cached_response = _query_cache[cache_key]
        if time.time() - cached_time < _CACHE_TTL:
            logger.debug("Cache hit for query: %s", query[:80])
            return cached_response
        else:
            # Expired — remove stale entry
            del _query_cache[cache_key]

    # Try OpenAI API
    if _client is not None:
        try:
            response = _call_openai(query)
            if response is not None:
                # Cache and return
                _query_cache[cache_key] = (time.time(), response)
                return response
        except Exception as e:
            logger.warning("OpenAI API call failed, falling back to keyword analysis: %s", e)

    # Fallback to keyword-based analysis
    fallback_response = _keyword_fallback(query)
    _query_cache[cache_key] = (time.time(), fallback_response)
    return fallback_response


def _call_openai(query: str) -> AnalysisResponse | None:
    """Call the OpenAI API and parse the structured response."""
    completion = _client.chat.completions.create(
        model="gpt-4o",
        max_tokens=4096,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    # Extract text content from the response
    raw_text = completion.choices[0].message.content or ""

    if not raw_text.strip():
        logger.warning("OpenAI returned empty response")
        return None

    # Strip markdown code fences if present
    text = raw_text.strip()
    if text.startswith("```"):
        # Remove opening fence (with optional language tag)
        first_newline = text.index("\n") if "\n" in text else 3
        text = text[first_newline + 1:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    # Parse JSON
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("Failed to parse OpenAI response as JSON: %s", text[:200])
        # Try to use raw text as the answer directly
        return AnalysisResponse(
            query=query,
            answer=raw_text.strip(),
            data_points=[],
            charts=[],
            sources=["MacroMind AI Analysis"],
        )

    # Build AnalysisResponse from parsed JSON
    answer = data.get("answer", raw_text.strip())
    data_points = data.get("data_points", [])
    charts = data.get("charts", [])
    sources = data.get("sources", [])

    # Validate data_points structure
    cleaned_data_points: list[dict[str, Any]] = []
    for dp in data_points:
        if isinstance(dp, dict) and "label" in dp and "value" in dp:
            cleaned_data_points.append({"label": str(dp["label"]), "value": str(dp["value"])})

    # Validate charts structure
    cleaned_charts: list[dict[str, Any]] = []
    for chart in charts:
        if isinstance(chart, dict) and "type" in chart and "title" in chart:
            cleaned_charts.append(chart)

    # Validate sources
    cleaned_sources: list[str] = []
    for src in sources:
        if isinstance(src, str):
            cleaned_sources.append(src)

    return AnalysisResponse(
        query=query,
        answer=answer,
        data_points=cleaned_data_points,
        charts=cleaned_charts,
        sources=cleaned_sources,
    )


# ─── Keyword-based fallback router ──────────────────────────────────────────

def _keyword_fallback(query: str) -> AnalysisResponse:
    """Route query to the appropriate keyword-based analysis function."""
    q = query.lower()

    # Check for company ticker first
    for ticker in _KNOWN_TICKERS:
        if ticker.lower() in q:
            return _company_analysis(ticker, query)

    # Keyword-based routing
    if any(kw in q for kw in ["oil", "energy", "crude", "opec", "aramco", "petroleum"]):
        return _oil_analysis(query)

    if any(kw in q for kw in ["china", "asia", "shanghai", "beijing", "taiwan", "tsmc"]):
        return _china_analysis(query)

    if any(kw in q for kw in ["recession", "downturn", "contraction", "slowdown", "unemployment"]):
        return _recession_analysis(query)

    if any(kw in q for kw in ["inflation", "cpi", "price", "cost of living"]):
        return _inflation_analysis(query)

    if any(kw in q for kw in ["crypto", "bitcoin", "btc", "ethereum", "blockchain"]):
        return _crypto_analysis(query)

    if any(kw in q for kw in ["gold", "commodity", "commodities", "metals"]):
        return _commodity_analysis(query)

    # Default: macro overview
    return _macro_overview(query)


# ─── Fallback analysis functions ─────────────────────────────────────────────

def _company_analysis(ticker: str, query: str) -> AnalysisResponse:
    normalized = ticker.upper()
    if normalized == "TSM":
        normalized = "TSMC"
    profile = get_company_profile(normalized)
    if not profile:
        return AnalysisResponse(
            query=query,
            answer=f"Ticker '{ticker}' not found in our database.",
            data_points=[],
            charts=[],
            sources=["MacroMind Internal Database"],
        )
    return AnalysisResponse(
        query=query,
        answer=(
            f"**{profile['name']}** ({profile['ticker']}) operates in the {profile['sector']} sector. "
            f"The company has a market capitalization of ${profile['market_cap']/1e9:.0f}B and "
            f"trades at a P/E ratio of {profile['pe_ratio']}x. Revenue stands at "
            f"${profile['revenue']/1e9:.1f}B with {profile['employees']:,} employees.\n\n"
            f"Financial Health Score: {profile['financial_health_score']}/100 | "
            f"ESG Score: {profile['esg_score']}/100 | "
            f"Geopolitical Exposure: {profile['geopolitical_exposure']}/10\n\n"
            f"{profile['description']}"
        ),
        data_points=[
            {"label": "Market Cap", "value": f"${profile['market_cap']/1e12:.2f}T"},
            {"label": "P/E Ratio", "value": f"{profile['pe_ratio']}x"},
            {"label": "Revenue", "value": f"${profile['revenue']/1e9:.1f}B"},
            {"label": "Employees", "value": f"{profile['employees']:,}"},
            {"label": "Financial Health", "value": f"{profile['financial_health_score']}/100"},
            {"label": "ESG Score", "value": f"{profile['esg_score']}/100"},
            {"label": "Geopolitical Exposure", "value": f"{profile['geopolitical_exposure']}/10"},
        ],
        charts=[
            {"type": "gauge", "title": "Financial Health", "value": profile["financial_health_score"], "max": 100},
            {"type": "gauge", "title": "ESG Score", "value": profile["esg_score"], "max": 100},
        ],
        sources=["SEC Filings", "Bloomberg Terminal", "MacroMind Proprietary Models"],
    )


def _oil_analysis(query: str) -> AnalysisResponse:
    market = get_market_overview()
    oil = next((c for c in market["commodities"] if "oil" in c["name"].lower()), None)
    gas = next((c for c in market["commodities"] if "gas" in c["name"].lower()), None)

    return AnalysisResponse(
        query=query,
        answer=(
            "**Oil Market Analysis**\n\n"
            f"WTI Crude is currently trading at ${oil['price']}/bbl ({oil['change_pct']:+.2f}%). "
            "OPEC+ has extended production cuts through Q3 2025, providing a floor under prices. "
            "However, demand concerns from China's slowing economy are capping the upside.\n\n"
            "**Key Factors:**\n"
            "- OPEC+ compliance remains high at 95%, with Saudi Arabia bearing most voluntary cuts\n"
            "- US shale production has plateaued at ~13.2M bbl/day as capital discipline holds\n"
            "- Strategic Petroleum Reserve at lowest levels since 1983\n"
            "- Strait of Hormuz risk premium embedded in prices (~$5-8/bbl)\n\n"
            "**Outlook:** Range-bound $72-85/bbl unless a geopolitical event triggers breakout."
        ),
        data_points=[
            {"label": "WTI Crude", "value": f"${oil['price']}/bbl" if oil else "N/A"},
            {"label": "Natural Gas", "value": f"${gas['price']}/MMBtu" if gas else "N/A"},
            {"label": "OPEC+ Compliance", "value": "95%"},
            {"label": "US Shale Production", "value": "13.2M bbl/day"},
            {"label": "Global Demand", "value": "102.3M bbl/day"},
            {"label": "SPR Level", "value": "347M barrels"},
        ],
        charts=[
            {"type": "line", "title": "Oil Price Trend (20 periods)", "data": generate_sparkline(oil["price"], oil["price"] * 0.02) if oil else []},
            {"type": "bar", "title": "OPEC+ Production by Country", "data": [
                {"country": "Saudi Arabia", "production": 9.0},
                {"country": "Russia", "production": 9.4},
                {"country": "Iraq", "production": 4.3},
                {"country": "UAE", "production": 3.2},
                {"country": "Kuwait", "production": 2.6},
            ]},
        ],
        sources=["IEA Monthly Oil Report", "EIA Short-Term Energy Outlook", "OPEC Monthly Bulletin"],
    )


def _china_analysis(query: str) -> AnalysisResponse:
    return AnalysisResponse(
        query=query,
        answer=(
            "**China & Asia Exposure Analysis**\n\n"
            "China's economy is navigating a structural slowdown driven by the property sector "
            "crisis and demographic headwinds. GDP growth of 4.7% masks significant underlying "
            "weakness, with deflationary pressures building.\n\n"
            "**Key Themes:**\n"
            "- Property sector: New home prices falling for 10th consecutive month. Evergrande "
            "liquidation sets precedent for developer defaults.\n"
            "- Taiwan risk: Cross-strait tensions elevate semiconductor supply chain risk. "
            "TSMC produces 90%+ of advanced chips globally.\n"
            "- Trade war 2.0: US tariffs on Chinese EVs (100%), semiconductors, and solar panels. "
            "EU following with EV tariffs of 17-38%.\n"
            "- Bright spots: Chinese EVs (BYD surpassing Tesla in global sales), AI development, "
            "and renewable energy manufacturing dominance.\n\n"
            "**Portfolio Implications:** Reduce direct China equity exposure; maintain indirect "
            "exposure through commodities and EM that benefit from Chinese demand."
        ),
        data_points=[
            {"label": "China GDP Growth", "value": "4.7%"},
            {"label": "China CPI", "value": "0.3%"},
            {"label": "Youth Unemployment", "value": "14.7%"},
            {"label": "PMI (Manufacturing)", "value": "49.1"},
            {"label": "USD/CNY", "value": "7.2456"},
            {"label": "Shanghai Composite", "value": "3,086.81"},
            {"label": "Property Investment YoY", "value": "-9.8%"},
        ],
        charts=[
            {"type": "bar", "title": "China Key Indicators", "data": [
                {"indicator": "GDP Growth", "value": 4.7},
                {"indicator": "CPI", "value": 0.3},
                {"indicator": "PMI", "value": 49.1},
                {"indicator": "Industrial Production", "value": 5.6},
            ]},
        ],
        sources=["NBS China", "Caixin PMI Survey", "PBOC Monetary Policy Reports", "MacroMind Geopolitical Risk Model"],
    )


def _recession_analysis(query: str) -> AnalysisResponse:
    return AnalysisResponse(
        query=query,
        answer=(
            "**Recession Probability Analysis**\n\n"
            "MacroMind's proprietary recession model currently assigns a **28% probability** of "
            "US recession within the next 12 months, down from 45% six months ago.\n\n"
            "**Leading Indicators:**\n"
            "- Yield curve (2Y-10Y): Uninverted for 3 months -- historically recessions follow "
            "6-18 months after uninversion\n"
            "- Initial jobless claims: 215K (stable, not signaling labor deterioration)\n"
            "- ISM Manufacturing PMI: 51.3 (expansion territory)\n"
            "- Consumer confidence: Declining but from elevated levels\n"
            "- Corporate earnings: Q1 2025 S&P 500 EPS growth +8.2% YoY\n\n"
            "**Risk Factors:**\n"
            "- Lag effects of 525bps of rate hikes still working through economy\n"
            "- Commercial real estate stress could trigger credit tightening\n"
            "- Consumer savings buffer eroding; credit card delinquencies rising\n\n"
            "**Assessment:** Soft landing remains base case (55% probability), but the window "
            "for a credit event remains open through Q4 2025."
        ),
        data_points=[
            {"label": "Recession Probability (12M)", "value": "28%"},
            {"label": "US GDP Growth", "value": "2.1%"},
            {"label": "Unemployment Rate", "value": "3.9%"},
            {"label": "Initial Claims", "value": "215K"},
            {"label": "ISM Manufacturing", "value": "51.3"},
            {"label": "Yield Curve (2Y-10Y)", "value": "+12bps"},
            {"label": "Fed Funds Rate", "value": "5.25-5.50%"},
        ],
        charts=[
            {"type": "gauge", "title": "Recession Probability", "value": 28, "max": 100},
            {"type": "line", "title": "Leading Indicator Composite", "data": [
                45, 42, 40, 38, 36, 35, 34, 33, 32, 31, 30, 29, 28
            ]},
        ],
        sources=[
            "Federal Reserve Economic Data (FRED)",
            "Conference Board Leading Economic Index",
            "MacroMind Proprietary Recession Model",
            "BLS Employment Situation Report",
        ],
    )


def _inflation_analysis(query: str) -> AnalysisResponse:
    return AnalysisResponse(
        query=query,
        answer=(
            "**Inflation Analysis**\n\n"
            "Core PCE inflation (the Fed's preferred measure) stands at 2.7% YoY, down from the "
            "2022 peak of 5.6% but still above the 2% target. The 'last mile' of disinflation "
            "is proving difficult.\n\n"
            "**Inflationary Pressures:**\n"
            "- Shelter costs: Still elevated at 5.4% YoY, but leading indicators suggest cooling\n"
            "- Services ex-shelter: 3.5%, driven by wages in labor-intensive sectors\n"
            "- Insurance costs: Auto and home insurance surging 20%+\n\n"
            "**Disinflationary Forces:**\n"
            "- Goods deflation: -1.2% YoY as supply chains normalize\n"
            "- China exporting deflation through excess manufacturing capacity\n"
            "- AI productivity gains beginning to show in unit labor costs\n\n"
            "**Outlook:** Inflation likely settles in the 2.3-2.8% range by year-end, insufficient "
            "for aggressive rate cuts but sufficient to avoid re-acceleration."
        ),
        data_points=[
            {"label": "Core PCE YoY", "value": "2.7%"},
            {"label": "CPI YoY", "value": "3.1%"},
            {"label": "Shelter Inflation", "value": "5.4%"},
            {"label": "Goods Inflation", "value": "-1.2%"},
            {"label": "Services Inflation", "value": "3.5%"},
            {"label": "Wage Growth", "value": "4.1%"},
        ],
        charts=[
            {"type": "line", "title": "Inflation Trajectory (Monthly)", "data": [
                5.6, 5.3, 5.0, 4.7, 4.4, 4.1, 3.8, 3.5, 3.3, 3.1, 2.9, 2.8, 2.7
            ]},
        ],
        sources=["BLS CPI Report", "BEA PCE Price Index", "Federal Reserve Beige Book"],
    )


def _crypto_analysis(query: str) -> AnalysisResponse:
    market = get_market_overview()
    btc = next((c for c in market["crypto"] if c["symbol"] == "BTC"), None)
    eth = next((c for c in market["crypto"] if c["symbol"] == "ETH"), None)

    return AnalysisResponse(
        query=query,
        answer=(
            "**Cryptocurrency Market Analysis**\n\n"
            f"Bitcoin is trading at ${btc['price']:,.2f} ({btc['change_24h']:+.2f}% 24h) with "
            f"a market cap of ${btc['market_cap']/1e12:.2f}T. Ethereum is at "
            f"${eth['price']:,.2f} ({eth['change_24h']:+.2f}% 24h).\n\n"
            "**Key Drivers:**\n"
            "- Bitcoin ETFs have accumulated $58B in AUM since January 2024 launch\n"
            "- Bitcoin halving (April 2024) historically precedes 12-18 month bull cycles\n"
            "- Institutional adoption accelerating: pension funds, sovereign wealth allocating 1-3%\n"
            "- Ethereum ETF approval and staking yield attracting TradFi capital\n\n"
            "**Risks:**\n"
            "- Regulatory uncertainty: SEC enforcement actions continue\n"
            "- Correlation with risk assets during market stress events\n"
            "- Mt. Gox distributions and German government sales creating supply overhang"
        ),
        data_points=[
            {"label": "Bitcoin Price", "value": f"${btc['price']:,.2f}" if btc else "N/A"},
            {"label": "Bitcoin Market Cap", "value": f"${btc['market_cap']/1e12:.2f}T" if btc else "N/A"},
            {"label": "Ethereum Price", "value": f"${eth['price']:,.2f}" if eth else "N/A"},
            {"label": "BTC ETF AUM", "value": "$58B"},
            {"label": "BTC Dominance", "value": "54.2%"},
            {"label": "Total Crypto Market Cap", "value": "$2.68T"},
        ],
        charts=[
            {"type": "line", "title": "Bitcoin Price (20 periods)", "data": btc["sparkline"] if btc else []},
            {"type": "line", "title": "Ethereum Price (20 periods)", "data": eth["sparkline"] if eth else []},
        ],
        sources=["CoinGecko", "Glassnode On-Chain Analytics", "Bloomberg Crypto Outlook"],
    )


def _commodity_analysis(query: str) -> AnalysisResponse:
    market = get_market_overview()
    gold = next((c for c in market["commodities"] if "gold" in c["name"].lower()), None)

    return AnalysisResponse(
        query=query,
        answer=(
            "**Commodity Market Analysis**\n\n"
            f"Gold is trading at ${gold['price']:,.2f}/oz ({gold['change_pct']:+.2f}%), near "
            "all-time highs driven by central bank purchases and geopolitical hedging.\n\n"
            "**Key Themes:**\n"
            "- Central banks bought 1,037 tonnes of gold in 2023, second-highest year on record\n"
            "- China and Russia leading de-dollarization through gold accumulation\n"
            "- Industrial metals (copper, lithium) supported by energy transition demand\n"
            "- Agricultural commodities face weather-related supply risks\n\n"
            "**Outlook:** Gold targets $2,500 on continued central bank buying and potential "
            "rate cuts. Copper is structurally bullish on electrification demand."
        ),
        data_points=[
            {"label": "Gold", "value": f"${gold['price']:,.2f}/oz" if gold else "N/A"},
            {"label": "Silver", "value": "$29.84/oz"},
            {"label": "Copper", "value": "$4.62/lb"},
            {"label": "CB Gold Purchases (2023)", "value": "1,037 tonnes"},
            {"label": "Gold/Silver Ratio", "value": "78.7x"},
        ],
        charts=[
            {"type": "bar", "title": "Commodity Performance (%)", "data": [
                {"name": c["name"], "change": c["change_pct"]} for c in market["commodities"]
            ]},
        ],
        sources=["World Gold Council", "LME", "USDA WASDE Report"],
    )


def _macro_overview(query: str) -> AnalysisResponse:
    report = get_macro_report()
    return AnalysisResponse(
        query=query,
        answer=(
            f"**{report['title']}**\n\n{report['summary']}\n\n"
            f"**Outlook:**\n{report['outlook']}"
        ),
        data_points=[
            {"label": "US GDP Growth", "value": "2.1%"},
            {"label": "US Core PCE", "value": "2.7%"},
            {"label": "US Unemployment", "value": "3.9%"},
            {"label": "Eurozone GDP", "value": "0.3%"},
            {"label": "China GDP", "value": "4.7%"},
            {"label": "S&P 500 Fwd P/E", "value": "21.0x"},
            {"label": "VIX", "value": "14.8"},
            {"label": "Fed Funds Rate", "value": "5.25-5.50%"},
        ],
        charts=[
            {"type": "bar", "title": "Global GDP Growth Comparison", "data": [
                {"region": "US", "gdp": 2.1},
                {"region": "Eurozone", "gdp": 0.3},
                {"region": "China", "gdp": 4.7},
                {"region": "India", "gdp": 7.2},
                {"region": "Japan", "gdp": 0.9},
            ]},
        ],
        sources=[
            "IMF World Economic Outlook",
            "Federal Reserve Economic Projections",
            "ECB Economic Bulletin",
            "MacroMind Global Macro Model",
        ],
    )
