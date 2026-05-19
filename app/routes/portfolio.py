"""Portfolio analysis routes for Glimmora MacroMind."""

from __future__ import annotations

from fastapi import APIRouter

from app.models.schemas import PortfolioAnalysis, PortfolioHolding
from app.services import portfolio_service

router = APIRouter(prefix="/api/portfolio", tags=["Portfolio"])


@router.post("/analyze", response_model=PortfolioAnalysis)
async def analyze_portfolio(holdings: list[PortfolioHolding]):
    """Analyze a portfolio and return risk metrics, diversification score, and recommendations."""
    holdings_dicts = [h.model_dump() for h in holdings]
    return portfolio_service.analyze_portfolio(holdings_dicts)
