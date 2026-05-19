"""Rich mock data generators for Glimmora MacroMind.

All data uses realistic company names, prices, and relationships.
random.seed() is used where appropriate to keep data stable within a
single server session while still varying across restarts.
"""

from __future__ import annotations

import math
import random
from datetime import datetime, timedelta
from typing import Any

# Seed for reproducibility within a session
random.seed(42)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def generate_sparkline(base: float, volatility: float, points: int = 20) -> list[float]:
    """Generate a realistic-looking price series with momentum + mean-reversion."""
    prices: list[float] = [base]
    momentum = 0.0
    for _ in range(points - 1):
        momentum = 0.7 * momentum + random.gauss(0, volatility)
        mean_revert = (base - prices[-1]) * 0.05
        prices.append(round(prices[-1] + momentum + mean_revert, 2))
    return prices


def _ts(days_ago: int = 0) -> str:
    return (datetime.utcnow() - timedelta(days=days_ago)).isoformat() + "Z"


# ─── Market Overview ─────────────────────────────────────────────────────────

def get_market_overview() -> dict[str, Any]:
    indices = [
        {"name": "S&P 500",        "value": 5428.93, "change":  23.41, "change_pct":  0.43, "sparkline": generate_sparkline(5380, 18)},
        {"name": "NASDAQ Composite","value": 17187.56,"change":  89.27, "change_pct":  0.52, "sparkline": generate_sparkline(17050, 45)},
        {"name": "Nikkei 225",     "value": 38471.20,"change": -112.35,"change_pct": -0.29, "sparkline": generate_sparkline(38600, 120)},
        {"name": "FTSE 100",       "value": 8317.64, "change":  14.88, "change_pct":  0.18, "sparkline": generate_sparkline(8280, 15)},
        {"name": "DAX",            "value": 18684.02,"change":  47.63, "change_pct":  0.26, "sparkline": generate_sparkline(18600, 35)},
        {"name": "Shanghai Comp.", "value": 3086.81, "change":  -8.74, "change_pct": -0.28, "sparkline": generate_sparkline(3100, 12)},
    ]
    forex = [
        {"pair": "EUR/USD", "rate": 1.0843, "change":  0.0012, "change_pct":  0.11},
        {"pair": "USD/JPY", "rate": 156.72, "change":  0.34,   "change_pct":  0.22},
        {"pair": "GBP/USD", "rate": 1.2711, "change": -0.0008, "change_pct": -0.06},
        {"pair": "USD/CHF", "rate": 0.9031, "change":  0.0015, "change_pct":  0.17},
        {"pair": "AUD/USD", "rate": 0.6628, "change": -0.0021, "change_pct": -0.32},
        {"pair": "USD/CNY", "rate": 7.2456, "change":  0.0098, "change_pct":  0.14},
    ]
    crypto = [
        {"name": "Bitcoin",  "symbol": "BTC", "price": 69842.50, "market_cap": 1.372e12, "change_24h":  1.84, "sparkline": generate_sparkline(68500, 420)},
        {"name": "Ethereum", "symbol": "ETH", "price": 3812.30,  "market_cap": 4.58e11,  "change_24h":  2.31, "sparkline": generate_sparkline(3720, 28)},
        {"name": "Solana",   "symbol": "SOL", "price": 172.46,   "market_cap": 7.82e10,  "change_24h":  3.67, "sparkline": generate_sparkline(165, 4.5)},
        {"name": "BNB",      "symbol": "BNB", "price": 612.80,   "market_cap": 9.41e10,  "change_24h": -0.42, "sparkline": generate_sparkline(618, 6)},
        {"name": "XRP",      "symbol": "XRP", "price": 0.5284,   "market_cap": 2.91e10,  "change_24h":  0.95, "sparkline": generate_sparkline(0.52, 0.008)},
        {"name": "Cardano",  "symbol": "ADA", "price": 0.4613,   "market_cap": 1.64e10,  "change_24h": -1.18, "sparkline": generate_sparkline(0.47, 0.007)},
    ]
    commodities = [
        {"name": "Crude Oil (WTI)", "price": 78.42, "unit": "USD/bbl",  "change":  1.23, "change_pct":  1.59},
        {"name": "Gold",            "price": 2348.60,"unit": "USD/oz",  "change": 12.40, "change_pct":  0.53},
        {"name": "Silver",          "price": 29.84, "unit": "USD/oz",   "change":  0.38, "change_pct":  1.29},
        {"name": "Natural Gas",     "price": 2.73,  "unit": "USD/MMBtu","change": -0.08, "change_pct": -2.85},
        {"name": "Copper",          "price": 4.62,  "unit": "USD/lb",   "change":  0.07, "change_pct":  1.54},
        {"name": "Wheat",           "price": 5.86,  "unit": "USD/bu",   "change": -0.04, "change_pct": -0.68},
    ]
    alerts = [
        "BREAKING: Federal Reserve signals potential rate pause at next FOMC meeting",
        "China manufacturing PMI contracts for 3rd consecutive month (49.1 vs 49.5 expected)",
        "Oil prices surge on OPEC+ extension of production cuts through Q3",
        "US 10-Year Treasury yield hits 4.52% -- highest since November",
    ]
    return {
        "indices": indices,
        "forex": forex,
        "crypto": crypto,
        "commodities": commodities,
        "alerts": alerts,
    }


# ─── Knowledge Graph ─────────────────────────────────────────────────────────

