"""Live forex exchange rate service for Glimmora MacroMind.

Fetches real-time exchange rates from the free open.er-api.com API (no key needed).
"""

from __future__ import annotations

import logging
import time

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
_fx_cache: dict = {"data": None, "ts": 0}
_CACHE_TTL = 600  # 10 minutes


def get_live_exchange_rates(base: str = "USD") -> dict:
    """Fetch live exchange rates from the free open.er-api.com API.

    Rates are cached for 10 minutes to respect the upstream rate limit.

    Parameters
    ----------
    base : str
        The base currency code (e.g. "USD", "EUR", "GBP").

    Returns
    -------
    dict
        A mapping of currency code -> exchange rate relative to *base*.
        Returns cached data (or empty dict) if the request fails.
    """
    now = time.time()

    # Return cached data if still fresh
    if _fx_cache["data"] and now - _fx_cache["ts"] < _CACHE_TTL:
        return _fx_cache["data"]

    try:
        resp = httpx.get(
            f"https://open.er-api.com/v6/latest/{base}",
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        _fx_cache["data"] = data.get("rates", {})
        _fx_cache["ts"] = now
        return _fx_cache["data"]
    except Exception as e:
        logger.warning(f"Failed to fetch live FX rates: {e}")
        return _fx_cache.get("data") or {}
