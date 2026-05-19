"""Knowledge graph routes for Glimmora MacroMind."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.models.schemas import KnowledgeGraph, KnowledgeGraphNode
from app.services import knowledge_service

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge Graph"])


@router.get("/graph", response_model=KnowledgeGraph)
async def full_graph():
    """Return the full knowledge graph of global financial entities and relationships."""
    return knowledge_service.get_full_graph()


@router.get("/entity/{entity_id}", response_model=KnowledgeGraph)
async def entity_connections(entity_id: str):
    """Return the entity and its direct connections as a subgraph."""
    return knowledge_service.get_entity_connections(entity_id)


@router.get("/search", response_model=list[KnowledgeGraphNode])
async def search_entities(q: str = Query(..., min_length=1, description="Search query")):
    """Search for entities in the knowledge graph."""
    return knowledge_service.search_entities(q)