def get_knowledge_graph() -> dict[str, Any]:
    nodes = [
        # Tech
        {"id": "AAPL",   "label": "Apple Inc.",             "type": "company",    "sector": "Technology",     "market_cap": 3.42e12, "country": "US"},
        {"id": "MSFT",   "label": "Microsoft Corp.",        "type": "company",    "sector": "Technology",     "market_cap": 3.18e12, "country": "US"},
        {"id": "GOOGL",  "label": "Alphabet Inc.",          "type": "company",    "sector": "Technology",     "market_cap": 2.17e12, "country": "US"},
        {"id": "NVDA",   "label": "NVIDIA Corp.",           "type": "company",    "sector": "Semiconductors", "market_cap": 2.84e12, "country": "US"},
        {"id": "TSMC",   "label": "Taiwan Semiconductor",   "type": "company",    "sector": "Semiconductors", "market_cap": 8.12e11, "country": "TW"},
        {"id": "SSNLF",  "label": "Samsung Electronics",    "type": "company",    "sector": "Technology",     "market_cap": 3.62e11, "country": "KR"},
        {"id": "META",   "label": "Meta Platforms",          "type": "company",    "sector": "Technology",     "market_cap": 1.27e12, "country": "US"},
        {"id": "AMZN",   "label": "Amazon.com",             "type": "company",    "sector": "E-Commerce",     "market_cap": 1.92e12, "country": "US"},
        # Finance
        {"id": "JPM",    "label": "JPMorgan Chase",         "type": "company",    "sector": "Finance",        "market_cap": 5.72e11, "country": "US"},
        {"id": "GS",     "label": "Goldman Sachs",          "type": "company",    "sector": "Finance",        "market_cap": 1.54e11, "country": "US"},
        {"id": "BLK",    "label": "BlackRock Inc.",          "type": "company",    "sector": "Asset Mgmt",     "market_cap": 1.18e11, "country": "US"},
        {"id": "HSBC",   "label": "HSBC Holdings",          "type": "company",    "sector": "Finance",        "market_cap": 1.61e11, "country": "GB"},
        # Energy
        {"id": "2222",   "label": "Saudi Aramco",           "type": "company",    "sector": "Energy",         "market_cap": 1.79e12, "country": "SA"},
        {"id": "XOM",    "label": "ExxonMobil",             "type": "company",    "sector": "Energy",         "market_cap": 5.04e11, "country": "US"},
        {"id": "SHEL",   "label": "Shell plc",              "type": "company",    "sector": "Energy",         "market_cap": 2.28e11, "country": "GB"},
        # Automotive / Industrial
        {"id": "TSLA",   "label": "Tesla Inc.",             "type": "company",    "sector": "Automotive",     "market_cap": 5.68e11, "country": "US"},
        {"id": "TM",     "label": "Toyota Motor",           "type": "company",    "sector": "Automotive",     "market_cap": 3.14e11, "country": "JP"},
        {"id": "VOW",    "label": "Volkswagen AG",          "type": "company",    "sector": "Automotive",     "market_cap": 6.82e10, "country": "DE"},
        # Pharma
        {"id": "JNJ",    "label": "Johnson & Johnson",      "type": "company",    "sector": "Healthcare",     "market_cap": 3.48e11, "country": "US"},
        {"id": "NVO",    "label": "Novo Nordisk",           "type": "company",    "sector": "Healthcare",     "market_cap": 5.62e11, "country": "DK"},
        # Mining / Materials
        {"id": "BHP",    "label": "BHP Group",              "type": "company",    "sector": "Mining",         "market_cap": 1.52e11, "country": "AU"},
        {"id": "RIO",    "label": "Rio Tinto",              "type": "company",    "sector": "Mining",         "market_cap": 1.12e11, "country": "AU"},
        # Governments / Central Banks
        {"id": "US_GOV",  "label": "United States Govt",    "type": "government", "sector": None, "market_cap": None, "country": "US"},
        {"id": "CN_GOV",  "label": "China Govt",            "type": "government", "sector": None, "market_cap": None, "country": "CN"},
        {"id": "EU_ECB",  "label": "European Central Bank", "type": "central_bank","sector": None, "market_cap": None, "country": "EU"},
        {"id": "US_FED",  "label": "Federal Reserve",       "type": "central_bank","sector": None, "market_cap": None, "country": "US"},
        {"id": "JP_BOJ",  "label": "Bank of Japan",         "type": "central_bank","sector": None, "market_cap": None, "country": "JP"},
        # Commodities
        {"id": "OIL",     "label": "Crude Oil",             "type": "commodity",  "sector": "Energy",    "market_cap": None, "country": None},
        {"id": "GOLD",    "label": "Gold",                  "type": "commodity",  "sector": "Metals",    "market_cap": None, "country": None},
        {"id": "LITHIUM", "label": "Lithium",               "type": "commodity",  "sector": "Materials", "market_cap": None, "country": None},
        {"id": "CHIPS",   "label": "Semiconductors",        "type": "commodity",  "sector": "Technology","market_cap": None, "country": None},
        # Indices
        {"id": "SPX",     "label": "S&P 500 Index",         "type": "index",      "sector": None, "market_cap": None, "country": "US"},
    ]
    edges = [
        # Supply chain: chip dependencies
        {"source": "AAPL",  "target": "TSMC",   "relationship": "depends_on_manufacturing",  "strength": 0.95},
        {"source": "NVDA",  "target": "TSMC",   "relationship": "depends_on_manufacturing",  "strength": 0.98},
        {"source": "MSFT",  "target": "NVDA",   "relationship": "major_customer",             "strength": 0.85},
        {"source": "GOOGL", "target": "NVDA",   "relationship": "major_customer",             "strength": 0.78},
        {"source": "META",  "target": "NVDA",   "relationship": "major_customer",             "strength": 0.82},
        {"source": "AMZN",  "target": "NVDA",   "relationship": "major_customer",             "strength": 0.75},
        {"source": "SSNLF", "target": "CHIPS",  "relationship": "produces",                   "strength": 0.88},
        {"source": "TSMC",  "target": "CHIPS",  "relationship": "produces",                   "strength": 0.96},
        # Energy supply chains
        {"source": "2222",  "target": "OIL",    "relationship": "produces",                   "strength": 0.95},
        {"source": "XOM",   "target": "OIL",    "relationship": "produces",                   "strength": 0.85},
        {"source": "SHEL",  "target": "OIL",    "relationship": "produces",                   "strength": 0.80},
        {"source": "2222",  "target": "CN_GOV", "relationship": "supplies_oil_to",            "strength": 0.72},
        {"source": "2222",  "target": "JP_BOJ", "relationship": "supplies_oil_to",            "strength": 0.55},
        {"source": "OIL",   "target": "VOW",    "relationship": "input_cost",                 "strength": 0.60},
        {"source": "OIL",   "target": "TM",     "relationship": "input_cost",                 "strength": 0.55},
        # Financial system
        {"source": "US_FED","target": "JPM",    "relationship": "regulates",                  "strength": 0.90},
        {"source": "US_FED","target": "GS",     "relationship": "regulates",                  "strength": 0.90},
        {"source": "US_FED","target": "SPX",    "relationship": "influences",                 "strength": 0.92},
        {"source": "EU_ECB","target": "HSBC",   "relationship": "regulates",                  "strength": 0.75},
        {"source": "JP_BOJ","target": "TM",     "relationship": "monetary_policy_affects",    "strength": 0.68},
        {"source": "JPM",   "target": "AAPL",   "relationship": "major_lender",               "strength": 0.45},
        {"source": "BLK",   "target": "AAPL",   "relationship": "major_shareholder",          "strength": 0.72},
        {"source": "BLK",   "target": "MSFT",   "relationship": "major_shareholder",          "strength": 0.70},
        {"source": "BLK",   "target": "NVDA",   "relationship": "major_shareholder",          "strength": 0.65},
        {"source": "GS",    "target": "TSLA",   "relationship": "investment_banking",         "strength": 0.50},
        # Automotive / EV
        {"source": "TSLA",  "target": "LITHIUM","relationship": "depends_on",                 "strength": 0.88},
        {"source": "TM",    "target": "LITHIUM","relationship": "depends_on",                 "strength": 0.45},
        {"source": "VOW",   "target": "LITHIUM","relationship": "depends_on",                 "strength": 0.52},
        {"source": "TSLA",  "target": "NVDA",   "relationship": "uses_chips_from",            "strength": 0.60},
        {"source": "TSLA",  "target": "SSNLF",  "relationship": "battery_supplier",           "strength": 0.55},
        # Geopolitical
        {"source": "CN_GOV","target": "TSMC",   "relationship": "geopolitical_tension",       "strength": 0.88},
        {"source": "US_GOV","target": "TSMC",   "relationship": "strategic_ally",             "strength": 0.80},
        {"source": "US_GOV","target": "CN_GOV", "relationship": "trade_tension",              "strength": 0.85},
        {"source": "CN_GOV","target": "BHP",    "relationship": "major_trade_partner",        "strength": 0.78},
        {"source": "CN_GOV","target": "RIO",    "relationship": "major_trade_partner",        "strength": 0.74},
        # Mining / resources
        {"source": "BHP",   "target": "LITHIUM","relationship": "produces",                   "strength": 0.62},
        {"source": "RIO",   "target": "LITHIUM","relationship": "produces",                   "strength": 0.48},
        {"source": "BHP",   "target": "GOLD",   "relationship": "produces",                   "strength": 0.40},
        # Healthcare
        {"source": "NVO",   "target": "US_GOV", "relationship": "regulated_by_FDA",           "strength": 0.70},
        {"source": "JNJ",   "target": "US_GOV", "relationship": "regulated_by_FDA",           "strength": 0.75},
        # Cloud / infrastructure
        {"source": "AMZN",  "target": "MSFT",   "relationship": "cloud_competitor",           "strength": 0.90},
        {"source": "GOOGL", "target": "MSFT",   "relationship": "cloud_competitor",           "strength": 0.85},
        {"source": "AAPL",  "target": "AMZN",   "relationship": "uses_cloud_services",        "strength": 0.40},
        {"source": "AAPL",  "target": "GOOGL",  "relationship": "search_revenue_deal",        "strength": 0.82},
        # Index membership
        {"source": "AAPL",  "target": "SPX",    "relationship": "constituent",                "strength": 0.99},
        {"source": "MSFT",  "target": "SPX",    "relationship": "constituent",                "strength": 0.99},
        {"source": "NVDA",  "target": "SPX",    "relationship": "constituent",                "strength": 0.98},
        {"source": "AMZN",  "target": "SPX",    "relationship": "constituent",                "strength": 0.98},
        {"source": "GOOGL", "target": "SPX",    "relationship": "constituent",                "strength": 0.97},
        {"source": "META",  "target": "SPX",    "relationship": "constituent",                "strength": 0.96},
        {"source": "TSLA",  "target": "SPX",    "relationship": "constituent",                "strength": 0.94},
        {"source": "JPM",   "target": "SPX",    "relationship": "constituent",                "strength": 0.93},
    ]
    return {"nodes": nodes, "edges": edges}


