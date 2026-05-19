"""Risk monitoring service for Glimmora MacroMind."""

from __future__ import annotations

from app.data.mock_data import get_risk_radar as _get_risk_data
from app.models.schemas import RiskAlert, RiskRadar


def get_risk_radar() -> RiskRadar:
    """Return the current systemic risk radar."""
    data = _get_risk_data()
    return RiskRadar(
        systemic_risk_score=data["systemic_risk_score"],
        alerts=[RiskAlert(**a) for a in data["alerts"]],
        risk_categories=data["risk_categories"],
    )


def get_risk_alerts() -> list[RiskAlert]:
    """Return only the current risk alerts."""
    data = _get_risk_data()
    return [RiskAlert(**a) for a in data["alerts"]]


def get_risk_detail(risk_id: str) -> RiskAlert | None:
    """Return detailed information for a specific risk alert."""
    data = _get_risk_data()
    for alert in data["alerts"]:
        if alert["id"] == risk_id:
            return RiskAlert(**alert)
    return None
