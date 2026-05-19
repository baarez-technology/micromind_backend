"""Market data service for Glimmora MacroMind.

Uses yfinance batch download for speed. Returns mock data instantly
if live data isn't cached yet, and refreshes in background.
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Any

from app.data.mock_data import get_market_overview as get_mock_data
from app.models.schemas import (
    Commodity,
    CryptoCoin,
    ForexPair,
    MarketIndex,
    MarketOverview,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
_live_cache: dict[str, Any] | None = None
_cache_ts: float = 0
_CACHE_TTL = 300  # 5 minutes
_fetching = False

# ---------------------------------------------------------------------------
# Symbol config
# ---------------------------------------------------------------------------
INDEX_SYMBOLS = {
    "^GSPC": "S&P 500", "^IXIC": "NASDAQ Composite", "^FTSE": "FTSE 100",
    "^N225": "Nikkei 225", "^GDAXI": "DAX", "000001.SS": "Shanghai Comp.",
}
FOREX_SYMBOLS = {
    "EURUSD=X": "EUR/USD", "GBPUSD=X": "GBP/USD", "USDJPY=X": "USD/JPY",
    "AUDUSD=X": "AUD/USD", "USDCHF=X": "USD/CHF", "USDCAD=X": "USD/CAD",
}
CRYPTO_SYMBOLS = {
    "BTC-USD": ("Bitcoin", "BTC"), "ETH-USD": ("Ethereum", "ETH"),
    "BNB-USD": ("BNB", "BNB"), "SOL-USD": ("Solana", "SOL"),
    "XRP-USD": ("XRP", "XRP"), "ADA-USD": ("Cardano", "ADA"),
}
COMMODITY_SYMBOLS = {
    "CL=F": ("Crude Oil (WTI)", "USD/bbl"), "GC=F": ("Gold", "USD/oz"),
    "SI=F": ("Silver", "USD/oz"), "NG=F": ("Natural Gas", "USD/MMBtu"),
    "HG=F": ("Copper", "USD/lb"), "ZW=F": ("Wheat", "USD/bu"),
}


def _background_fetch():
    """Fetch all market data via yfinance in one batch call. Runs in a thread."""
    global _live_cache, _cache_ts, _fetching
    _fetching = True
    try:
        import yfinance as yf

        all_symbols = (
            list(INDEX_SYMBOLS.keys()) +
            list(FOREX_SYMBOLS.keys()) +
            list(CRYPTO_SYMBOLS.keys()) +
            list(COMMODITY_SYMBOLS.keys())
        )

        # Batch download — single network call for all symbols
        df = yf.download(all_symbols, period="1mo", interval="1d", group_by="ticker", threads=True, progress=False)

        indices = []
        for sym, name in INDEX_SYMBOLS.items():
            try:
                if sym in df.columns.get_level_values(0):
                    closes = df[sym]["Close"].dropna().tolist()[-20:]
                else:
                    closes = df["Close"][sym].dropna().tolist()[-20:]
                if not closes:
                    continue
                price = round(closes[-1], 2)
                change = round(closes[-1] - closes[0], 2) if len(closes) > 1 else 0
                change_pct = round((change / closes[0]) * 100, 2) if closes[0] else 0
                indices.append({"name": name, "value": price, "change": change, "change_pct": change_pct, "sparkline": [round(c, 2) for c in closes]})
            except Exception as e:
                logger.debug("Index %s failed: %s", sym, e)

        forex = []
        for sym, pair in FOREX_SYMBOLS.items():
            try:
                if sym in df.columns.get_level_values(0):
                    closes = df[sym]["Close"].dropna().tolist()[-20:]
                else:
                    closes = df["Close"][sym].dropna().tolist()[-20:]
                if not closes:
                    continue
                rate = round(closes[-1], 4)
                change = round(closes[-1] - closes[0], 4) if len(closes) > 1 else 0
                change_pct = round((change / closes[0]) * 100, 2) if closes[0] else 0
                forex.append({"pair": pair, "rate": rate, "change": change, "change_pct": change_pct})
            except Exception as e:
                logger.debug("Forex %s failed: %s", sym, e)

        crypto = []
        for sym, (cname, csym) in CRYPTO_SYMBOLS.items():
            try:
                if sym in df.columns.get_level_values(0):
                    closes = df[sym]["Close"].dropna().tolist()[-20:]
                else:
                    closes = df["Close"][sym].dropna().tolist()[-20:]
                if not closes:
                    continue
                price = round(closes[-1], 2)
                change_24h = round(((closes[-1] - closes[-2]) / closes[-2]) * 100, 2) if len(closes) >= 2 else 0
                crypto.append({"name": cname, "symbol": csym, "price": price, "market_cap": price * 1e7, "change_24h": change_24h, "sparkline": [round(c, 2) for c in closes]})
            except Exception as e:
                logger.debug("Crypto %s failed: %s", sym, e)

        commodities = []
        for sym, (cname, unit) in COMMODITY_SYMBOLS.items():
            try:
                if sym in df.columns.get_level_values(0):
                    closes = df[sym]["Close"].dropna().tolist()[-20:]
                else:
                    closes = df["Close"][sym].dropna().tolist()[-20:]
                if not closes:
                    continue
                price = round(closes[-1], 2)
                change = round(closes[-1] - closes[0], 2) if len(closes) > 1 else 0
                change_pct = round((change / closes[0]) * 100, 2) if closes[0] else 0
                commodities.append({"name": cname, "price": price, "unit": unit, "change": change, "change_pct": change_pct})
            except Exception as e:
                logger.debug("Commodity %s failed: %s", sym, e)

        if indices or forex or crypto or commodities:
            _live_cache = {"indices": indices, "forex": forex, "crypto": crypto, "commodities": commodities}
            _cache_ts = time.time()
            logger.info("Live market data cached: %d indices, %d forex, %d crypto, %d commodities",
                        len(indices), len(forex), len(crypto), len(commodities))
    except Exception as e:
        logger.warning("Background market fetch failed: %s", e)
    finally:
        _fetching = False


def _ensure_live_data():
    """Kick off a background fetch if cache is stale. Never blocks."""
    global _fetching
    now = time.time()
    if _live_cache and now - _cache_ts < _CACHE_TTL:
        return  # cache is fresh
    if not _fetching:
        thread = threading.Thread(target=_background_fetch, daemon=True)
        thread.start()


def _get_data() -> dict:
    """Return live data if cached, otherwise mock data. Never blocks."""
    _ensure_live_data()
    if _live_cache:
        return _live_cache
    return get_mock_data()


# ---------------------------------------------------------------------------
# Public API (same signatures as before)
# ---------------------------------------------------------------------------

def get_markets() -> MarketOverview:
    data = _get_data()
    alerts = []
    # Generate alerts from data
    for idx in data.get("indices", []):
        if abs(idx.get("change_pct", 0)) > 1:
            direction = "surges" if idx["change_pct"] > 0 else "drops"
            alerts.append(f"{idx['name']} {direction} {abs(idx['change_pct']):.1f}%")
    if not alerts:
        alerts = data.get("alerts", ["Markets trading in normal range"])

    return MarketOverview(
        indices=[MarketIndex(**i) for i in data.get("indices", [])],
        forex=[ForexPair(**f) for f in data.get("forex", [])],
        crypto=[CryptoCoin(**c) for c in data.get("crypto", [])],
        commodities=[Commodity(**c) for c in data.get("commodities", [])],
        alerts=alerts[:5],
    )


def get_indices() -> list[MarketIndex]:
    data = _get_data()
    return [MarketIndex(**i) for i in data.get("indices", [])]


def get_forex() -> list[ForexPair]:
    data = _get_data()
    return [ForexPair(**f) for f in data.get("forex", [])]


def get_crypto() -> list[CryptoCoin]:
    data = _get_data()
    return [CryptoCoin(**c) for c in data.get("crypto", [])]


def get_commodities() -> list[Commodity]:
    data = _get_data()
    return [Commodity(**c) for c in data.get("commodities", [])]


def get_index_detail(symbol: str) -> MarketIndex | None:
    data = _get_data()
    sym = symbol.lower()
    for idx in data.get("indices", []):
        if sym in idx["name"].lower():
            return MarketIndex(**idx)
    return None


def search_markets(query: str) -> dict:
    q = query.lower()
    data = _get_data()
    return {
        "indices": [MarketIndex(**i) for i in data.get("indices", []) if q in i["name"].lower()],
        "forex": [ForexPair(**f) for f in data.get("forex", []) if q in f["pair"].lower()],
        "crypto": [CryptoCoin(**c) for c in data.get("crypto", []) if q in c["name"].lower() or q in c["symbol"].lower()],
        "commodities": [Commodity(**c) for c in data.get("commodities", []) if q in c["name"].lower()],
    }


def get_market_alerts() -> list[str]:
    data = _get_data()
    alerts = []
    for idx in data.get("indices", []):
        pct = idx.get("change_pct", 0)
        if abs(pct) > 1:
            alerts.append(f"{idx['name']} {'rallies' if pct > 0 else 'sells off'} {abs(pct):.1f}%")
    for c in data.get("crypto", []):
        pct = c.get("change_24h", 0)
        if abs(pct) > 5:
            alerts.append(f"{c['name']} {'surges' if pct > 0 else 'drops'} {abs(pct):.1f}% in 24h")
    return alerts[:5] if alerts else ["Markets trading within normal ranges"]