# ─── Scenario Impacts ────────────────────────────────────────────────────────

_SCENARIO_TEMPLATES: dict[str, dict[str, Any]] = {
    "oil_shock": {
        "narrative": (
            "A sudden supply disruption in the Strait of Hormuz causes oil prices to "
            "spike by {severity}0%. Energy-importing economies face immediate inflationary "
            "pressure while oil exporters see windfall revenues. Transportation and "
            "manufacturing sectors bear the brunt, with airlines and petrochemical firms "
            "seeing margin compression. Central banks face a dilemma between fighting "
            "inflation and supporting growth. The shock ripples through supply chains "
            "within 2-4 weeks, raising consumer prices globally."
        ),
        "impacts": [
            {"asset_class": "Commodities", "asset_name": "Crude Oil (WTI)",     "base_impact":  15.0, "confidence": 0.92, "explanation": "Direct supply shock drives crude prices sharply higher"},
            {"asset_class": "Commodities", "asset_name": "Natural Gas",         "base_impact":   8.0, "confidence": 0.78, "explanation": "Substitution effect as energy consumers switch fuels"},
            {"asset_class": "Equities",    "asset_name": "ExxonMobil (XOM)",    "base_impact":  12.0, "confidence": 0.85, "explanation": "Major beneficiary of higher oil prices"},
            {"asset_class": "Equities",    "asset_name": "Saudi Aramco",        "base_impact":  10.0, "confidence": 0.80, "explanation": "Revenue boost from higher prices despite disruption"},
            {"asset_class": "Equities",    "asset_name": "S&P 500",            "base_impact":  -4.5, "confidence": 0.82, "explanation": "Broad market sell-off on growth concerns"},
            {"asset_class": "Equities",    "asset_name": "Airlines Index",      "base_impact": -14.0, "confidence": 0.88, "explanation": "Fuel costs represent 25-30% of airline operating expenses"},
            {"asset_class": "Equities",    "asset_name": "Toyota Motor",        "base_impact":  -6.0, "confidence": 0.72, "explanation": "Higher input costs and weaker consumer demand"},
            {"asset_class": "Forex",       "asset_name": "USD/JPY",            "base_impact":   2.5, "confidence": 0.65, "explanation": "JPY weakens as Japan is a major oil importer"},
            {"asset_class": "Bonds",       "asset_name": "US 10Y Treasury",     "base_impact":  -1.8, "confidence": 0.70, "explanation": "Inflation expectations rise, pushing yields higher (prices lower)"},
            {"asset_class": "Crypto",      "asset_name": "Bitcoin",             "base_impact":   3.0, "confidence": 0.45, "explanation": "Safe-haven narrative drives modest inflows"},
        ],
        "gdp_base": -0.8,
        "inflation_base": 1.5,
    },
    "rate_hike": {
        "narrative": (
            "The Federal Reserve surprises markets with an unexpected {severity}0 basis-point "
            "rate hike, citing persistent inflation. Bond yields spike, and equity markets "
            "sell off sharply as growth expectations are revised downward. The tech sector, "
            "highly sensitive to discount rates, leads the decline. Credit spreads widen, "
            "increasing borrowing costs for corporations and consumers. Emerging market "
            "currencies face pressure as the dollar strengthens."
        ),
        "impacts": [
            {"asset_class": "Equities",    "asset_name": "NASDAQ Composite",    "base_impact":  -6.0, "confidence": 0.90, "explanation": "Growth/tech stocks highly sensitive to rate increases"},
            {"asset_class": "Equities",    "asset_name": "S&P 500",            "base_impact":  -3.5, "confidence": 0.88, "explanation": "Broad market repricing of equity risk premium"},
            {"asset_class": "Equities",    "asset_name": "JPMorgan Chase",      "base_impact":   3.2, "confidence": 0.72, "explanation": "Banks benefit from wider net interest margins"},
            {"asset_class": "Equities",    "asset_name": "Tesla Inc.",          "base_impact":  -8.5, "confidence": 0.82, "explanation": "High-multiple growth stock faces severe discount rate headwind"},
            {"asset_class": "Bonds",       "asset_name": "US 10Y Treasury",     "base_impact":  -3.0, "confidence": 0.92, "explanation": "Yields spike, bond prices fall across the curve"},
            {"asset_class": "Forex",       "asset_name": "DXY (Dollar Index)",  "base_impact":   2.8, "confidence": 0.85, "explanation": "Higher rates attract global capital flows to USD"},
            {"asset_class": "Forex",       "asset_name": "EUR/USD",            "base_impact":  -2.2, "confidence": 0.80, "explanation": "Euro weakens against strengthening dollar"},
            {"asset_class": "Equities",    "asset_name": "Real Estate (REITs)", "base_impact":  -7.0, "confidence": 0.85, "explanation": "Higher mortgage rates depress property valuations"},
            {"asset_class": "Crypto",      "asset_name": "Bitcoin",             "base_impact":  -5.0, "confidence": 0.55, "explanation": "Risk assets broadly sell off in tightening regime"},
            {"asset_class": "Commodities", "asset_name": "Gold",               "base_impact":  -2.5, "confidence": 0.68, "explanation": "Opportunity cost of holding gold rises with rates"},
        ],
        "gdp_base": -0.5,
        "inflation_base": -0.3,
    },
    "china_taiwan_conflict": {
        "narrative": (
            "Escalating tensions in the Taiwan Strait trigger a severity-{severity} "
            "geopolitical crisis. Global semiconductor supply chains face existential "
            "risk as TSMC, which produces over 90% of advanced chips, is directly "
            "threatened. Tech companies worldwide scramble to secure inventory. "
            "Military posturing disrupts shipping lanes, affecting 40% of global "
            "container traffic. Markets enter risk-off mode as nuclear-armed powers "
            "increase their alert status."
        ),
        "impacts": [
            {"asset_class": "Equities",    "asset_name": "TSMC",               "base_impact": -35.0, "confidence": 0.95, "explanation": "Direct existential threat to operations and fab integrity"},
            {"asset_class": "Equities",    "asset_name": "NVIDIA Corp.",        "base_impact": -22.0, "confidence": 0.92, "explanation": "98% fab dependency on TSMC; cannot manufacture GPUs without them"},
            {"asset_class": "Equities",    "asset_name": "Apple Inc.",          "base_impact": -18.0, "confidence": 0.90, "explanation": "Complete iPhone/Mac chip supply from TSMC at risk"},
            {"asset_class": "Equities",    "asset_name": "S&P 500",            "base_impact": -12.0, "confidence": 0.88, "explanation": "Systemic risk event; broad risk-off across all sectors"},
            {"asset_class": "Equities",    "asset_name": "Shanghai Composite",  "base_impact": -20.0, "confidence": 0.85, "explanation": "Chinese equities face sanctions risk and capital flight"},
            {"asset_class": "Equities",    "asset_name": "Samsung Electronics", "base_impact":   8.0, "confidence": 0.60, "explanation": "Potential beneficiary as alternative chip manufacturer"},
            {"asset_class": "Commodities", "asset_name": "Gold",               "base_impact":  15.0, "confidence": 0.88, "explanation": "Classic safe-haven bid in geopolitical crisis"},
            {"asset_class": "Commodities", "asset_name": "Crude Oil",          "base_impact":  18.0, "confidence": 0.78, "explanation": "Shipping disruptions in Pacific affect energy logistics"},
            {"asset_class": "Forex",       "asset_name": "USD/CNY",            "base_impact":   8.0, "confidence": 0.82, "explanation": "CNY depreciates sharply on capital outflow fears"},
            {"asset_class": "Bonds",       "asset_name": "US 10Y Treasury",     "base_impact":   4.0, "confidence": 0.80, "explanation": "Flight to safety drives Treasury rally (lower yields)"},
            {"asset_class": "Crypto",      "asset_name": "Bitcoin",             "base_impact":  -8.0, "confidence": 0.50, "explanation": "Risk-off; institutional crypto liquidated for margin calls"},
        ],
        "gdp_base": -2.5,
        "inflation_base": 3.0,
    },
    "global_recession": {
        "narrative": (
            "Synchronized economic contraction across the US, EU, and China triggers "
            "a global recession of severity {severity}. Consumer spending collapses, "
            "corporate earnings decline by 20-30%, and unemployment rises. Central banks "
            "pivot to emergency easing but are constrained by still-elevated inflation. "
            "Credit markets seize up as default rates climb. Commodity demand destruction "
            "pushes energy and metals prices lower."
        ),
        "impacts": [
            {"asset_class": "Equities",    "asset_name": "S&P 500",            "base_impact": -15.0, "confidence": 0.90, "explanation": "Earnings decline and multiple compression drive broad sell-off"},
            {"asset_class": "Equities",    "asset_name": "NASDAQ Composite",    "base_impact": -18.0, "confidence": 0.88, "explanation": "Growth stocks hit hardest as revenue growth stalls"},
            {"asset_class": "Equities",    "asset_name": "DAX",                "base_impact": -14.0, "confidence": 0.85, "explanation": "Export-dependent German economy contracts sharply"},
            {"asset_class": "Equities",    "asset_name": "Goldman Sachs",       "base_impact": -20.0, "confidence": 0.82, "explanation": "Investment banking revenue collapses; trading losses mount"},
            {"asset_class": "Commodities", "asset_name": "Crude Oil",          "base_impact": -25.0, "confidence": 0.85, "explanation": "Demand destruction outweighs any supply cuts"},
            {"asset_class": "Commodities", "asset_name": "Copper",             "base_impact": -20.0, "confidence": 0.82, "explanation": "Industrial demand falls as construction and manufacturing slow"},
            {"asset_class": "Bonds",       "asset_name": "US 10Y Treasury",     "base_impact":   8.0, "confidence": 0.88, "explanation": "Safe-haven flows and rate cut expectations boost bonds"},
            {"asset_class": "Commodities", "asset_name": "Gold",               "base_impact":  10.0, "confidence": 0.78, "explanation": "Safe-haven demand and monetary easing expectations"},
            {"asset_class": "Forex",       "asset_name": "EUR/USD",            "base_impact":  -3.0, "confidence": 0.65, "explanation": "Dollar strengthens as global reserve currency in crisis"},
            {"asset_class": "Crypto",      "asset_name": "Bitcoin",             "base_impact": -12.0, "confidence": 0.55, "explanation": "Risk assets broadly liquidated; crypto correlates with equities"},
        ],
        "gdp_base": -3.0,
        "inflation_base": -1.0,
    },
    "usd_collapse": {
        "narrative": (
            "A sudden loss of confidence in US fiscal sustainability triggers a severity-{severity} "
            "dollar crisis. Foreign central banks begin diversifying reserves away from USD. "
            "The dollar index falls precipitously, import prices soar, and inflation re-accelerates. "
            "Commodities priced in USD surge. The Federal Reserve faces an impossible choice between "
            "defending the currency and supporting the economy."
        ),
        "impacts": [
            {"asset_class": "Forex",       "asset_name": "DXY (Dollar Index)",  "base_impact": -12.0, "confidence": 0.90, "explanation": "Direct dollar devaluation across all major pairs"},
            {"asset_class": "Forex",       "asset_name": "EUR/USD",            "base_impact":  10.0, "confidence": 0.88, "explanation": "Euro strengthens as alternative reserve currency"},
            {"asset_class": "Commodities", "asset_name": "Gold",               "base_impact":  25.0, "confidence": 0.92, "explanation": "Gold surges as ultimate alternative to fiat currency"},
            {"asset_class": "Commodities", "asset_name": "Crude Oil",          "base_impact":  15.0, "confidence": 0.78, "explanation": "Dollar-denominated commodities reprice higher"},
            {"asset_class": "Crypto",      "asset_name": "Bitcoin",             "base_impact":  30.0, "confidence": 0.60, "explanation": "Digital gold narrative accelerates institutional adoption"},
            {"asset_class": "Equities",    "asset_name": "S&P 500",            "base_impact":  -8.0, "confidence": 0.75, "explanation": "Domestic market falls in real terms despite nominal support"},
            {"asset_class": "Bonds",       "asset_name": "US 10Y Treasury",     "base_impact": -15.0, "confidence": 0.88, "explanation": "Foreign selling of Treasuries crashes bond prices"},
            {"asset_class": "Equities",    "asset_name": "ExxonMobil (XOM)",    "base_impact":   8.0, "confidence": 0.72, "explanation": "Oil revenues rise with commodity prices"},
            {"asset_class": "Equities",    "asset_name": "Nikkei 225",         "base_impact":   5.0, "confidence": 0.60, "explanation": "Japanese exporters benefit from weaker dollar"},
            {"asset_class": "Equities",    "asset_name": "FTSE 100",           "base_impact":   4.0, "confidence": 0.58, "explanation": "UK multinationals benefit from non-USD revenue"},
        ],
        "gdp_base": -1.5,
        "inflation_base": 4.0,
    },
    "climate_crisis": {
        "narrative": (
            "A cascade of extreme weather events -- Category 5 hurricanes, unprecedented "
            "flooding in Asia, and record droughts in Europe -- force governments to "
            "declare climate emergencies at severity {severity}. Emergency carbon pricing "
            "is implemented globally. Insurance losses mount, agricultural output falls, "
            "and the energy transition accelerates violently, stranding fossil fuel assets."
        ),
        "impacts": [
            {"asset_class": "Equities",    "asset_name": "ExxonMobil (XOM)",    "base_impact": -20.0, "confidence": 0.82, "explanation": "Stranded asset risk as carbon pricing erodes fossil fuel economics"},
            {"asset_class": "Equities",    "asset_name": "Saudi Aramco",        "base_impact": -18.0, "confidence": 0.78, "explanation": "Existential threat to hydrocarbon-dependent business model"},
            {"asset_class": "Equities",    "asset_name": "Shell plc",           "base_impact": -15.0, "confidence": 0.80, "explanation": "Transition costs accelerate; reserves devalued"},
            {"asset_class": "Equities",    "asset_name": "Tesla Inc.",          "base_impact":  18.0, "confidence": 0.75, "explanation": "EV adoption accelerates as regulations tighten on ICE vehicles"},
            {"asset_class": "Equities",    "asset_name": "Novo Nordisk",        "base_impact":   2.0, "confidence": 0.40, "explanation": "Healthcare sector relatively insulated from climate regulation"},
            {"asset_class": "Commodities", "asset_name": "Lithium",             "base_impact":  30.0, "confidence": 0.78, "explanation": "Explosive demand for EV batteries accelerates mining"},
            {"asset_class": "Commodities", "asset_name": "Wheat",               "base_impact":  20.0, "confidence": 0.72, "explanation": "Crop failures from drought and flooding reduce global supply"},
            {"asset_class": "Commodities", "asset_name": "Crude Oil",          "base_impact": -10.0, "confidence": 0.65, "explanation": "Demand destruction from carbon pricing offsets near-term supply issues"},
            {"asset_class": "Equities",    "asset_name": "S&P 500",            "base_impact":  -5.0, "confidence": 0.70, "explanation": "Mixed impact: fossil losses offset by green winners"},
            {"asset_class": "Bonds",       "asset_name": "Green Bonds Index",   "base_impact":   8.0, "confidence": 0.72, "explanation": "Massive inflows into sustainable fixed income"},
        ],
        "gdp_base": -1.2,
        "inflation_base": 2.0,
    },
    "tech_bubble_burst": {
        "narrative": (
            "The AI hype cycle reverses sharply at severity {severity} as major tech "
            "companies report disappointing AI revenue. NVIDIA misses earnings estimates "
            "for the first time in 8 quarters. The Magnificent Seven lose $3 trillion in "
            "combined market cap within weeks. Venture capital funding freezes, startups "
            "collapse, and Silicon Valley enters a severe contraction. The contagion "
            "spreads to broader markets as tech-heavy indices drag down global portfolios."
        ),
        "impacts": [
            {"asset_class": "Equities",    "asset_name": "NVIDIA Corp.",        "base_impact": -35.0, "confidence": 0.90, "explanation": "AI revenue miss triggers massive de-rating of premium multiple"},
            {"asset_class": "Equities",    "asset_name": "Microsoft Corp.",     "base_impact": -15.0, "confidence": 0.85, "explanation": "Azure AI spending questioned; Copilot revenue disappoints"},
            {"asset_class": "Equities",    "asset_name": "Apple Inc.",          "base_impact": -10.0, "confidence": 0.80, "explanation": "Contagion from tech sell-off despite hardware resilience"},
            {"asset_class": "Equities",    "asset_name": "Meta Platforms",      "base_impact": -20.0, "confidence": 0.85, "explanation": "Metaverse + AI capex under scrutiny; no clear ROI path"},
            {"asset_class": "Equities",    "asset_name": "NASDAQ Composite",    "base_impact": -22.0, "confidence": 0.92, "explanation": "Tech-heavy index bears full brunt of sector rotation"},
            {"asset_class": "Equities",    "asset_name": "S&P 500",            "base_impact": -10.0, "confidence": 0.88, "explanation": "Mag-7 concentration means tech crash drags whole index"},
            {"asset_class": "Equities",    "asset_name": "TSMC",               "base_impact": -18.0, "confidence": 0.82, "explanation": "Chip demand collapse as hyperscaler capex is cut"},
            {"asset_class": "Equities",    "asset_name": "JPMorgan Chase",      "base_impact":   3.0, "confidence": 0.55, "explanation": "Rotation into value/financials provides modest uplift"},
            {"asset_class": "Bonds",       "asset_name": "US 10Y Treasury",     "base_impact":   5.0, "confidence": 0.78, "explanation": "Flight to safety as equity risk premium spikes"},
            {"asset_class": "Commodities", "asset_name": "Gold",               "base_impact":   6.0, "confidence": 0.68, "explanation": "Safe-haven flows benefit precious metals"},
        ],
        "gdp_base": -1.0,
        "inflation_base": -0.5,
    },
}


