"""Analysis routes for Glimmora MacroMind."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.data.mock_data import get_company_profile as _get_profile, get_macro_report as _get_report
from app.models.schemas import AnalysisQuery, AnalysisResponse, CompanyProfile, MacroReport
from app.services import analysis_service

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])


@router.post("/query", response_model=AnalysisResponse)
async def analyze(request: AnalysisQuery):
    """Analyze a natural-language query and return relevant financial intelligence."""
    return analysis_service.analyze_query(request.query)


@router.get("/macro-report", response_model=MacroReport)
async def macro_report():
    """Return the latest macro intelligence report."""
    data = _get_report()
    return MacroReport(**data)


@router.get("/company/{ticker}", response_model=CompanyProfile)
async def company_profile(ticker: str):
    """Return a detailed company profile for the given ticker."""
    profile = _get_profile(ticker)
    if profile is None:
        raise HTTPException(
            status_code=404,
            detail=f"Company profile not found for ticker: {ticker.upper()}",
        )
    return CompanyProfile(**profile)
