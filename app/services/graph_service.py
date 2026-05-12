from __future__ import annotations

from collections import deque

from app.data.sample_graph import load_sample_graph
from app.models import GraphDataset, GraphEdge, GraphNode, GraphSummary, JsonLdEntity, KnowledgePath, PathStep


class GraphService:
    def __init__(self) -> None:
        self.dataset = load_sample_graph()
        self.nodes = {node.id: node for node in self.dataset.nodes}
        self.outbound: dict[str, list[GraphEdge]] = {}
        for edge in self.dataset.edges:
            self.outbound.setdefault(edge.source, []).append(edge)

    def summary(self) -> GraphSummary:
        obligations = [node for node in self.dataset.nodes if node.type == "obligation"]
        controls = [node for node in self.dataset.nodes if node.type == "control"]
        regulators = [node for node in self.dataset.nodes if node.type == "regulator"]
        high_pressure = sorted(
            [node for node in self.dataset.nodes if node.risk_pressure >= 85],
            key=lambda node: node.risk_pressure,
            reverse=True
        )[:5]

        return GraphSummary(
            node_count=len(self.dataset.nodes),
            edge_count=len(self.dataset.edges),
            regulator_count=len(regulators),
            obligation_count=len(obligations),
            control_count=len(controls),
            high_pressure_entities=[node.label for node in high_pressure],
            lead_recommendation="Stabilize reserve evidence and supervisory review links before expanding treasury-sweep distribution."
        )

    def entity(self, entity_id: str) -> GraphNode:
        return self.nodes[entity_id]

    def entities(self, node_type: str | None = None) -> list[GraphNode]:
        if node_type is None:
            return self.dataset.nodes
        return [node for node in self.dataset.nodes if node.type == node_type]

    def outbound_edges(self, entity_id: str) -> list[GraphEdge]:
        return self.outbound.get(entity_id, [])

    def lead_paths(self) -> list[KnowledgePath]:
        return [
            self.path_between("sec", "risk-disclosure-pack"),
            self.path_between("stablecoin-sweep", "custody-control"),
            self.path_between("finra", "surveillance-control"),
        ]

    def path_between(self, start: str, end: str) -> KnowledgePath:
        queue: deque[tuple[str, list[GraphEdge]]] = deque([(start, [])])
        seen = {start}

        while queue:
            current, path = queue.popleft()
            if current == end:
                steps = [
                    PathStep(source=self.nodes[edge.source].label, relationship=edge.relationship, target=self.nodes[edge.target].label)
                    for edge in path
                ]
                return KnowledgePath(
                    start=self.nodes[start].label,
                    end=self.nodes[end].label,
                    steps=steps,
                    summary=self._path_summary(path)
                )

            for edge in self.outbound.get(current, []):
                if edge.target in seen:
                    continue
                seen.add(edge.target)
                queue.append((edge.target, [*path, edge]))

        return KnowledgePath(
            start=self.nodes[start].label,
            end=self.nodes[end].label,
            steps=[],
            summary="No path found."
        )

    def jsonld_export(self) -> JsonLdEntity:
        graph_items: list[dict] = []
        for node in self.dataset.nodes:
            graph_items.append(
                {
                    "@id": f"urn:finreg:{node.id}",
                    "@type": self._jsonld_type(node),
                    "name": node.label,
                    "description": node.summary,
                    "jurisdiction": node.jurisdiction,
                    "identifier": node.id,
                    "isPartOf": node.source_document,
                    "measurementTechnique": "Risk pressure scoring",
                    "additionalProperty": {
                        "@type": "PropertyValue",
                        "name": "riskPressure",
                        "value": node.risk_pressure
                    }
                }
            )

        for edge in self.dataset.edges:
            graph_items.append(
                {
                    "@id": f"urn:finreg:edge:{edge.source}:{edge.relationship}:{edge.target}",
                    "@type": "DefinedTerm",
                    "name": edge.relationship,
                    "description": edge.rationale,
                    "subjectOf": {"@id": f"urn:finreg:{edge.source}"},
                    "inDefinedTermSet": {"@id": f"urn:finreg:{edge.target}"}
                }
            )

        return JsonLdEntity(
            data={
                "@context": {
                    "@vocab": "https://schema.org/",
                    "FinancialProduct": "https://schema.org/FinancialProduct",
                    "DefinedTerm": "https://schema.org/DefinedTerm"
                },
                "@type": "Dataset",
                "name": "Fintech Regulatory Knowledge Graph",
                "description": "Structured graph connecting regulators, rules, products, obligations, controls, and disclosures for AI-queryable compliance context.",
                "creator": {
                    "@type": "Person",
                    "name": "Miz Causevic"
                },
                "distribution": {
                    "@type": "DataDownload",
                    "encodingFormat": "application/ld+json"
                },
                "@graph": graph_items
            }
        )

    def _jsonld_type(self, node: GraphNode) -> str:
        mapping = {
            "regulator": "Organization",
            "regulation": "Legislation",
            "rule": "Legislation",
            "firm": "Organization",
            "product": "FinancialProduct",
            "control": "DefinedTerm",
            "obligation": "DefinedTerm",
            "disclosure": "CreativeWork"
        }
        return mapping[node.type]

    def _path_summary(self, edges: list[GraphEdge]) -> str:
        if not edges:
            return "No path found."
        labels = [self.nodes[edges[0].source].label]
        for edge in edges:
            labels.append(self.nodes[edge.target].label)
        return " → ".join(labels)


graph_service = GraphService()