def get_scenario_impacts(scenario_type: str, severity: int) -> dict[str, Any]:
    """Return cascading impacts for a given scenario type and severity (1-10)."""
    template = _SCENARIO_TEMPLATES.get(scenario_type)
    if template is None:
        return {
            "scenario": scenario_type,
            "impacts": [],
            "gdp_impact": 0.0,
            "inflation_impact": 0.0,
            "narrative": f"Unknown scenario type: {scenario_type}. Available types: {', '.join(_SCENARIO_TEMPLATES.keys())}",
        }

    severity_multiplier = severity / 5.0  # severity 5 = 1x baseline

    impacts = []
    for imp in template["impacts"]:
        scaled_impact = round(imp["base_impact"] * severity_multiplier, 2)
        impacts.append({
            "asset_class": imp["asset_class"],
            "asset_name": imp["asset_name"],
            "impact_pct": scaled_impact,
            "confidence": round(imp["confidence"] * (1 - abs(severity - 5) * 0.03), 2),
            "explanation": imp["explanation"],
        })

    return {
        "scenario": scenario_type,
        "impacts": impacts,
        "gdp_impact": round(template["gdp_base"] * severity_multiplier, 2),
        "inflation_impact": round(template["inflation_base"] * severity_multiplier, 2),
        "narrative": template["narrative"].format(severity=severity),
    }


