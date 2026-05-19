"""Risk monitoring routes for Glimmora MacroMind."""

from __future__ import annotations

from fastapi import APIRouter

from app.models.schemas import RiskAlert, RiskRadar
from app.services import risk_service

router = APIRouter(prefix="/api/risk", tags=["Risk"])


@router.get("/radar", response_model=RiskRadar)
async def risk_radar():
    """Return the systemic risk radar with all categories and alerts."""
    return risk_service.get_risk_radar()


@router.get("/alerts", response_model=list[RiskAlert])
async def risk_alerts():
    """Return current risk alerts sorted by severity."""
    return risk_service.get_risk_alerts()
