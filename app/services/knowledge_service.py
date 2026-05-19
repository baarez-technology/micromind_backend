"""Knowledge graph service for Glimmora MacroMind."""

from __future__ import annotations

from app.data.mock_data import get_knowledge_graph
from app.models.schemas import KnowledgeGraph, KnowledgeGraphEdge, KnowledgeGraphNode


def get_full_graph() -> KnowledgeGraph:
    """Return the complete knowledge graph."""
    data = get_knowledge_graph()
    return KnowledgeGraph(
        nodes=[KnowledgeGraphNode(**n) for n in data["nodes"]],
        edges=[KnowledgeGraphEdge(**e) for e in data["edges"]],
    )


def get_entity_connections(entity_id: str) -> KnowledgeGraph:
    """Return a subgraph containing only the specified entity and its direct connections."""
    data = get_knowledge_graph()
    eid = entity_id.upper()

    # Find edges connected to this entity
    connected_edges = [
        e for e in data["edges"]
        if e["source"] == eid or e["target"] == eid
    ]

    # Collect all connected node IDs
    connected_ids = {eid}
    for edge in connected_edges:
        connected_ids.add(edge["source"])
        connected_ids.add(edge["target"])

    # Filter nodes
    connected_nodes = [n for n in data["nodes"] if n["id"] in connected_ids]

    return KnowledgeGraph(
        nodes=[KnowledgeGraphNode(**n) for n in connected_nodes],
        edges=[KnowledgeGraphEdge(**e) for e in connected_edges],
    )


def search_entities(query: str) -> list[KnowledgeGraphNode]:
    """Search for entities matching the query."""
    data = get_knowledge_graph()
    q = query.lower()

    results = []
    for node in data["nodes"]:
        if (
            q in node["id"].lower()
            or q in node["label"].lower()
            or q in node["type"].lower()
            or (node.get("sector") and q in node["sector"].lower())
            or (node.get("country") and q in node["country"].lower())
        ):
            results.append(KnowledgeGraphNode(**node))

    return results
