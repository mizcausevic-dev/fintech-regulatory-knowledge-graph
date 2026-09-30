from __future__ import annotations

import json
import os
from html import escape

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

from app.services.graph_service import graph_service


def shell(title: str, section: str, body: str) -> str:
    summary = graph_service.summary()
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <style>
      :root {{
        --bg:#07111b;
        --panel:#152236;
        --panel-alt:#101a2a;
        --line:rgba(104,142,199,.24);
        --text:#eef4ff;
        --muted:#9eb5d6;
        --accent:#86caff;
        --gold:#f3e4c2;
        --warn:#ffd48a;
      }}
      * {{ box-sizing:border-box; }}
      body {{
        margin:0;
        color:var(--text);
        font-family:Inter,Segoe UI,sans-serif;
        background:
          radial-gradient(circle at top left, rgba(62,112,180,.24), transparent 28%),
          linear-gradient(180deg, #06101a 0%, #091423 100%);
      }}
      main {{
        width:min(1460px,calc(100% - 40px));
        margin:20px auto;
        padding:22px;
        border-radius:30px;
        border:1px solid var(--line);
        background:linear-gradient(180deg, rgba(11,18,31,.96), rgba(8,14,25,.98));
      }}
      .topbar,.panel,.hero,.metric,.card,.export-box {{
        border:1px solid var(--line);
        border-radius:28px;
        background:linear-gradient(180deg, rgba(20,32,50,.92), rgba(14,23,37,.95));
      }}
      .topbar {{
        display:flex;
        justify-content:space-between;
        gap:16px;
        align-items:center;
        padding:12px 14px;
        margin-bottom:18px;
      }}
      .brand {{
        color:var(--accent);
        letter-spacing:.28em;
        font-size:12px;
        font-weight:700;
        text-transform:uppercase;
      }}
      .lane {{
        color:var(--muted);
        letter-spacing:.16em;
        text-transform:uppercase;
        font-size:12px;
        margin-left:14px;
      }}
      .status {{
        display:flex;
        gap:10px;
        flex-wrap:wrap;
      }}
      .chip,.nav a {{
        border:1px solid rgba(104,142,199,.22);
        border-radius:999px;
        background:rgba(21,34,54,.82);
        padding:10px 14px;
        color:var(--text);
        font-size:13px;
        text-decoration:none;
        font-weight:600;
      }}
      .nav a.active {{
        color:var(--accent);
        background:rgba(134,202,255,.12);
      }}
      .nav a:focus-visible {{ outline:3px solid var(--warn); outline-offset:3px; }}
      .hero {{
        display:grid;
        grid-template-columns:1.45fr .95fr;
        gap:18px;
        padding:28px;
        margin-bottom:20px;
      }}
      .hero-side {{
        padding:0;
      }}
      .eyebrow {{
        color:var(--accent);
        letter-spacing:.28em;
        text-transform:uppercase;
        font-size:12px;
        font-weight:700;
      }}
      h1,h2,h3 {{
        margin:12px 0 14px;
        font-family:Georgia,serif;
        letter-spacing:-.025em;
        color:var(--gold);
      }}
      h1 {{ font-size:clamp(40px,4.1vw,64px); line-height:1.06; }}
      h2 {{ font-size:clamp(30px,3vw,42px); line-height:1.12; }}
      h3 {{ font-size:clamp(24px,2vw,30px); line-height:1.16; }}
      .hero-side h3 {{ overflow-wrap:break-word; }}
      p,li {{ color:var(--muted); line-height:1.55; }}
      .lede {{ font-size:22px; max-width:900px; }}
      .metrics,.grid-2,.grid-3 {{
        display:grid;
        gap:18px;
      }}
      .metrics {{ grid-template-columns:repeat(4,1fr); margin-bottom:20px; }}
      .grid-2 {{ grid-template-columns:1.06fr .94fr; }}
      .grid-3 {{ grid-template-columns:repeat(3,1fr); }}
      .grid-2 > *, .grid-3 > * {{ min-width:0; }}
      .metric,.card,.panel,.export-box {{ padding:22px; }}
      .metric strong {{
        display:block;
        margin:14px 0 10px;
        font-size:52px;
        line-height:.95;
        color:var(--gold);
        font-family:Georgia,serif;
      }}
      .metric-label {{
        font-size:12px;
        color:var(--muted);
        letter-spacing:.18em;
        text-transform:uppercase;
      }}
      .nav {{
        display:flex;
        gap:10px;
        flex-wrap:wrap;
        margin-bottom:18px;
      }}
      .list {{
        display:grid;
        gap:16px;
      }}
      .card-title {{
        font-family:Georgia,serif;
        color:var(--gold);
        font-size:26px;
        margin:10px 0;
      }}
      .tag {{
        display:inline-block;
        padding:8px 12px;
        border-radius:999px;
        background:rgba(21,34,54,.82);
        border:1px solid rgba(104,142,199,.22);
        color:var(--accent);
        font-size:12px;
        text-transform:uppercase;
        letter-spacing:.08em;
        font-weight:700;
      }}
      .mono, pre {{
        font-family:Consolas,Monaco,monospace;
        font-size:13px;
        line-height:1.55;
      }}
      pre {{
        margin:0;
        white-space:pre-wrap;
        word-break:break-word;
        color:var(--text);
      }}
      table {{
        width:100%;
        border-collapse:collapse;
        table-layout:fixed;
      }}
      th,td {{
        text-align:left;
        padding:14px 12px;
        border-bottom:1px solid rgba(104,142,199,.12);
        vertical-align:top;
        overflow-wrap:anywhere;
      }}
      th {{
        color:var(--accent);
        letter-spacing:.18em;
        font-size:12px;
        text-transform:uppercase;
      }}
      @media (max-width:1120px) {{
        .hero,.grid-2,.grid-3,.metrics {{ grid-template-columns:repeat(2,1fr); }}
      }}
      @media (max-width:780px) {{
        main {{ width:calc(100% - 20px); padding:14px; }}
        .hero,.grid-2,.grid-3,.metrics {{ grid-template-columns:1fr; }}
        h1 {{ font-size:clamp(32px,9vw,48px); }}
        th,td {{ padding:10px 6px; }}
      }}
    </style>
  </head>
  <body>
    <main>
      <p class="tag" role="note">Synthetic demonstration · no verified legal analysis or firm evidence</p>
      <section class="topbar">
        <div>
          <span class="brand">FINTECH REGULATORY KNOWLEDGE GRAPH</span>
          <span class="lane">{section}</span>
        </div>
        <div class="status">
          <span class="chip">Nodes {summary.node_count}</span>
          <span class="chip">Edges {summary.edge_count}</span>
          <span class="chip">High pressure {len(summary.high_pressure_entities)}</span>
        </div>
      </section>
      {body}
    </main>
  </body>
</html>"""


app = FastAPI(
    title="Fintech Regulatory Knowledge Graph",
    description="Synthetic local demonstration of graph relationships. No rule applicability, source evidence, or legal conclusion is verified.",
    version="1.0.0"
)


@app.get("/", response_class=HTMLResponse)
def overview() -> str:
    summary = graph_service.summary()
    paths = graph_service.lead_paths()
    lead_nodes = sorted(graph_service.entities(), key=lambda item: item.risk_pressure, reverse=True)[:3]
    return shell(
        "Fintech Regulatory Knowledge Graph",
        "OVERVIEW LANE",
        f"""
        <section class="hero">
          <article>
            <p class="eyebrow">Illustrative regulatory graph</p>
            <h1>Turn filings, rules, and product obligations into an AI-queryable fintech graph.</h1>
            <p class="lede">Explore how a graph could connect regulators, rules, products, firms, obligations, controls, and disclosures. Every product, score, evidence label, and relationship here is an illustrative fixture requiring counsel and source verification before use.</p>
          </article>
          <article class="hero-side">
            <nav class="nav" aria-label="Demo pages">
              <a class="active" aria-current="page" href="/">Overview</a>
              <a href="/graph">Graph board</a>
              <a href="/evidence">Evidence export</a>
              <a href="/docs">Docs</a>
            </nav>
            <p class="eyebrow">Sample review prompt</p>
            <h3>{summary.lead_recommendation}</h3>
            <p>The sample graph highlights reserve evidence around a fictional treasury sweep. The mapping is a hypothesis for review, not a determination that a rule applies to a real product.</p>
          </article>
        </section>
        <section class="metrics">
          <article class="metric"><div class="metric-label">Graph nodes</div><strong>{summary.node_count}</strong><p>Regulators, products, rules, obligations, controls, and disclosures.</p></article>
          <article class="metric"><div class="metric-label">Graph edges</div><strong>{summary.edge_count}</strong><p>Governance, requirement, control, and publishing relationships.</p></article>
          <article class="metric"><div class="metric-label">Regulators</div><strong>{summary.regulator_count}</strong><p>SEC, FINRA, and FCA anchor the current sample set.</p></article>
          <article class="metric"><div class="metric-label">Control pressure</div><strong>{summary.control_count}</strong><p>Control entities showing how obligations map into operational safeguards.</p></article>
        </section>
        <section class="grid-2">
          <article class="panel">
            <p class="eyebrow">Lead paths</p>
            <h2>Why the graph matters operationally.</h2>
            <div class="list">
              {"".join(
                  f'<div class="card"><span class="tag">path</span><div class="card-title">{path.start} → {path.end}</div><p>{path.summary}</p></div>'
                  for path in paths
              )}
            </div>
          </article>
          <article class="panel">
            <p class="eyebrow">High-pressure entities</p>
            <h2>Where the compliance story gets expensive.</h2>
            <div class="list">
              {"".join(
                  f'<div class="card"><span class="tag">{node.type}</span><div class="card-title">{node.label}</div><p>{node.summary}</p><p class="mono">risk_pressure={node.risk_pressure}</p></div>'
                  for node in sorted(lead_nodes, key=lambda item: item.risk_pressure, reverse=True)
              )}
            </div>
          </article>
        </section>
        """
    )


@app.get("/graph", response_class=HTMLResponse)
def graph_board() -> str:
    entities = graph_service.entities()
    regulators = [node for node in entities if node.type == "regulator"]
    products = [node for node in entities if node.type == "product"]
    obligations = [node for node in entities if node.type == "obligation"]
    controls = [node for node in entities if node.type == "control"]
    return shell(
        "Graph Board",
        "GRAPH BOARD",
        f"""
        <section class="hero">
          <article>
            <p class="eyebrow">Graph board</p>
            <h1>Regulators, products, obligations, and controls all sit in one traversable decision surface.</h1>
            <p class="lede">This board demonstrates how a candidate graph might connect products, rules, and controls. Its relationships and scores are synthetic and have not been validated against a firm's facts or current law.</p>
          </article>
          <article class="hero-side">
            <nav class="nav" aria-label="Demo pages">
              <a href="/">Overview</a>
              <a class="active" aria-current="page" href="/graph">Graph board</a>
              <a href="/evidence">Evidence export</a>
              <a href="/docs">Docs</a>
            </nav>
            <p class="eyebrow">Cluster lens</p>
            <h3>Four clusters drive the story.</h3>
            <p>The fixture groups regulators, products, obligations, and possible controls for review. Its edges do not establish jurisdiction, applicability, or control effectiveness.</p>
          </article>
        </section>
        <section class="grid-3">
          <article class="panel"><p class="eyebrow">Regulators</p><h2>Who governs</h2>{"".join(f'<div class="card"><div class="card-title">{node.label}</div><p>{node.summary}</p></div>' for node in regulators)}</article>
          <article class="panel"><p class="eyebrow">Products</p><h2>What creates pressure</h2>{"".join(f'<div class="card"><div class="card-title">{node.label}</div><p>{node.summary}</p><p class="mono">risk_pressure={node.risk_pressure}</p></div>' for node in products)}</article>
          <article class="panel"><p class="eyebrow">Obligations + controls</p><h2>How pressure gets answered</h2>{"".join(f'<div class="card"><span class="tag">{node.type}</span><div class="card-title">{node.label}</div><p>{node.summary}</p></div>' for node in [*obligations, *controls])}</article>
        </section>
        """
    )


@app.get("/evidence", response_class=HTMLResponse)
def evidence_export() -> str:
    export = graph_service.jsonld_export().data
    paths = graph_service.lead_paths()
    export_json = json.dumps(export, indent=2)
    return shell(
        "Evidence Export",
        "EVIDENCE EXPORT",
        f"""
        <section class="hero">
          <article>
            <p class="eyebrow">Evidence export</p>
            <h1>Inspect synthetic relationship paths and a JSON-LD graph export.</h1>
            <p class="lede">This lane exports the synthetic graph as JSON-LD for schema testing. It is not a source-verified evidence package or a basis for an automated compliance answer.</p>
          </article>
          <article class="hero-side">
            <nav class="nav" aria-label="Demo pages">
              <a href="/">Overview</a>
              <a href="/graph">Graph board</a>
              <a class="active" aria-current="page" href="/evidence">Evidence export</a>
              <a href="/docs">Docs</a>
            </nav>
            <p class="eyebrow">Export use case</p>
            <h3>Schema test only.</h3>
            <p>Exported source labels are fixture text, and risk scores are illustrative. A production graph needs source URLs, retrieval dates, reviewer approval, and applicability decisions before agents cite it.</p>
          </article>
        </section>
        <section class="grid-2">
          <article class="panel">
            <p class="eyebrow">Lead evidence chains</p>
            <h2>Sample paths to test and review.</h2>
            <table>
              <thead><tr><th>Start</th><th>End</th><th>Path</th></tr></thead>
              <tbody>
                {"".join(f'<tr><td>{path.start}</td><td>{path.end}</td><td>{path.summary}</td></tr>' for path in paths)}
              </tbody>
            </table>
          </article>
          <article class="export-box">
            <p class="eyebrow">JSON-LD sample</p>
            <h2>Structured export</h2>
            <pre>{escape(export_json)}</pre>
          </article>
        </section>
        """
    )


@app.get("/api/summary")
def api_summary():
    return graph_service.summary()


@app.get("/api/entities")
def api_entities(node_type: str | None = Query(default=None)):
    return graph_service.entities(node_type=node_type)


@app.get("/api/path")
def api_path(start: str, end: str):
    try:
        return graph_service.path_between(start, end)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown entity: {exc.args[0]}") from exc


@app.get("/api/export/jsonld")
def api_export_jsonld():
    return graph_service.jsonld_export().data


@app.get("/api/sample")
def api_sample():
    return {
        "summary": graph_service.summary(),
        "lead_paths": graph_service.lead_paths()[:2],
        "sample_entity": graph_service.entity("stablecoin-sweep")
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "4591"))
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)
