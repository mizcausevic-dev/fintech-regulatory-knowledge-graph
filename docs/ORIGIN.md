# Why We Built This

**fintech-regulatory-knowledge-graph** started from a compliance reality that a lot of teams know intimately: the problem is usually not the absence of documents. It is the absence of a usable map. Rules, disclosures, filings, product notes, and risk interpretations may all exist, yet the people trying to answer a concrete question still end up stitching context together manually. Which regulator matters here, which obligation applies, which product is implicated, and what evidence would support that answer?

That problem gets worse as organizations add more products, markets, and compliance surfaces. A flat set of documents can describe the world, but it does not necessarily make the relationships inside that world operationally visible. When the knowledge remains disconnected, compliance work becomes slower, more brittle, and harder to explain to downstream teams.

We built **fintech-regulatory-knowledge-graph** to model those relationships explicitly. The repo is focused on a practical graph of regulators, firms, disclosures, financial products, and obligations. Its purpose is not to show that graphs are interesting. Its purpose is to show how regulated knowledge can be turned into something queryable, explainable, and increasingly useful to both humans and AI systems.

Existing tooling helps in pieces. Document stores preserve filings. GRC tools manage tasks. Search can find keywords. What they still do not naturally provide is an operational view of how regulatory context connects across entities. That is the gap this repo is meant to address.

That shaped the design philosophy:

- **relationship-first** so obligations are understood in context, not in isolation
- **evidence-aware** so graph answers still point back to documents and disclosures
- **operator-usable** so the output helps real compliance and product teams
- **AI-queryable** so the same structure can support modern answer systems without losing traceability

This repo also avoids presenting the graph as a magic compliance solution. It is a mapping and explainability layer. Its value is in making regulated knowledge easier to navigate and reason about.

Next on the roadmap is richer export formats, deeper obligation tracing, and stronger support for review workflows around product and market change. The long-term value of **fintech-regulatory-knowledge-graph** is that it makes compliance context less like a filing archive and more like an operational system.