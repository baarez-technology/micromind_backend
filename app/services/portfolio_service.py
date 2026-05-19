"""Portfolio analysis service for Glimmora MacroMind."""

from __future__ import annotations

from app.data.mock_data import get_portfolio_analysis as _analyze
from app.models.schemas import PortfolioAnalysis, PortfolioHolding


def analyze_portfolio(holdings: list[dict]) -> PortfolioAnalysis:
    """Analyze a list of portfolio holdings and return risk metrics + recommendations."""
    data = _analyze(holdings)
    return PortfolioAnalysis(
        holdings=[PortfolioHolding(**h) for h in data["holdings"]],
        total_value=data["total_value"],
        risk_score=data["risk_score"],
        diversification_score=data["diversification_score"],
        recommendations=data["recommendations"],
        sector_exposure=data["sector_exposure"],
    )
