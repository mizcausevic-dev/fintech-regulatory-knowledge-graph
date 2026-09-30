# Architecture

## Core idea

This project demonstrates a possible regulatory graph using entirely synthetic relationships:

- regulators and rules are named reference categories, not applicability decisions
- products and firms are fictional fixtures
- obligations, controls, and disclosures illustrate possible relationships, not verified compliance evidence

## Local-first graph

The graph is seeded from local Python models so the repo stays one-shot and deterministic:

- no graph database required
- no live SEC or FCA scraping required
- no credentials required

This keeps the demo deterministic for portfolio and schema exploration. It cannot establish a real firm's regulatory obligations or control posture.

## API surface

- `GET /api/summary` returns fixture counts and illustrative scores
- `GET /api/entities` filters by node type
- `GET /api/path` explains why two entities are connected
- `GET /api/export/jsonld` returns a machine-readable synthetic fixture for schema tests

## Why JSON-LD matters

The JSON-LD export is useful for:

- testing graph serialization and retrieval interfaces
- prototyping source-provenance fields and reviewer workflows
- evaluating how a future source-verified graph might support search and AI retrieval

Before production use, replace every fixture label and edge with a primary-source URL, retrieval date, jurisdiction and product-applicability decision, reviewer approval, and correction path. Do not feed this fixture to an agent as authoritative compliance context.