def get_scenario_types() -> list[dict[str, str]]:
    """Return available scenario types with descriptions."""
    return [
        {"id": "oil_shock",              "name": "Oil Supply Shock",           "description": "Sudden disruption in global oil supply (Strait of Hormuz, OPEC collapse, etc.)"},
        {"id": "rate_hike",              "name": "Surprise Rate Hike",         "description": "Unexpected central bank tightening beyond market expectations"},
        {"id": "china_taiwan_conflict",  "name": "China-Taiwan Conflict",      "description": "Escalation of cross-strait tensions threatening semiconductor supply"},
        {"id": "global_recession",       "name": "Global Recession",           "description": "Synchronized economic contraction across major economies"},
        {"id": "usd_collapse",           "name": "USD Confidence Crisis",      "description": "Loss of confidence in US dollar as global reserve currency"},
        {"id": "climate_crisis",         "name": "Climate Emergency",          "description": "Cascade of extreme weather events forcing emergency carbon pricing"},
        {"id": "tech_bubble_burst",      "name": "Tech Bubble Burst",          "description": "AI hype cycle reversal triggering tech sector collapse"},
    ]


# ─── Risk Radar ──────────────────────────────────────────────────────────────

def get_risk_radar() -> dict[str, Any]:
    return {
        "systemic_risk_score": 6.8,
        "alerts": [
            {
                "id": "RISK-001",
                "severity": "critical",
                "title": "US Commercial Real Estate Debt Maturity Wall",
                "description": (
                    "$1.5 trillion in CRE loans mature in 2024-2025. Regional banks with concentrated "
                    "CRE exposure face potential liquidity crises. Office vacancy rates at 19.6% nationally."
                ),
                "affected_assets": ["Regional Bank ETF (KRE)", "Office REITs", "JPMorgan Chase", "US 10Y Treasury"],
                "timestamp": _ts(0),
            },
            {
                "id": "RISK-002",
                "severity": "high",
                "title": "China Property Sector Contagion Risk",
                "description": (
                    "Evergrande liquidation order sets precedent. Country Garden misses bond payments. "
                    "Shadow banking sector exposure estimated at $3 trillion. Local government financing "
                    "vehicles (LGFVs) face rollover risk."
                ),
                "affected_assets": ["Shanghai Composite", "USD/CNY", "BHP Group", "Rio Tinto", "Copper"],
                "timestamp": _ts(1),
            },
            {
                "id": "RISK-003",
                "severity": "high",
                "title": "Japanese Yen Carry Trade Unwind Risk",
                "description": (
                    "Bank of Japan yield curve control adjustment could trigger massive carry trade "
                    "unwinding. Estimated $4 trillion in yen-funded positions globally. Sudden JPY "
                    "appreciation would force cascading liquidations."
                ),
                "affected_assets": ["USD/JPY", "Nikkei 225", "Emerging Market Bonds", "AUD/USD"],
                "timestamp": _ts(2),
            },
            {
                "id": "RISK-004",
                "severity": "medium",
                "title": "US Fiscal Deficit Sustainability Concerns",
                "description": (
                    "US debt-to-GDP ratio exceeds 120%. Interest payments now exceed defense spending. "
                    "CBO projects $2.6 trillion deficit for FY2025. Bond vigilantes increasingly vocal."
                ),
                "affected_assets": ["US 10Y Treasury", "DXY (Dollar Index)", "Gold", "Bitcoin"],
                "timestamp": _ts(3),
            },
            {
                "id": "RISK-005",
                "severity": "medium",
                "title": "AI Concentration Risk in Equity Markets",
                "description": (
                    "Top 7 stocks represent 32% of S&P 500 market cap. NVIDIA alone accounts for "
                    "25% of S&P 500 YTD returns. Extreme concentration creates fragility -- any "
                    "single earnings miss could cascade through passive index funds."
                ),
                "affected_assets": ["NVIDIA Corp.", "S&P 500", "NASDAQ Composite", "TSMC", "Microsoft"],
                "timestamp": _ts(5),
            },
            {
                "id": "RISK-006",
                "severity": "low",
                "title": "European Energy Security - Winter 2025 Outlook",
                "description": (
                    "EU gas storage at 72% capacity heading into summer refill season. LNG imports "
                    "stable but Middle East shipping disruptions add risk premium. Industrial demand "
                    "recovery could tighten balances."
                ),
                "affected_assets": ["Natural Gas", "DAX", "EUR/USD", "Shell plc"],
                "timestamp": _ts(7),
            },
        ],
        "risk_categories": {
            "Geopolitical": 7.2,
            "Financial System": 6.5,
            "Market Structure": 7.8,
            "Macroeconomic": 6.0,
            "Climate / ESG": 5.4,
            "Cyber / Technology": 6.8,
        },
    }


