"""Scenario simulation service for Glimmora MacroMind."""

from __future__ import annotations

from app.data.mock_data import get_scenario_impacts, get_scenario_types
from app.models.schemas import ScenarioImpact, ScenarioRequest, ScenarioResult


def list_scenario_types() -> list[dict[str, str]]:
    """Return all available scenario types."""
    return get_scenario_types()


def simulate_scenario(request: ScenarioRequest) -> ScenarioResult:
    """Simulate a scenario and return cascading impacts."""
    data = get_scenario_impacts(request.scenario_type, request.severity)

    return ScenarioResult(
        scenario=data["scenario"],
        impacts=[ScenarioImpact(**imp) for imp in data["impacts"]],
        gdp_impact=data["gdp_impact"],
        inflation_impact=data["inflation_impact"],
        narrative=data["narrative"],
    )
