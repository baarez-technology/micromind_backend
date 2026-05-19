"""Scenario simulation routes for Glimmora MacroMind."""

from __future__ import annotations

from fastapi import APIRouter

from app.models.schemas import ScenarioRequest, ScenarioResult
from app.services import scenario_service

router = APIRouter(prefix="/api/scenarios", tags=["Scenarios"])


@router.get("/types")
async def get_scenario_types():
    """List all available scenario types for simulation."""
    return scenario_service.list_scenario_types()


@router.post("/simulate", response_model=ScenarioResult)
async def simulate(request: ScenarioRequest):
    """Run a scenario simulation and return cascading impacts."""
    return scenario_service.simulate_scenario(request)
