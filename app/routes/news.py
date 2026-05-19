"""News API routes for Glimmora MacroMind."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.services import news_service

router = APIRouter(prefix="/api/news", tags=["News"])


@router.get("/")
async def get_news(limit: int = Query(20, ge=1, le=50)):
    """Get latest financial news from multiple RSS feeds."""
    return {"articles": news_service.fetch_financial_news(limit)}


@router.get("/search")
async def search_news(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=30),
):
    """Search financial news by keyword."""
    return {"articles": news_service.search_news(q, limit)}


@router.get("/alerts")
async def get_alerts():
    """Get current market alerts derived from news headlines."""
    return {"alerts": news_service.fetch_market_alerts()}
