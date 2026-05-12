# Architecture

## Core idea

This project models fintech regulatory pressure as a graph:

- regulators explain jurisdiction and oversight
- rules explain why pressure exists
- products explain where pressure is created
- obligations explain what must happen
- controls explain how the firm answers the pressure
- disclosures explain how the story becomes auditable and AI-queryable

## Local-first graph

The graph is seeded from local Python models so the repo stays one-shot and deterministic:

- no graph database required
- no live SEC or FCA scraping required
- no credentials required

That makes it much easier to run in a hiring, consulting, or portfolio context while still telling a credible RegTech story.

## API surface

- `GET /api/summary` returns graph posture
- `GET /api/entities` filters by node type
- `GET /api/path` explains why two entities are connected
- `GET /api/export/jsonld` publishes machine-readable evidence for downstream AI and search agents

## Why JSON-LD matters

This repo is not only a graph exploration demo. It also publishes a structured semantic export, which makes it useful for:

- AI-grounded compliance Q&A
- internal policy retrieval
- structured evidence handoff
- future AEO / GEO style regulatory knowledge publishing