# ─── Macro Report ────────────────────────────────────────────────────────────

def get_macro_report() -> dict[str, Any]:
    return {
        "title": "Global Macro Intelligence Briefing -- Q2 2025",
        "date": _ts(0)[:10],
        "summary": (
            "The global economy enters Q2 2025 in a state of fragile expansion. US growth "
            "remains resilient at 2.1% annualized but is decelerating from post-pandemic highs. "
            "The Eurozone narrowly avoids recession with 0.3% growth, while China's structural "
            "slowdown deepens with property sector woes weighing on sentiment. Central banks "
            "globally are navigating the last mile of disinflation, with the Fed signaling a "
            "potential pause. Key risks remain concentrated in commercial real estate, Chinese "
            "shadow banking, and AI-driven market concentration."
        ),
        "sections": [
            {
                "title": "United States",
                "content": (
                    "GDP growth: 2.1% (annualized). Inflation (Core PCE): 2.7%. Unemployment: 3.9%. "
                    "The labor market is cooling gradually, with job openings declining but layoffs remaining "
                    "low. Consumer spending is shifting from goods to services. The Fed is expected to hold "
                    "rates at 5.25-5.50% through June, with markets pricing first cut in September. "
                    "Fiscal concerns are mounting as the deficit approaches $2.6 trillion."
                ),
                "indicators": {"gdp": 2.1, "inflation": 2.7, "unemployment": 3.9, "pmi": 51.3},
            },
            {
                "title": "Eurozone",
                "content": (
                    "GDP growth: 0.3%. Inflation (HICP): 2.4%. Unemployment: 6.4%. Germany remains the weak "
                    "link with industrial production declining for the 5th consecutive quarter. France and "
                    "Spain show relative strength. The ECB is expected to cut rates in June, ahead of the Fed. "
                    "Energy security has improved but remains a structural vulnerability."
                ),
                "indicators": {"gdp": 0.3, "inflation": 2.4, "unemployment": 6.4, "pmi": 47.8},
            },
            {
                "title": "China",
                "content": (
                    "GDP growth: 4.7% (official, likely overstated). CPI: 0.3%. Youth unemployment: 14.7%. "
                    "The property sector continues to contract with new home prices falling for the 10th "
                    "consecutive month. Deflationary pressures are building. The PBOC has cut rates but "
                    "transmission to the real economy is weak. Export competitiveness in EVs and solar is "
                    "a bright spot, but trade tensions with the US and EU are escalating."
                ),
                "indicators": {"gdp": 4.7, "inflation": 0.3, "unemployment": 5.2, "pmi": 49.1},
            },
            {
                "title": "Emerging Markets",
                "content": (
                    "EM growth divergence continues. India (7.2%) and Vietnam (6.5%) lead Asia. "
                    "Brazil (1.8%) stabilizes while Argentina's radical reforms show early signs of "
                    "disinflation. Middle East benefits from energy prices but faces geopolitical risk. "
                    "Sub-Saharan Africa struggles with debt sustainability. EM currencies under pressure "
                    "from strong USD, with the carry trade providing partial offset."
                ),
                "indicators": {"avg_gdp": 4.2, "avg_inflation": 5.8},
            },
            {
                "title": "Markets & Asset Allocation",
                "content": (
                    "Equities are priced for a soft landing that may not materialize. The S&P 500 forward "
                    "P/E of 21x exceeds historical averages by 15%. Fixed income offers compelling yields "
                    "with US investment-grade bonds at 5.2%. Commodities are mixed: oil range-bound, gold "
                    "at all-time highs on central bank buying. We recommend a modest underweight in equities, "
                    "overweight in quality fixed income, and a strategic allocation to gold and select EM debt."
                ),
                "indicators": {"sp500_pe": 21.0, "us_ig_yield": 5.2, "vix": 14.8},
            },
        ],
        "outlook": (
            "The base case (55% probability) is a soft landing with gradual disinflation and "
            "modest growth deceleration. The bull case (20%) sees AI productivity gains accelerating "
            "growth without reigniting inflation. The bear case (25%) involves a credit event -- most "
            "likely in CRE or Chinese shadow banking -- that triggers a synchronized global slowdown. "
            "Key events to watch: FOMC meetings in June and July, China Third Plenum policy signals, "
            "and US election dynamics. Portfolio positioning should emphasize quality, diversification, "
            "and optionality."
        ),
    }


