"""Glimmora MacroMind -- AGI Global Financial Intelligence Platform.

FastAPI application entry point.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import analysis, knowledge, markets, news, portfolio, risk, scenarios

app = FastAPI(
    title="Glimmora MacroMind",
    description="AGI Global Financial Intelligence Platform -- API Backend",
    version="1.0.0",
    redirect_slashes=True,
)

# ─── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(markets.router)
app.include_router(analysis.router)
app.include_router(scenarios.router)
app.include_router(knowledge.router)
app.include_router(risk.router)
app.include_router(portfolio.router)
app.include_router(news.router)


# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "online",
        "platform": "Glimmora MacroMind",
        "version": "1.0.0",
        "message": "AGI Global Financial Intelligence Platform -- Backend API",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
