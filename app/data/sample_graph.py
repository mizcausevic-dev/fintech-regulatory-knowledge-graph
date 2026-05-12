from __future__ import annotations

from app.models import GraphDataset, GraphEdge, GraphNode


def load_sample_graph() -> GraphDataset:
    return GraphDataset(
        nodes=[
            GraphNode(
                id="sec",
                type="regulator",
                label="U.S. Securities and Exchange Commission",
                summary="Primary U.S. securities regulator covering disclosures, custody posture, and market structure.",
                jurisdiction="United States",
                risk_pressure=88,
                source_document="Investment Advisers Act"
            ),
            GraphNode(
                id="finra",
                type="regulator",
                label="FINRA",
                summary="Self-regulatory body governing broker-dealer supervision, suitability, and communications posture.",
                jurisdiction="United States",
                risk_pressure=82,
                source_document="FINRA Rulebook"
            ),
            GraphNode(
                id="fca",
                type="regulator",
                label="Financial Conduct Authority",
                summary="UK regulator for conduct, consumer duty, and operational resilience expectations.",
                jurisdiction="United Kingdom",
                risk_pressure=79,
                source_document="FCA Handbook"
            ),
            GraphNode(
                id="brokerage-lending",
                type="product",
                label="Margin Lending Product",
                summary="Retail and institutional margin facility offered through the brokerage platform.",
                jurisdiction="United States",
                risk_pressure=76,
                source_document="Product shelf"
            ),
            GraphNode(
                id="stablecoin-sweep",
                type="product",
                label="Stablecoin Treasury Sweep",
                summary="Treasury placement product with crypto-adjacent settlement exposure and disclosure complexity.",
                jurisdiction="United States",
                risk_pressure=91,
                source_document="Treasury product memo"
            ),
            GraphNode(
                id="northstar-capital",
                type="firm",
                label="Northstar Capital Markets",
                summary="Sample fintech firm spanning brokerage, treasury operations, and institutional custody lanes.",
                jurisdiction="United States",
                risk_pressure=84,
                source_document="Corporate disclosure pack"
            ),
            GraphNode(
                id="rule-15c3-3",
                type="rule",
                label="SEC Rule 15c3-3",
                summary="Customer protection rule governing reserve and custody handling obligations.",
                jurisdiction="United States",
                risk_pressure=93,
                source_document="17 CFR 240.15c3-3"
            ),
            GraphNode(
                id="finra-3110",
                type="rule",
                label="FINRA Rule 3110",
                summary="Supervision rule requiring documented supervisory systems and escalation accountability.",
                jurisdiction="United States",
                risk_pressure=86,
                source_document="FINRA 3110"
            ),
            GraphNode(
                id="consumer-duty",
                type="rule",
                label="FCA Consumer Duty",
                summary="UK customer-outcomes regime with stronger governance and evidence expectations.",
                jurisdiction="United Kingdom",
                risk_pressure=77,
                source_document="PRIN 2A"
            ),
            GraphNode(
                id="capital-reserve-obligation",
                type="obligation",
                label="Daily reserve evidence",
                summary="Daily reserve evidence proving customer assets remain protected and reconciled.",
                jurisdiction="United States",
                risk_pressure=95,
                source_document="Reserve workbook"
            ),
            GraphNode(
                id="supervisory-review-obligation",
                type="obligation",
                label="Escalated supervisory review",
                summary="Formal review lane for higher-risk products, communications, and exception patterns.",
                jurisdiction="United States",
                risk_pressure=83,
                source_document="Supervisory manual"
            ),
            GraphNode(
                id="consumer-disclosure-obligation",
                type="obligation",
                label="Consumer outcome disclosure",
                summary="Narrative and quantitative disclosure proving customer outcomes remain fair and explainable.",
                jurisdiction="United Kingdom",
                risk_pressure=74,
                source_document="Disclosure deck"
            ),
            GraphNode(
                id="custody-control",
                type="control",
                label="Segregated custody control",
                summary="Operational control separating treasury sweep flows from customer custody assets.",
                jurisdiction="United States",
                risk_pressure=87,
                source_document="Control matrix"
            ),
            GraphNode(
                id="surveillance-control",
                type="control",
                label="Supervisory surveillance engine",
                summary="Control plane tracking suspicious flows, disclosure gaps, and approval exceptions.",
                jurisdiction="United States",
                risk_pressure=80,
                source_document="Surveillance runbook"
            ),
            GraphNode(
                id="risk-disclosure-pack",
                type="disclosure",
                label="Quarterly risk disclosure pack",
                summary="Board-ready disclosure package linking product posture to rules, controls, and evidence gaps.",
                jurisdiction="Multi-region",
                risk_pressure=72,
                source_document="Board materials"
            ),
        ],
        edges=[
            GraphEdge(source="sec", target="rule-15c3-3", relationship="oversees", rationale="SEC enforces customer protection handling."),
            GraphEdge(source="finra", target="finra-3110", relationship="oversees", rationale="FINRA governs supervision expectations."),
            GraphEdge(source="fca", target="consumer-duty", relationship="oversees", rationale="FCA owns the consumer duty framework."),
            GraphEdge(source="northstar-capital", target="brokerage-lending", relationship="offers", rationale="Firm distributes margin products."),
            GraphEdge(source="northstar-capital", target="stablecoin-sweep", relationship="offers", rationale="Firm distributes treasury sweep exposure."),
            GraphEdge(source="rule-15c3-3", target="capital-reserve-obligation", relationship="requires", rationale="Rule requires reserve evidence."),
            GraphEdge(source="finra-3110", target="supervisory-review-obligation", relationship="requires", rationale="Rule requires supervisory systems."),
            GraphEdge(source="consumer-duty", target="consumer-disclosure-obligation", relationship="requires", rationale="Rule requires outcome-focused disclosure."),
            GraphEdge(source="stablecoin-sweep", target="capital-reserve-obligation", relationship="maps_to", rationale="Treasury sweep product heightens reserve evidence pressure."),
            GraphEdge(source="brokerage-lending", target="supervisory-review-obligation", relationship="maps_to", rationale="Margin product triggers supervisory review posture."),
            GraphEdge(source="capital-reserve-obligation", target="custody-control", relationship="implements", rationale="Segregated custody is a core control response."),
            GraphEdge(source="supervisory-review-obligation", target="surveillance-control", relationship="implements", rationale="Surveillance engine enforces supervisory review."),
            GraphEdge(source="consumer-disclosure-obligation", target="risk-disclosure-pack", relationship="publishes", rationale="Disclosure pack satisfies customer outcome evidence."),
            GraphEdge(source="custody-control", target="risk-disclosure-pack", relationship="publishes", rationale="Control evidence flows into disclosure pack."),
            GraphEdge(source="surveillance-control", target="risk-disclosure-pack", relationship="publishes", rationale="Surveillance findings feed disclosure outputs."),
            GraphEdge(source="sec", target="northstar-capital", relationship="governs", rationale="Broker-dealer and advisory posture sits within SEC remit."),
            GraphEdge(source="finra", target="northstar-capital", relationship="governs", rationale="Supervision and suitability posture sits within FINRA remit."),
            GraphEdge(source="fca", target="stablecoin-sweep", relationship="governs", rationale="UK distribution posture creates conduct obligations.")
        ]
    )