# ─── Company Profiles ────────────────────────────────────────────────────────

_COMPANY_PROFILES: dict[str, dict[str, Any]] = {
    "AAPL": {
        "ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology",
        "market_cap": 3.42e12, "pe_ratio": 28.5, "revenue": 3.83e11, "employees": 164000,
        "description": (
            "Apple designs, manufactures, and markets smartphones, personal computers, tablets, "
            "wearables, and accessories. The company also operates digital content stores and "
            "streaming services. Apple's ecosystem lock-in and brand loyalty provide exceptional "
            "pricing power. Key risks include China dependency for manufacturing and TSMC reliance."
        ),
        "financial_health_score": 92.0, "esg_score": 78.0, "geopolitical_exposure": 7.5,
    },
    "MSFT": {
        "ticker": "MSFT", "name": "Microsoft Corp.", "sector": "Technology",
        "market_cap": 3.18e12, "pe_ratio": 35.2, "revenue": 2.27e11, "employees": 221000,
        "description": (
            "Microsoft develops and licenses software, cloud services (Azure), and hardware. "
            "The company has positioned itself as a leader in enterprise AI through its partnership "
            "with OpenAI. Azure is the second-largest cloud platform globally. Key risks include "
            "antitrust scrutiny and AI capex returns."
        ),
        "financial_health_score": 95.0, "esg_score": 82.0, "geopolitical_exposure": 5.0,
    },
    "NVDA": {
        "ticker": "NVDA", "name": "NVIDIA Corp.", "sector": "Semiconductors",
        "market_cap": 2.84e12, "pe_ratio": 65.8, "revenue": 7.95e10, "employees": 29600,
        "description": (
            "NVIDIA designs GPUs and system-on-chip units for gaming, professional visualization, "
            "data centers, and automotive markets. The company dominates the AI training chip market "
            "with ~80% share. Its CUDA ecosystem creates deep moats. Key risks include TSMC fab "
            "dependency and potential demand normalization."
        ),
        "financial_health_score": 88.0, "esg_score": 71.0, "geopolitical_exposure": 8.5,
    },
    "GOOGL": {
        "ticker": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology",
        "market_cap": 2.17e12, "pe_ratio": 25.1, "revenue": 3.07e11, "employees": 182502,
        "description": (
            "Alphabet operates Google Search, YouTube, Android, cloud computing, and autonomous "
            "driving (Waymo). Advertising remains the primary revenue driver (~80%). The company "
            "faces antitrust action that could force structural changes. AI integration across "
            "search and cloud is critical to future growth."
        ),
        "financial_health_score": 91.0, "esg_score": 74.0, "geopolitical_exposure": 6.0,
    },
    "AMZN": {
        "ticker": "AMZN", "name": "Amazon.com Inc.", "sector": "E-Commerce / Cloud",
        "market_cap": 1.92e12, "pe_ratio": 58.4, "revenue": 5.75e11, "employees": 1525000,
        "description": (
            "Amazon operates the world's largest e-commerce platform and AWS, the leading cloud "
            "infrastructure provider. AWS generates ~65% of operating income despite being ~17% "
            "of revenue. Advertising is a fast-growing third pillar. Key risks include regulatory "
            "pressure and margin sustainability in retail."
        ),
        "financial_health_score": 85.0, "esg_score": 65.0, "geopolitical_exposure": 4.5,
    },
    "JPM": {
        "ticker": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financial Services",
        "market_cap": 5.72e11, "pe_ratio": 11.8, "revenue": 1.62e11, "employees": 309926,
        "description": (
            "JPMorgan Chase is the largest US bank by assets, operating across consumer banking, "
            "investment banking, commercial banking, and asset management. The bank benefits from "
            "higher rates through net interest income expansion. Key risks include CRE exposure "
            "and potential credit deterioration in a recession."
        ),
        "financial_health_score": 87.0, "esg_score": 68.0, "geopolitical_exposure": 6.5,
    },
    "TSLA": {
        "ticker": "TSLA", "name": "Tesla Inc.", "sector": "Automotive / Energy",
        "market_cap": 5.68e11, "pe_ratio": 42.3, "revenue": 9.68e10, "employees": 140473,
        "description": (
            "Tesla designs, manufactures, and sells electric vehicles, energy storage systems, "
            "and solar products. The company leads in EV market share but faces intensifying "
            "competition from Chinese manufacturers (BYD). Energy storage and FSD (Full Self-Driving) "
            "represent future optionality. Key risks include margin pressure and CEO distraction."
        ),
        "financial_health_score": 75.0, "esg_score": 55.0, "geopolitical_exposure": 7.0,
    },
    "2222": {
        "ticker": "2222.SR", "name": "Saudi Aramco", "sector": "Energy",
        "market_cap": 1.79e12, "pe_ratio": 15.2, "revenue": 5.35e11, "employees": 72543,
        "description": (
            "Saudi Aramco is the world's largest oil producer and most profitable company. "
            "It produces ~12 million barrels per day and has the lowest extraction costs globally. "
            "The company is central to Saudi Arabia's Vision 2030 diversification plan. Key risks "
            "include energy transition and geopolitical instability in the Middle East."
        ),
        "financial_health_score": 94.0, "esg_score": 35.0, "geopolitical_exposure": 9.0,
    },
    "TSMC": {
        "ticker": "TSM", "name": "Taiwan Semiconductor Manufacturing", "sector": "Semiconductors",
        "market_cap": 8.12e11, "pe_ratio": 24.6, "revenue": 6.92e10, "employees": 76478,
        "description": (
            "TSMC is the world's largest dedicated semiconductor foundry, manufacturing chips for "
            "Apple, NVIDIA, AMD, Qualcomm, and others. It controls 90%+ of advanced chips (sub-7nm). "
            "The company is building fabs in Arizona and Japan to diversify geopolitical risk. "
            "Key risks include China-Taiwan tensions and EUV equipment dependency on ASML."
        ),
        "financial_health_score": 90.0, "esg_score": 72.0, "geopolitical_exposure": 9.5,
    },
    "NVO": {
        "ticker": "NVO", "name": "Novo Nordisk A/S", "sector": "Healthcare / Pharmaceuticals",
        "market_cap": 5.62e11, "pe_ratio": 42.8, "revenue": 3.28e10, "employees": 63434,
        "description": (
            "Novo Nordisk is a global leader in diabetes and obesity care, known for GLP-1 drugs "
            "Ozempic and Wegovy. The obesity market is projected to reach $100B+ by 2030. "
            "The company has pricing power and deep clinical pipelines. Key risks include "
            "manufacturing capacity constraints and political pressure on drug pricing."
        ),
        "financial_health_score": 91.0, "esg_score": 85.0, "geopolitical_exposure": 3.5,
    },
    "META": {
        "ticker": "META", "name": "Meta Platforms Inc.", "sector": "Technology",
        "market_cap": 1.27e12, "pe_ratio": 24.9, "revenue": 1.35e11, "employees": 67317,
        "description": (
            "Meta operates Facebook, Instagram, WhatsApp, and Messenger, serving ~3.9 billion "
            "monthly active users. The company has pivoted to AI-first strategy after Metaverse "
            "investments. Digital advertising recovery and Reels monetization drive growth. "
            "Key risks include regulatory scrutiny, AI capex, and competition from TikTok."
        ),
        "financial_health_score": 89.0, "esg_score": 52.0, "geopolitical_exposure": 6.0,
    },
    "BHP": {
        "ticker": "BHP", "name": "BHP Group Ltd.", "sector": "Mining / Resources",
        "market_cap": 1.52e11, "pe_ratio": 12.4, "revenue": 5.36e10, "employees": 80000,
        "description": (
            "BHP is the world's largest mining company by market cap, producing iron ore, copper, "
            "nickel, potash, and coal. The company is pivoting toward future-facing commodities "
            "(copper, potash) critical for energy transition. Key risks include China demand "
            "slowdown and ESG-driven divestment from coal."
        ),
        "financial_health_score": 83.0, "esg_score": 62.0, "geopolitical_exposure": 7.0,
    },
}


