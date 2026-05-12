from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


NodeType = Literal[
    "regulator",
    "regulation",
    "rule",
    "firm",
    "product",
    "control",
    "obligation",
    "disclosure"
]

EdgeType = Literal[
    "oversees",
    "governs",
    "offers",
    "requires",
    "implements",
    "publishes",
    "maps_to"
]


class GraphNode(BaseModel):
    id: str
    type: NodeType
    label: str
    summary: str
    jurisdiction: str | None = None
    risk_pressure: int = Field(ge=0, le=100)
    source_document: str | None = None


class GraphEdge(BaseModel):
    source: str
    target: str
    relationship: EdgeType
    rationale: str


class PathStep(BaseModel):
    source: str
    relationship: str
    target: str


class KnowledgePath(BaseModel):
    start: str
    end: str
    steps: list[PathStep]
    summary: str


class GraphSummary(BaseModel):
    node_count: int
    edge_count: int
    regulator_count: int
    obligation_count: int
    control_count: int
    high_pressure_entities: list[str]
    lead_recommendation: str


class JsonLdEntity(BaseModel):
    data: dict


class GraphDataset(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]

