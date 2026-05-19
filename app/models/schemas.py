"""Pydantic models for Glimmora MacroMind API responses."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ─── Market Data ─────────────────────────────────────────────────────────────

class MarketIndex(BaseModel):
    name: str
    value: float
    change: float
    change_pct: float
    sparkline: list[float] = Field(default_factory=list)


class ForexPair(BaseModel):
    pair: str
    rate: float
    change: float
    change_pct: float


class CryptoCoin(BaseModel):
    name: str
    symbol: str
    price: float
    market_cap: float
    change_24h: float
    sparkline: list[float] = Field(default_factory=list)


class Commodity(BaseModel):
    name: str
    price: float
    unit: str
    change: float
    change_pct: float


class MarketOverview(BaseModel):
    indices: list[MarketIndex]
    forex: list[ForexPair]
    crypto: list[CryptoCoin]
    commodities: list[Commodity]
    alerts: list[str] = Field(default_factory=list)


# ─── Knowledge Graph ─────────────────────────────────────────────────────────

class KnowledgeGraphNode(BaseModel):
    id: str
    label: str
    type: str
    sector: str | None = None
    market_cap: float | None = None
    country: str | None = None


class KnowledgeGraphEdge(BaseModel):
    source: str
    target: str
    relationship: str
    strength: float = Field(ge=0.0, le=1.0)


class KnowledgeGraph(BaseModel):
    nodes: list[KnowledgeGraphNode]
    edges: list[KnowledgeGraphEdge]


# ─── Scenario Simulation ─────────────────────────────────────────────────────

class ScenarioRequest(BaseModel):
    scenario_type: str
    severity: int = Field(ge=1, le=10, default=5)
    description: str | None = None


class ScenarioImpact(BaseModel):
    asset_class: str
    asset_name: str
    impact_pct: float
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str


class ScenarioResult(BaseModel):
    scenario: str
    impacts: list[ScenarioImpact]
    gdp_impact: float
    inflation_impact: float
    narrative: str


# ─── Analysis ─────────────────────────────────────────────────────────────────

class AnalysisQuery(BaseModel):
    query: str


class AnalysisResponse(BaseModel):
    query: str
    answer: str
    data_points: list[dict[str, Any]] = Field(default_factory=list)
    charts: list[dict[str, Any]] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)


# ─── Risk ─────────────────────────────────────────────────────────────────────

class RiskAlert(BaseModel):
    id: str
    severity: str
    title: str
    description: str
    affected_assets: list[str] = Field(default_factory=list)
    timestamp: str


class RiskRadar(BaseModel):
    systemic_risk_score: float
    alerts: list[RiskAlert]
    risk_categories: dict[str, float] = Field(default_factory=dict)


# ─── Portfolio ────────────────────────────────────────────────────────────────

class PortfolioHolding(BaseModel):
    symbol: str
    name: str
    weight: float
    value: float
    sector: str


class PortfolioAnalysis(BaseModel):
    holdings: list[PortfolioHolding]
    total_value: float
    risk_score: float
    diversification_score: float
    recommendations: list[str] = Field(default_factory=list)
    sector_exposure: dict[str, float] = Field(default_factory=dict)


# ─── Macro Report ────────────────────────────────────────────────────────────

class MacroReport(BaseModel):
    title: str
    date: str
    summary: str
    sections: list[dict[str, Any]] = Field(default_factory=list)
    outlook: str


# ─── Company Profile ─────────────────────────────────────────────────────────

class CompanyProfile(BaseModel):
    ticker: str
    name: str
    sector: str
    market_cap: float
    pe_ratio: float
    revenue: float
    employees: int
    description: str
    financial_health_score: float
    esg_score: float
    geopolitical_exposure: float