def get_company_profile(ticker: str) -> dict[str, Any] | None:
    """Return company profile for a given ticker. Returns None if not found."""
    t = ticker.upper()
    return _COMPANY_PROFILES.get(t)


# ─── Portfolio Analysis ──────────────────────────────────────────────────────

def get_portfolio_analysis(holdings: list[dict[str, Any]]) -> dict[str, Any]:
    """Analyze a list of portfolio holdings and return risk/allocation metrics."""

    # Map sector weights
    sector_exposure: dict[str, float] = {}
    total_value = 0.0
    enriched: list[dict[str, Any]] = []

    for h in holdings:
        symbol = h.get("symbol", "UNKNOWN")
        weight = h.get("weight", 0.0)
        value = h.get("value", 0.0)
        name = h.get("name", symbol)

        # Try to get sector from known companies
        profile = _COMPANY_PROFILES.get(symbol.upper())
        sector = profile["sector"] if profile else h.get("sector", "Other")

        sector_exposure[sector] = sector_exposure.get(sector, 0.0) + weight
        total_value += value

        enriched.append({
            "symbol": symbol,
            "name": name,
            "weight": weight,
            "value": value,
            "sector": sector,
        })

    # Calculate diversification score (lower HHI = more diversified)
    hhi = sum(w ** 2 for w in sector_exposure.values())
    max_hhi = 1.0  # worst case: all in one sector
    diversification_score = round((1 - hhi / max_hhi) * 100, 1)

    # Simple risk score based on sector allocations (tech = higher risk, etc.)
    sector_risk = {
        "Technology": 7.5, "Semiconductors": 8.0, "E-Commerce / Cloud": 7.0,
        "Financial Services": 6.0, "Finance": 6.0, "Energy": 7.0,
        "Automotive / Energy": 8.0, "Automotive": 6.5, "Healthcare": 4.0,
        "Healthcare / Pharmaceuticals": 4.0, "Mining / Resources": 7.0,
        "Mining": 7.0, "Asset Mgmt": 5.5, "Other": 5.0,
    }
    risk_score = round(
        sum(sector_exposure.get(s, 0) * sector_risk.get(s, 5.0) for s in sector_exposure) / max(sum(sector_exposure.values()), 0.01),
        1,
    )

    # Generate recommendations
    recommendations = []
    if sector_exposure.get("Technology", 0) + sector_exposure.get("Semiconductors", 0) > 0.50:
        recommendations.append("Portfolio is heavily concentrated in technology. Consider diversifying into defensive sectors like healthcare or utilities.")
    if len(sector_exposure) < 3:
        recommendations.append("Very low sector diversification. Add exposure to at least 5 distinct sectors to reduce concentration risk.")
    if sector_exposure.get("Energy", 0) < 0.05:
        recommendations.append("Consider adding energy exposure as an inflation hedge and portfolio diversifier.")
    if not any(s in sector_exposure for s in ["Healthcare", "Healthcare / Pharmaceuticals"]):
        recommendations.append("No healthcare allocation detected. Healthcare provides defensive characteristics and demographic tailwinds.")
    if diversification_score < 50:
        recommendations.append("Diversification score is low. Rebalance to reduce single-sector dependency.")
    if risk_score > 7.0:
        recommendations.append("Overall risk score is elevated. Consider adding bonds or gold to reduce portfolio volatility.")
    if not recommendations:
        recommendations.append("Portfolio is well-diversified across sectors with balanced risk exposure.")
        recommendations.append("Consider periodic rebalancing to maintain target allocation weights.")

    return {
        "holdings": enriched,
        "total_value": total_value,
        "risk_score": risk_score,
        "diversification_score": diversification_score,
        "recommendations": recommendations,
        "sector_exposure": {k: round(v, 4) for k, v in sector_exposure.items()},
    }
