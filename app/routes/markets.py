"""Market data routes for Glimmora MacroMind."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import Commodity, CryptoCoin, ForexPair, MarketIndex, MarketOverview
from app.services import market_service

router = APIRouter(prefix="/api/markets", tags=["Markets"])


@router.get("/", response_model=MarketOverview)
async def market_overview():
    """Return full market overview: indices, forex, crypto, commodities, and alerts."""
    return market_service.get_markets()


@router.get("/indices", response_model=list[MarketIndex])
async def get_indices():
    """Return all stock market indices."""
    return market_service.get_indices()


@router.get("/forex", response_model=list[ForexPair])
async def get_forex():
    """Return all forex pairs."""
    return market_service.get_forex()


@router.get("/crypto", response_model=list[CryptoCoin])
async def get_crypto():
    """Return all cryptocurrency data."""
    return market_service.get_crypto()


@router.get("/commodities", response_model=list[Commodity])
async def get_commodities():
    """Return all commodity prices."""
    return market_service.get_commodities()


@router.get("/search")
async def search_markets(q: str = Query(..., min_length=1, description="Search query")):
    """Search across all market data."""
    results = market_service.search_markets(q)
    return results
